#!/usr/bin/env python3
"""Build the LowMine v0.2.0 adaptation from the supplied source .mcpack.

Requires Python 3.10+. Uses only the Python standard library. Branding PNGs are
passed in explicitly. This is a static resource-pack transformation; it does
not patch Minecraft or measure FPS.
"""
from __future__ import annotations

import argparse
import json
import shutil
import stat
import tempfile
import uuid
import zipfile
from pathlib import Path, PurePosixPath

VERSION = "0.2.0"
REPOSITORY_URL = "https://github.com/contatorzlkz-prog/low-mine"
SOURCE_URL = "https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance"
LICENSE_URL = "https://creativecommons.org/licenses/by-nc/3.0/"
PROJECT_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_URL, REPOSITORY_URL)

EN = {
    "lowmine.settings.title": "LOWMINE PERFORMANCE  |  v0.2.0",
    "lowmine.settings.intro": "Tune visual effects. These settings work with both LowMine profiles.",
    "lowmine.section.particles": "PARTICLES",
    "lowmine.setting.particle_amount": "Particle amount (%)",
    "lowmine.setting.particle_amount.help": "Scales configurable particle emitters. 50% is the balanced default; 0% disables these effects.",
    "lowmine.setting.potion_effects": "Potion and status effects",
    "lowmine.setting.potion_effects.help": "Keeps the visual particles from potion effects, splash potions and lingering clouds.",
    "lowmine.setting.witch_evoker": "Witch and Evoker effects",
    "lowmine.setting.witch_evoker.help": "Toggles the custom brewing and spell particles.",
    "lowmine.setting.arrow_trails": "Arrow trails",
    "lowmine.setting.arrow_trails.help": "Toggles the custom trail behind tipped arrows.",
    "lowmine.setting.cauldron": "Cauldron effects",
    "lowmine.setting.cauldron.help": "Toggles the custom drips and splashes around filled cauldrons.",
    "lowmine.setting.geysers": "Geyser effects",
    "lowmine.setting.geysers.help": "Toggles custom geyser columns, plumes and puffs.",
    "lowmine.setting.noxious_gas": "Geyser gas",
    "lowmine.setting.noxious_gas.help": "Toggles drifting gas particles around geyser fields.",
    "lowmine.setting.sulfur": "Sulfur particles",
    "lowmine.setting.sulfur.help": "Toggles sulfur bubbles and cubes in sulfur caves.",
    "lowmine.section.entities": "ENTITY RENDERING",
    "lowmine.setting.xp_orbs": "Experience orbs",
    "lowmine.setting.xp_orbs.help": "Hides the orb models only. Experience is still collected.",
    "lowmine.section.profiles": "PROFILES",
    "lowmine.subpacks.help": "Choose LowMine Lite for shorter fog and more particle overrides, or LowMine PvP for a longer view and its extra HUD.",
    "lowmine.credit": "Original work by XiaoCraft; adapted by the LowMine Project. See ATTRIBUTION.txt.",
    "pack.name": "§dLowMine Performance§r",
    "pack.description": "§7Adaptation of Boosted FPS by XiaoCraft.§r",
    "accessibility.chat.howtoemote": "§dLowMine Performance loaded. §7Adapted from XiaoCraft's Boosted FPS.",
}

PT_BR = {
    "lowmine.settings.title": "LOWMINE PERFORMANCE  |  v0.2.0",
    "lowmine.settings.intro": "Ajuste os efeitos visuais. Estas opções funcionam nos dois perfis LowMine.",
    "lowmine.section.particles": "PARTÍCULAS",
    "lowmine.setting.particle_amount": "Quantidade de partículas (%)",
    "lowmine.setting.particle_amount.help": "Ajusta a quantidade dos emissores configuráveis. 50% é o padrão equilibrado; 0% desativa esses efeitos.",
    "lowmine.setting.potion_effects": "Efeitos de poções e status",
    "lowmine.setting.potion_effects.help": "Mantém as partículas visuais de poções, poções arremessáveis e nuvens persistentes.",
    "lowmine.setting.witch_evoker": "Efeitos de bruxas e evocadores",
    "lowmine.setting.witch_evoker.help": "Ativa ou desativa as partículas personalizadas de preparo e feitiços.",
    "lowmine.setting.arrow_trails": "Rastros de flechas",
    "lowmine.setting.arrow_trails.help": "Ativa ou desativa o rastro visual personalizado das flechas com efeito.",
    "lowmine.setting.cauldron": "Efeitos de caldeirões",
    "lowmine.setting.cauldron.help": "Ativa ou desativa gotas e respingos personalizados ao redor de caldeirões cheios.",
    "lowmine.setting.geysers": "Efeitos de gêiseres",
    "lowmine.setting.geysers.help": "Ativa ou desativa colunas, plumas e pequenas nuvens dos gêiseres.",
    "lowmine.setting.noxious_gas": "Gás de gêiseres",
    "lowmine.setting.noxious_gas.help": "Ativa ou desativa partículas de gás nas áreas de gêiseres.",
    "lowmine.setting.sulfur": "Partículas de enxofre",
    "lowmine.setting.sulfur.help": "Ativa ou desativa bolhas e cubos de enxofre nas cavernas de enxofre.",
    "lowmine.section.entities": "RENDERIZAÇÃO DE ENTIDADES",
    "lowmine.setting.xp_orbs": "Orbes de experiência",
    "lowmine.setting.xp_orbs.help": "Oculta apenas o modelo dos orbes. A experiência continua sendo coletada.",
    "lowmine.section.profiles": "PERFIS",
    "lowmine.subpacks.help": "Escolha LowMine Lite para neblina mais curta e mais efeitos removidos, ou LowMine PvP para visão mais distante e HUD adicional.",
    "lowmine.credit": "Trabalho original de XiaoCraft; adaptação do projeto LowMine. Consulte ATTRIBUTION.txt.",
    "pack.name": "§dLowMine Performance§r",
    "pack.description": "§7Adaptação do Boosted FPS de XiaoCraft.§r",
    "accessibility.chat.howtoemote": "§dLowMine Performance carregado. §7Adaptação do Boosted FPS de XiaoCraft.",
}


