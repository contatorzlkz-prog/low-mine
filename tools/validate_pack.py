#!/usr/bin/env python3
"""Static validator for Minecraft Bedrock .mcpack archives.

This checks archive structure and JSON syntax. It does not launch Minecraft,
prove runtime compatibility, or measure FPS.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
import zipfile
from pathlib import Path


def validate_pack(path: Path) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    report: dict[str, object] = {}

    if not path.is_file():
        return [f"File not found: {path}"], report

    if not zipfile.is_zipfile(path):
        return ["Input is not a valid ZIP/.mcpack archive."], report

    try:
        with zipfile.ZipFile(path) as archive:
            bad_member = archive.testzip()
            if bad_member:
                errors.append(f"Corrupted ZIP member: {bad_member}")

            names = [name for name in archive.namelist() if not name.endswith("/")]
            name_set = set(names)
            report["entries"] = len(names)

            if "manifest.json" not in name_set:
                errors.append("manifest.json is missing from the archive root.")
                return errors, report

            try:
                manifest = json.loads(archive.read("manifest.json").decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                errors.append(f"Invalid manifest.json: {exc}")
                return errors, report

            header = manifest.get("header", {})
            modules = manifest.get("modules", [])
            report["pack_name"] = header.get("name")
            report["version"] = header.get("version")
            report["min_engine_version"] = header.get("min_engine_version")
            report["subpacks"] = [
                item.get("folder_name") for item in manifest.get("subpacks", [])
            ]

            ids: list[str] = []
            for label, value in [
                ("header.uuid", header.get("uuid")),
                *[
                    (f"modules[{index}].uuid", module.get("uuid"))
                    for index, module in enumerate(modules)
                ],
            ]:
                if not value:
                    errors.append(f"{label} is missing.")
                    continue
                try:
                    uuid.UUID(str(value))
                except ValueError:
                    errors.append(f"{label} is not a valid UUID: {value}")
                ids.append(str(value))
            if len(ids) != len(set(ids)):
                errors.append("Manifest header/module UUIDs are not unique.")

            json_files = [name for name in names if name.lower().endswith(".json")]
            json_errors: list[str] = []
            for name in json_files:
                try:
                    json.loads(archive.read(name).decode("utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    json_errors.append(f"{name}: {exc}")
            report["json_files_checked"] = len(json_files)
            report["invalid_json_files"] = len(json_errors)
            errors.extend(json_errors)

            for subpack in manifest.get("subpacks", []):
                folder = str(subpack.get("folder_name", "")).strip("/")
                if folder and not any(name.startswith(folder + "/") for name in names):
                    errors.append(f"Declared subpack folder is missing: {folder}")

            report["attribution_notice"] = "ATTRIBUTION.txt" in name_set
            if not report["attribution_notice"]:
                errors.append("ATTRIBUTION.txt is missing.")

    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"Could not read archive: {exc}")

    return errors, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="Path to a .mcpack file")
    args = parser.parse_args()

    errors, report = validate_pack(args.pack)
    print(json.dumps(report, indent=2, ensure_ascii=False))

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("\nStatic validation passed. This is not an in-game compatibility or FPS test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
