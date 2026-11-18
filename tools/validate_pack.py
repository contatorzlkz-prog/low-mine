#!/usr/bin/env python3
"""Static validator for LowMine Ultra Low .mcpack files.

Checks archive integrity, manifest identity/version, settings, translations,
fog references, registered UI overrides and key assets. It does not launch
Minecraft, prove UI compatibility or measure FPS.
"""
from __future__ import annotations
import argparse, collections, json, os, re, struct, sys, uuid, zipfile
from pathlib import PurePosixPath

QUERY = re.compile(r"query\.(?:get_pack_setting|is_pack_setting_enabled)\s*\(\s*['\"]([^'\"]+)['\"]")

def png_size(data):
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])

def validate(filename):
    errors, report = [], {}
    try:
        z = zipfile.ZipFile(filename)
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Cannot open archive: {exc}"], report
    with z:
        if z.testzip():
            errors.append("ZIP CRC check failed")
        names = [i.filename for i in z.infolist() if not i.is_dir()]
        unique = set(names)
        if len(names) != len(unique):
            errors.append("Duplicate archive paths")
        if any(PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts or "\\" in n for n in names):
            errors.append("Unsafe archive path")
        report["files"] = len(names)
        if "manifest.json" not in unique:
            return errors + ["manifest.json missing at root"], report
        parsed, bad_json = {}, []
        for name in names:
            if name.lower().endswith(".json"):
                try:
                    parsed[name] = json.loads(z.read(name).decode("utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    bad_json.append(f"{name}: {exc}")
        errors.extend("Invalid JSON " + x for x in bad_json)
        report["json_files"] = len(parsed)
        report["invalid_json"] = len(bad_json)
        m = parsed.get("manifest.json", {})
        h = m.get("header", {})
        report["pack_name"] = h.get("name")
        report["version"] = h.get("version")
        if m.get("format_version") != 3 or h.get("version") != [0, 3, 0]:
            errors.append("Expected manifest format 3 and version [0, 3, 0]")
        if m.get("subpacks") or any(n.startswith("subpacks/") or "pvp_fps" in n.lower() for n in names):
            errors.append("PvP/subpack content must not exist in Ultra Low")
        if "pbr" in m.get("capabilities", []):
            errors.append("PBR capability present without PBR assets")
        meta = m.get("metadata", {})
        if "XiaoCraft" not in " ".join(meta.get("authors", [])) or "CC BY-NC 3.0" not in str(meta.get("license", "")):
            errors.append("Original author/license attribution missing")
        ids = [h.get("uuid")] + [x.get("uuid") for x in m.get("modules", [])]
        try:
            for value in ids:
                uuid.UUID(str(value))
        except (ValueError, TypeError, AttributeError):
            errors.append("Invalid/missing UUID")
        if len(ids) != len(set(ids)):
            errors.append("Manifest UUIDs are not unique")

        settings = [s for s in m.get("settings", []) if s.get("type") in ("slider", "toggle")]
        setting_ids = [s.get("name") for s in settings]
        if len(settings) != 8 or len(setting_ids) != len(set(setting_ids)):
            errors.append(f"Expected 8 unique settings, found {len(settings)}")
        report["active_settings"] = {s.get("name"): s.get("default") for s in settings}

        refs = collections.Counter()
        for name in names:
            if PurePosixPath(name).suffix.lower() in (".json", ".lang", ".ui", ".material"):
                txt = z.read(name).decode("utf-8-sig", errors="replace")
                refs.update(QUERY.findall(txt))
                if "bfps:" in txt or "xiao:fog_" in txt:
                    errors.append(f"Old internal namespace remains: {name}")
        if set(refs) != set(setting_ids):
            errors.append(f"Settings/query mismatch: missing {set(setting_ids)-set(refs)}, extra {set(refs)-set(setting_ids)}")
        report["setting_queries"] = dict(refs)

        langs = [n for n in names if n.endswith(".lang")]
        missing = {}
        for item in m.get("settings", []):
            key = item.get("text")
            if not isinstance(key, str):
                continue
            for name in langs:
                content = z.read(name).decode("utf-8-sig", errors="replace")
                if not re.search(rf"^{re.escape(key)}=", content, re.M):
                    missing.setdefault(key, []).append(name)
        if missing:
            errors.append(f"Missing setting translations: {missing}")
        report["language_files"] = len(langs)

        biome = parsed.get("biomes_client.json", {}).get("biomes", {})
        fog_refs = {v.get("fog_identifier") for v in biome.values() if isinstance(v, dict) and v.get("fog_identifier")}
        fog_ids = set()
        for name, data in parsed.items():
            if name.startswith("fogs/") and name.endswith(".json"):
                fog_ids.add(data.get("minecraft:fog_settings", {}).get("description", {}).get("identifier"))
        missing_fog = sorted(x for x in fog_refs if x.startswith("lowmine:") and x not in fog_ids)
        if missing_fog:
            errors.append(f"Missing custom fog definitions: {missing_fog}")
        report["biomes"] = len(biome)
        report["fog_definitions"] = len(fog_ids)

        registered = parsed.get("ui/_ui_defs.json", {}).get("ui_defs", [])
        required_ui = ["ui/inventory_screen.json", "ui/chest_screen.json", "ui/data_driven_container_screen.json"]
        for name in required_ui:
            if name not in registered or name not in parsed:
                errors.append(f"UI override missing or not registered: {name}")
        inv = parsed.get("ui/inventory_screen.json", {})
        for key in ("inventory_screen@crafting.inventory_screen_base", "crafting_screen@crafting.inventory_screen_base"):
            if inv.get(key, {}).get("$screen_background_alpha") != 0.08:
                errors.append(f"Inventory alpha override missing: {key}")
        chest = parsed.get("ui/chest_screen.json", {})
        for key in ("small_chest_screen@common.inventory_screen_common", "large_chest_screen@common.inventory_screen_common",
                    "ender_chest_screen@common.inventory_screen_common", "shulker_box_screen@chest.small_chest_screen",
                    "barrel_screen@chest.small_chest_screen"):
            variables = chest.get(key, {}).get("variables", [])
            if len(variables) < 2 or variables[0].get("$screen_background_alpha") != 0.08 or variables[1].get("requires") != "$pocket_screen":
                errors.append(f"Chest UI override incomplete: {key}")
        dd = parsed.get("ui/data_driven_container_screen.json", {}).get("screen@common.inventory_screen_common", {}).get("variables", [])
        if len(dd) < 2 or dd[0].get("$screen_background_alpha") != 0.08:
            errors.append("Data-driven container UI override incomplete")
        report["registered_ui_overrides"] = [x for x in required_ui if x in registered]

        pngs = [n for n in names if n.lower().endswith(".png")]
        pixels, dimensions = 0, {}
        for name in pngs:
            size = png_size(z.read(name))
            if not size:
                errors.append(f"Invalid PNG header: {name}")
                continue
            pixels += size[0] * size[1]
            if name in ("pack_icon.png", "textures/ui/pack_icon.png", "textures/ui/title.png", "textures/environment/clouds.png"):
                dimensions[name] = size
        report["png_files"] = len(pngs)
        report["png_pixels"] = pixels
        report["rgba_texel_estimate_mb"] = round(pixels * 4 / 1_000_000, 3)
        report["key_png_dimensions"] = dimensions
        if "ATTRIBUTION.txt" not in unique:
            errors.append("ATTRIBUTION.txt missing")
        else:
            notice = z.read("ATTRIBUTION.txt").decode("utf-8", errors="replace")
            if "XiaoCraft" not in notice or "CC BY-NC 3.0" not in notice:
                errors.append("Attribution notice incomplete")
        report["archive_bytes"] = os.path.getsize(filename)
    return errors, report

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pack", help="Path to .mcpack")
    args = ap.parse_args()
    errors, report = validate(args.pack)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if errors:
        print("\nVALIDATION FAILED:", file=sys.stderr)
        for item in errors:
            print("- " + item, file=sys.stderr)
        return 1
    print("\nStatic validation passed. Runtime behavior and FPS still need in-game tests.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