def stable_uuid(label: str) -> str:
    return str(uuid.uuid5(PROJECT_NAMESPACE, f"{label}:v{VERSION}"))


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_extract(archive: zipfile.ZipFile, destination: Path) -> None:
    seen: set[str] = set()
    for info in archive.infolist():
        name = info.filename
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name:
            raise ValueError(f"Unsafe archive path: {name!r}")
        if name in seen:
            raise ValueError(f"Duplicate archive entry: {name!r}")
        seen.add(name)
        mode = (info.external_attr >> 16) & 0xFFFF
        if stat.S_ISLNK(mode):
            raise ValueError(f"Symlink entry is not allowed: {name!r}")
    archive.extractall(destination)


def update_lang_file(path: Path, values: dict[str, str]) -> None:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    replaced = set(values)
    output: list[str] = []
    for line in lines:
        if "=" in line and not line.lstrip().startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key in replaced:
                continue
        output.append(line)
    if output and output[-1].strip():
        output.append("")
    output.append("## LowMine pack and settings")
    output.extend(f"{key}={value}" for key, value in values.items())
    path.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")


def transform_text_files(root: Path) -> None:
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".lang", ".ui", ".material"}:
            continue
        try:
            before = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        after = before.replace("bfps:", "lowmine:").replace("xiao:fog_", "lowmine:fog_")
        if after != before:
            path.write_text(after, encoding="utf-8")


def update_manifest(root: Path) -> None:
    path = root / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    manifest["format_version"] = 3

    header = manifest["header"]
    header["name"] = f"§l§dLowMine Performance §r§7v{VERSION}"
    header["description"] = (
        "§dLowMine Performance§r\n"
        "§7Bedrock resource-pack adaptation for lower-end devices\n"
        "§7LowMine Lite and LowMine PvP profiles · 9 configurable controls\n"
        "§7Original work by XiaoCraft (CC BY-NC 3.0). See ATTRIBUTION.txt."
    )
    header["version"] = VERSION

    for module in manifest.get("modules", []):
        module["description"] = "LowMine Performance — adapted resource-pack module"
        module["version"] = VERSION

    manifest["subpacks"] = [
        {
            "folder_name": "fps",
            "name": "§bLowMine Lite §7- Performance First",
            "memory_performance_tier": 1,
        },
        {
            "folder_name": "pvp_fps",
            "name": "§dLowMine PvP §7- HUD + Clear View",
            "memory_performance_tier": 2,
        },
    ]

    manifest["settings"] = [
        {"type": "label", "text": "lowmine.settings.title"},
        {"type": "label", "text": "lowmine.settings.intro"},
        {"type": "label", "text": "lowmine.section.particles"},
        {"type": "slider", "text": "lowmine.setting.particle_amount", "name": "lowmine:particle_amount", "min": 0, "max": 100, "step": 10, "default": 50},
        {"type": "label", "text": "lowmine.setting.particle_amount.help"},
        {"type": "toggle", "text": "lowmine.setting.potion_effects", "name": "lowmine:potion_effects", "default": True},
        {"type": "label", "text": "lowmine.setting.potion_effects.help"},
        {"type": "toggle", "text": "lowmine.setting.witch_evoker", "name": "lowmine:witch_evoker", "default": False},
        {"type": "label", "text": "lowmine.setting.witch_evoker.help"},
        {"type": "toggle", "text": "lowmine.setting.arrow_trails", "name": "lowmine:arrow_trails", "default": False},
        {"type": "label", "text": "lowmine.setting.arrow_trails.help"},
        {"type": "toggle", "text": "lowmine.setting.cauldron", "name": "lowmine:cauldron", "default": False},
        {"type": "label", "text": "lowmine.setting.cauldron.help"},
        {"type": "toggle", "text": "lowmine.setting.geysers", "name": "lowmine:geysers", "default": False},
        {"type": "label", "text": "lowmine.setting.geysers.help"},
        {"type": "toggle", "text": "lowmine.setting.noxious_gas", "name": "lowmine:noxious_gas", "default": False},
        {"type": "label", "text": "lowmine.setting.noxious_gas.help"},
        {"type": "toggle", "text": "lowmine.setting.sulfur", "name": "lowmine:sulfur", "default": False},
        {"type": "label", "text": "lowmine.setting.sulfur.help"},
        {"type": "label", "text": "lowmine.section.entities"},
        {"type": "toggle", "text": "lowmine.setting.xp_orbs", "name": "lowmine:xp_orbs", "default": False},
        {"type": "label", "text": "lowmine.setting.xp_orbs.help"},
        {"type": "label", "text": "lowmine.section.profiles"},
        {"type": "label", "text": "lowmine.subpacks.help"},
        {"type": "label", "text": "lowmine.credit"},
    ]
    manifest["metadata"] = {
        "authors": ["XiaoCraft (original author)", "LowMine Project (adaptation)"],
        "license": "CC BY-NC 3.0 (adapted source work; see ATTRIBUTION.txt)",
        "url": REPOSITORY_URL,
        "product_type": "addon",
    }
    write_json(path, manifest)


