#!/usr/bin/env python3
"""Validate a LowMine Ultra Low v0.3.2 Bedrock .mcpack.

Static checks only: archive, manifest, JSON, particles, fog, UI registration,
translucent UI textures and attribution. Does not launch Minecraft or measure FPS.
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, re, struct, sys, uuid, zipfile
from pathlib import PurePosixPath
from PIL import Image
from io import BytesIO

EXPECTED_VERSION = "0.3.2"
REQUIRED_UI = [
    "ui/inventory_screen.json",
    "ui/inventory_screen_pocket.json",
    "ui/chest_screen.json",
    "ui/data_driven_container_screen.json",
]

def validate(filename: str):
    errors, report = [], {}
    try:
        archive = zipfile.ZipFile(filename)
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"Cannot open mcpack: {exc}"], report

    with archive:
        bad = archive.testzip()
        if bad:
            errors.append(f"ZIP CRC failed at {bad}")
        infos = [item for item in archive.infolist() if not item.is_dir()]
        names = [item.filename for item in infos]
        unique = set(names)
        if len(names) != len(unique):
            errors.append("Duplicate archive paths found")
        if any(PurePosixPath(n).is_absolute() or ".." in PurePosixPath(n).parts or "\\" in n for n in names):
            errors.append("Unsafe absolute or parent-relative path found")
        report["archive_entries"] = len(names)

        if "manifest.json" not in unique:
            return errors + ["manifest.json must be at archive root"], report

        parsed, invalid = {}, []
        for name in names:
            if name.lower().endswith(".json"):
                try:
                    parsed[name] = json.loads(archive.read(name).decode("utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    invalid.append(f"{name}: {exc}")
        errors.extend("Invalid JSON: " + item for item in invalid)
        report["json_files"] = len(parsed)
        report["invalid_json"] = len(invalid)

        manifest = parsed.get("manifest.json", {})
        header = manifest.get("header", {})
        modules = manifest.get("modules", [])
        report["pack_name"] = header.get("name")
        report["version"] = header.get("version")

        if manifest.get("format_version") != 3:
            errors.append("manifest format_version must be 3")
        if not isinstance(header.get("version"), str) or header.get("version") != EXPECTED_VERSION:
            errors.append("header.version must be the SemVer string '0.3.2'")
        if not isinstance(header.get("min_engine_version"), str):
            errors.append("manifest v3 min_engine_version must be a string")
        if not modules or any(not isinstance(m.get("version"), str) or m.get("version") != EXPECTED_VERSION for m in modules):
            errors.append("all module.version values must be the SemVer string '0.3.2'")
        if "settings" in manifest:
            errors.append("Experimental custom pack settings must be absent")
        if "subpacks" in manifest:
            errors.append("Ultra Low must be a single profile with no subpacks")
        if any(n.startswith("subpacks/") or "pvp_fps" in n.lower() for n in names):
            errors.append("PvP/subpack files remain in the archive")
        if "pbr" in manifest.get("capabilities", []):
            errors.append("PBR capability is enabled without PBR assets")

        metadata = manifest.get("metadata", {})
        authors = " ".join(metadata.get("authors", []))
        if "XiaoCraft" not in authors:
            errors.append("Original author XiaoCraft is missing from metadata")
        if "CC BY-NC 3.0" not in str(metadata.get("license", "")):
            errors.append("Original CC BY-NC 3.0 license is missing from metadata")

        ids = [header.get("uuid")] + [module.get("uuid") for module in modules]
        try:
            for value in ids:
                uuid.UUID(str(value))
        except (ValueError, TypeError, AttributeError):
            errors.append("Manifest contains a missing or invalid UUID")
        if len(ids) != len(set(ids)):
            errors.append("Manifest header/module UUIDs are not unique")

        # No experimental settings-query Molang should be required by this pack.
        setting_query_files = []
        for name in names:
            if PurePosixPath(name).suffix.lower() in {".json", ".lang", ".ui", ".material"}:
                content = archive.read(name).decode("utf-8-sig", errors="replace")
                if "query.get_pack_setting" in content or "query.is_pack_setting_enabled" in content:
                    setting_query_files.append(name)
                if "bfps:" in content or "xiao:fog_" in content:
                    errors.append(f"Old internal namespace remains in {name}")
        if setting_query_files:
            errors.append(f"Experimental pack-setting queries remain: {setting_query_files[:10]}")

        # Hard-zero particle emitters that are actually bundled with the pack.
        particle_names = [n for n in parsed if n.startswith("particles/") and n.endswith(".json")]
        particle_stats = {"definition_files": len(particle_names), "max_particles_zero": 0, "num_particles_zero": 0}
        nonzero = []
        def check_particle(node, filename):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "max_particles":
                        if value == 0:
                            particle_stats["max_particles_zero"] += 1
                        else:
                            nonzero.append((filename, key, value))
                    elif key == "num_particles":
                        if value == "0" or value == 0:
                            particle_stats["num_particles_zero"] += 1
                        else:
                            nonzero.append((filename, key, value))
                    check_particle(value, filename)
            elif isinstance(node, list):
                for value in node:
                    check_particle(value, filename)
        for name in particle_names:
            check_particle(parsed[name], name)
        if len(particle_names) != 188:
            errors.append(f"Expected 188 pack particle definitions, found {len(particle_names)}")
        if nonzero:
            errors.append(f"Nonzero particle spawn/max fields remain: {nonzero[:10]}")
        report["particle_audit"] = particle_stats

        # Hide only the visual orb. The game still handles XP collection.
        xp_desc = parsed.get("entity/experience_orb.entity.json", {}).get("minecraft:client_entity", {}).get("description", {})
        if xp_desc.get("render_controllers") != [{"controller.render.experience_orb": "0"}]:
            errors.append("XP-orb render controller is not disabled")
        if "scripts" in xp_desc or "animations" in xp_desc:
            errors.append("XP-orb animation/scripts remain unnecessarily active")

        # Biome -> custom fog identifier resolution.
        biome_data = parsed.get("biomes_client.json", {}).get("biomes", {})
        fog_names = [n for n in parsed if n.startswith("fogs/") and n.endswith(".json")]
        fog_ids = {
            parsed[n].get("minecraft:fog_settings", {}).get("description", {}).get("identifier")
            for n in fog_names
        }
        missing_fog = [
            value.get("fog_identifier")
            for value in biome_data.values()
            if isinstance(value, dict)
            and str(value.get("fog_identifier", "")).startswith("lowmine:")
            and value.get("fog_identifier") not in fog_ids
        ]
        if len(biome_data) != 94:
            errors.append(f"Expected 94 biome entries, found {len(biome_data)}")
        if len(fog_names) != 104:
            errors.append(f"Expected 104 fog JSON files, found {len(fog_names)}")
        if missing_fog:
            errors.append(f"Missing custom fog definitions: {missing_fog}")
        report["biomes"] = len(biome_data)
        report["fog_files"] = len(fog_names)
        report["missing_fog_ids"] = missing_fog

        # Validate against the actual Mojang sample file structure, not just JSON syntax.
        registry = parsed.get("ui/_ui_defs.json", {}).get("ui_defs", [])
        for name in REQUIRED_UI:
            if name not in registry or name not in parsed:
                errors.append(f"UI override missing/unregistered: {name}")

        desktop = parsed.get("ui/inventory_screen.json", {})
        for key in ("inventory_screen@crafting.inventory_screen_base", "crafting_screen@crafting.inventory_screen_base"):
            screen = desktop.get(key, {})
            if screen.get("$screen_content") != "crafting.recipe_inventory_screen_content" or screen.get("$screen_bg_content") != "common.screen_background" or screen.get("$screen_background_alpha") != 0.08:
                errors.append(f"Desktop inventory screen override invalid: {key}")

        pocket = parsed.get("ui/inventory_screen_pocket.json", {})
        for key in ("inventory_screen_pocket@crafting_pocket.inventory_screen_pocket_base", "creative_inventory_screen_pocket@crafting_pocket.inventory_screen_pocket_base"):
            screen = pocket.get(key, {})
            if screen.get("$screen_content") != "crafting_pocket.recipe_inventory_screen_content_pocket" or screen.get("$screen_bg_content") != "common.screen_background" or screen.get("$screen_background_alpha") != 0.08:
                errors.append(f"Pocket inventory screen override invalid: {key}")

        chest = parsed.get("ui/chest_screen.json", {})
        for key in ("small_chest_screen@common.inventory_screen_common", "large_chest_screen@common.inventory_screen_common", "ender_chest_screen@common.inventory_screen_common", "shulker_box_screen@chest.small_chest_screen", "barrel_screen@chest.small_chest_screen"):
            variables = chest.get(key, {}).get("variables", [])
            if not variables or variables[0].get("$screen_content") is None or variables[0].get("$screen_bg_content") != "common.screen_background" or variables[0].get("$screen_background_alpha") != 0.08:
                errors.append(f"Chest/container screen override invalid: {key}")
            if len(variables) < 2 or variables[1].get("requires") != "$pocket_screen":
                errors.append(f"Pocket/container branch missing: {key}")

        data_driven = parsed.get("ui/data_driven_container_screen.json", {}).get("screen@common.inventory_screen_common", {}).get("variables", [])
        if not data_driven or data_driven[0].get("$screen_content") != "data_driven_container.desktop_panel" or data_driven[0].get("$screen_background_alpha") != 0.08:
            errors.append("Data-driven container UI override invalid")
        report["registered_ui_files"] = [n for n in REQUIRED_UI if n in registry]

        # Texture footprint estimate and translucent UI asset sanity.
        pngs = [n for n in names if n.lower().endswith(".png")]
        png_pixels = 0
        for name in pngs:
            data = archive.read(name)
            if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
                errors.append(f"Invalid PNG header: {name}")
                continue
            width, height = struct.unpack(">II", data[16:24])
            png_pixels += width * height
        report["png_files"] = len(pngs)
        report["png_pixels"] = png_pixels
        report["rgba_texel_estimate_mb"] = round(png_pixels * 4 / 1_000_000, 3)

        for name in ("textures/ui/dialog_background_opaque.png", "textures/ui/dialog_background_opaque_overlap_bottom.png"):
            if name not in unique:
                errors.append(f"Missing translucent dialog texture: {name}")
            else:
                image = Image.open(BytesIO(archive.read(name))).convert("RGBA")
                if image.getchannel("A").getextrema()[1] > 100:
                    errors.append(f"Dialog texture alpha was not reduced enough: {name}")

        for name in ("ATTRIBUTION.txt", "pack_icon.png", "textures/ui/pack_icon.png", "textures/ui/title.png"):
            if name not in unique:
                errors.append(f"Required asset missing: {name}")
        attribution = archive.read("ATTRIBUTION.txt").decode("utf-8", errors="replace") if "ATTRIBUTION.txt" in unique else ""
        if "XiaoCraft" not in attribution or "CC BY-NC 3.0" not in attribution:
            errors.append("Attribution file must retain XiaoCraft and CC BY-NC 3.0")

        report["archive_bytes"] = os.path.getsize(filename)
        report["sha256"] = hashlib.sha256(open(filename, "rb").read()).hexdigest()

    return errors, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", help="Path to a .mcpack file")
    args = parser.parse_args()
    errors, report = validate(args.pack)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if errors:
        print("\nVALIDATION FAILED", file=sys.stderr)
        for item in errors:
            print("- " + item, file=sys.stderr)
        return 1
    print("\nAll static checks passed. Import and in-game behavior still require testing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
