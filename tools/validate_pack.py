#!/usr/bin/env python3
"""Static validator for LowMine Bedrock resource-pack archives.

Checks ZIP integrity, manifest identifiers, JSON syntax, pack-setting wiring,
translations, subpack folders, fog references and key PNG assets. It cannot run
Minecraft or measure actual performance.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import struct
import sys
import uuid
import zipfile
from pathlib import PurePosixPath

SETTING_CALL = re.compile(
    r"query\.(?:get_pack_setting|is_pack_setting_enabled)\s*\(\s*['\"]([^'\"]+)['\"]"
)


def png_size(data: bytes) -> tuple[int, int] | None:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def validate(path: str) -> tuple[list[str], list[str], dict[str, object]]:
    errors: list[str] = []
    warnings: list[str] = []
    report: dict[str, object] = {}

    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Cannot open ZIP: {exc}"], warnings, report

    with archive:
        corrupt = archive.testzip()
        if corrupt:
            errors.append(f"ZIP integrity failure: {corrupt}")

        names = [i.filename for i in archive.infolist() if not i.is_dir()]
        name_set = set(names)
        duplicates = [n for n, count in collections.Counter(names).items() if count > 1]
        unsafe = [n for n in names if PurePosixPath(n).is_absolute()
                  or ".." in PurePosixPath(n).parts or "\\" in n]
        if duplicates:
            errors.append(f"Duplicate paths: {duplicates[:10]}")
        if unsafe:
            errors.append(f"Unsafe paths: {unsafe[:10]}")

        report["archive_entries"] = len(names)
        report["extension_counts"] = dict(collections.Counter(
            PurePosixPath(n).suffix.lower() or "[no extension]" for n in names
        ))

        if "manifest.json" not in name_set:
            return errors + ["manifest.json missing at archive root"], warnings, report

        try:
            manifest = json.loads(archive.read("manifest.json").decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            return errors + [f"Invalid manifest.json: {exc}"], warnings, report

        header = manifest.get("header", {})
        modules = manifest.get("modules", [])
        report["manifest_format"] = manifest.get("format_version")
        report["pack_name"] = header.get("name")
        report["pack_version"] = header.get("version")
        report["min_engine_version"] = header.get("min_engine_version")

        if manifest.get("format_version") != 3:
            errors.append("Expected manifest format_version 3")
        if header.get("version") != "0.2.0":
            warnings.append(f"Expected header version 0.2.0, found {header.get('version')!r}")
        metadata = manifest.get("metadata", {})
        if not metadata.get("authors"):
            errors.append("metadata.authors missing")
        if "CC BY-NC 3.0" not in str(metadata.get("license", "")):
            errors.append("metadata.license must identify CC BY-NC 3.0")

        uuids: list[str] = []
        for label, value in [
            ("header.uuid", header.get("uuid")),
            *[(f"modules[{i}].uuid", m.get("uuid")) for i, m in enumerate(modules)],
        ]:
            if not value:
                errors.append(f"{label} missing")
                continue
            try:
                uuid.UUID(str(value))
                uuids.append(str(value))
            except ValueError:
                errors.append(f"Invalid {label}: {value}")
        if len(uuids) != len(set(uuids)):
            errors.append("Manifest UUIDs are not unique")

        for subpack in manifest.get("subpacks", []):
            folder = str(subpack.get("folder_name", "")).strip("/")
            archive_folder = f"subpacks/{folder}/" if folder else ""
            if not folder or not any(n.startswith(archive_folder) for n in names):
                errors.append(f"Subpack folder missing: {archive_folder!r}")

        settings = [s for s in manifest.get("settings", [])
                    if s.get("type") in {"toggle", "slider"}]
        setting_ids = [s.get("name") for s in settings]
        if len(setting_ids) != len(set(setting_ids)):
            errors.append("Duplicate setting identifiers")
        report["configurable_controls"] = len(settings)
        report["settings"] = {s.get("name"): s.get("default") for s in settings}
        if len(settings) != 9:
            warnings.append(f"Expected 9 controls, found {len(settings)}")

        json_names = [n for n in names if n.lower().endswith(".json")]
        parsed: dict[str, object] = {}
        bad_json: list[str] = []
        for name in json_names:
            try:
                parsed[name] = json.loads(archive.read(name).decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                bad_json.append(f"{name}: {exc}")
        report["json_checked"] = len(json_names)
        report["invalid_json"] = len(bad_json)
        errors.extend(bad_json)

        setting_refs: collections.Counter[str] = collections.Counter()
        old_ids: list[str] = []
        for name in names:
            if PurePosixPath(name).suffix.lower() not in {".json", ".lang", ".ui", ".material"}:
                continue
            try:
                content = archive.read(name).decode("utf-8-sig")
            except UnicodeDecodeError:
                continue
            setting_refs.update(SETTING_CALL.findall(content))
            if "bfps:" in content or "xiao:fog_" in content:
                old_ids.append(name)
        for ref in setting_refs:
            if ref not in setting_ids:
                errors.append(f"Undefined setting queried: {ref}")
        for key in setting_ids:
            if not setting_refs[key]:
                errors.append(f"Declared setting is never queried: {key}")
        if old_ids:
            errors.append(f"Old internal namespace remains: {old_ids[:10]}")
        report["setting_query_references"] = dict(setting_refs)

        langs = [n for n in names if n.endswith(".lang")]
        missing_labels: dict[str, list[str]] = {}
        for setting in manifest.get("settings", []):
            key = setting.get("text")
            if not isinstance(key, str):
                continue
            absent = []
            for filename in langs:
                text = archive.read(filename).decode("utf-8-sig", errors="replace")
                if not re.search(rf"^{re.escape(key)}=", text, re.MULTILINE):
                    absent.append(filename)
            if absent:
                missing_labels[key] = absent
        report["language_files"] = len(langs)
        report["missing_setting_labels"] = missing_labels
        if missing_labels:
            errors.append("Setting labels are missing from language files")

        fog_report = {}
        for biome_file, fog_dir in [
            ("biomes_client.json", "fogs/"),
            ("subpacks/fps/biomes_client.json", "subpacks/fps/fogs/"),
        ]:
            data = parsed.get(biome_file)
            if not isinstance(data, dict):
                errors.append(f"Biome file missing or invalid: {biome_file}")
                continue
            biomes = data.get("biomes", {})
            refs = {v.get("fog_identifier") for v in biomes.values()
                    if isinstance(v, dict) and v.get("fog_identifier")}
            defined: set[str] = set()
            for filename in names:
                if filename.startswith(fog_dir) and filename.endswith(".json"):
                    fog_doc = parsed.get(filename)
                    if isinstance(fog_doc, dict):
                        fog = fog_doc.get("minecraft:fog_settings", {})
                        ident = fog.get("description", {}).get("identifier") if isinstance(fog, dict) else None
                        if ident:
                            defined.add(ident)
            missing = sorted(v for v in refs if v.startswith("lowmine:") and v not in defined)
            if missing:
                errors.append(f"Unresolved custom fog IDs in {biome_file}: {missing[:10]}")
            fog_report[biome_file] = {
                "biomes": len(biomes),
                "fog_references": len(refs),
                "definitions": len(defined),
                "missing_custom_ids": missing,
            }
        report["fog_audit"] = fog_report

        required = ["ATTRIBUTION.txt", "pack_icon.png",
                    "textures/ui/pack_icon.png", "textures/ui/title.png"]
        for name in required:
            if name not in name_set:
                errors.append(f"Required file missing: {name}")
        image_sizes = {}
        for name in required[1:]:
            if name in name_set:
                size = png_size(archive.read(name))
                if not size:
                    errors.append(f"Invalid PNG: {name}")
                else:
                    image_sizes[name] = size
        report["png_dimensions"] = image_sizes

        if "ATTRIBUTION.txt" in name_set:
            notice = archive.read("ATTRIBUTION.txt").decode("utf-8", errors="replace")
            if "XiaoCraft" not in notice or "CC BY-NC 3.0" not in notice:
                errors.append("Attribution notice must include XiaoCraft and CC BY-NC 3.0")

    return errors, warnings, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", help="Path to .mcpack")
    args = parser.parse_args()
    errors, warnings, report = validate(args.pack)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    for item in warnings:
        print(f"WARNING: {item}", file=sys.stderr)
    if errors:
        print("\nVALIDATION FAILED:", file=sys.stderr)
        for item in errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    print("\nStatic validation passed; this does not test Minecraft runtime compatibility or FPS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