def build(source: Path, output: Path, icon: Path, title: Path) -> None:
    if not source.is_file() or not zipfile.is_zipfile(source):
        raise ValueError(f"Invalid source .mcpack: {source}")
    if not icon.is_file() or not title.is_file():
        raise FileNotFoundError("Both --icon and --title PNG files are required.")

    with tempfile.TemporaryDirectory(prefix="lowmine-build-") as temp:
        root = Path(temp) / "pack"
        root.mkdir()
        with zipfile.ZipFile(source) as archive:
            bad = archive.testzip()
            if bad:
                raise ValueError(f"Corrupt source archive entry: {bad}")
            safe_extract(archive, root)

        update_manifest(root)
        transform_text_files(root)
        for lang_file in (root / "texts").glob("*.lang"):
            values = dict(EN)
            if lang_file.name == "pt_BR.lang":
                values.update(PT_BR)
            update_lang_file(lang_file, values)

        manifest_path = root / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["header"]["uuid"] = stable_uuid("manifest-header")
        for index, module in enumerate(manifest.get("modules", [])):
            module["uuid"] = stable_uuid(f"manifest-module-{index}")
        write_json(manifest_path, manifest)

        shutil.copyfile(icon, root / "pack_icon.png")
        shutil.copyfile(icon, root / "textures/ui/pack_icon.png")
        pvp_logo = root / "subpacks/pvp_fps/textures/ui/Boosted FPS.png"
        if pvp_logo.exists():
            shutil.copyfile(icon, pvp_logo)
        shutil.copyfile(title, root / "textures/ui/title.png")

        attribution = f"""LowMine Performance v{VERSION} — attribution and license

This package is an adaptation of:
  Boosted FPS (Optimized Performance) v2.4.1
  Original author: XiaoCraft
  Original project: {SOURCE_URL}

Changes made by the LowMine Project in v{VERSION}:
  - Rebranded the pack, profiles, icons, title image and localized settings.
  - Assigned new stable manifest and module UUIDs.
  - Renamed custom setting and custom fog identifiers to the LowMine namespace.
  - Added nine configurable controls with revised default values.
  - Reduced the title image from 4096x604 to 2048x302.
  - Added Brazilian Portuguese settings text and English fallback labels.

This is an adaptation, not an original replacement for the source work. No measured FPS improvement is claimed. Runtime testing is still required.

The original work is listed under the Creative Commons Attribution-NonCommercial 3.0 Unported license (CC BY-NC 3.0):
  {LICENSE_URL}

The original author and project are credited above, and the changes are identified. This adaptation is not endorsed by or affiliated with XiaoCraft.

The license prohibits use primarily intended for commercial advantage or private monetary compensation. Keep the attribution and license information with redistributed copies, and respect the full license terms.
"""
        (root / "ATTRIBUTION.txt").write_text(attribution, encoding="utf-8")

        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w") as archive:
            for path in sorted(p for p in root.rglob("*") if p.is_file()):
                info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (0o100644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    with zipfile.ZipFile(output) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"Built archive integrity failure: {bad}")
        for name in archive.namelist():
            if name.lower().endswith(".json"):
                json.loads(archive.read(name).decode("utf-8-sig"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--icon", type=Path, required=True)
    parser.add_argument("--title", type=Path, required=True)
    args = parser.parse_args()
    build(args.source, args.output, args.icon, args.title)
    print(f"Built {args.output} ({args.output.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
