#!/usr/bin/env python3
"""Validação estática do LowMine Equilibrado 8x v0.6.2."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from io import BytesIO
from PIL import Image

UI_FILES = (
    "ui/_ui_defs.json",
    "ui/inventory_screen.json",
    "ui/inventory_screen_pocket.json",
    "ui/chest_screen.json",
)
CONTAINERS = (
    "small_chest_screen@common.inventory_screen_common",
    "large_chest_screen@common.inventory_screen_common",
    "ender_chest_screen@common.inventory_screen_common",
    "shulker_box_screen@chest.small_chest_screen",
    "barrel_screen@chest.small_chest_screen",
)
MATERIALS = ("leather", "chain", "iron", "gold", "diamond", "netherite", "copper")
ITEM_MATERIALS = {
    "leather": "leather", "chain": "chainmail", "iron": "iron",
    "gold": "gold", "diamond": "diamond", "netherite": "netherite", "copper": "copper",
}
PIECES = ("helmet", "chestplate", "leggings", "boots")

def validate(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    failures = []
    with zipfile.ZipFile(path, "r") as pack:
        if pack.testzip() is not None:
            failures.append("CRC do arquivo ZIP inválido")
        listed = pack.namelist()
        names = set(listed)
        if len(names) != len(listed):
            failures.append("Há caminhos duplicados no pacote")
        if "manifest.json" not in names:
            failures.append("manifest.json ausente")
            manifest = {}
        else:
            manifest = json.loads(pack.read("manifest.json").decode("utf-8-sig"))
        header = manifest.get("header", {})
        if header.get("version") != "0.6.2":
            failures.append("Versão do cabeçalho não é 0.6.2")
        if any(module.get("version") != "0.6.2" for module in manifest.get("modules", [])):
            failures.append("Versão de um módulo não é 0.6.2")

        for ui_path in UI_FILES:
            if ui_path not in names:
                failures.append(f"Tela de interface ausente: {ui_path}")
        if "ui/chest_screen.json" in names:
            chest = json.loads(pack.read("ui/chest_screen.json").decode("utf-8-sig"))
            for container in CONTAINERS:
                if container not in chest:
                    failures.append(f"Contêiner sem override: {container}")

        block_pngs = [
            name for name in names
            if name.startswith("textures/blocks/") and name.lower().endswith(".png")
        ]
        bad_blocks = []
        for name in block_pngs:
            with Image.open(BytesIO(pack.read(name))) as image:
                if image.size != (8, 8):
                    bad_blocks.append(f"{name}: {image.size}")
        if bad_blocks:
            failures.append("Texturas de bloco fora de 8x8: " + ", ".join(bad_blocks[:8]))
        log_pngs = [
            name for name in block_pngs
            if Path(name).stem.lower().startswith(("log_", "stripped_"))
            or "_log" in Path(name).stem.lower()
        ]
        if not log_pngs:
            failures.append("Nenhuma textura de tronco encontrada")

        armor_maps = []
        armor_icons = []
        for material in MATERIALS:
            for layer in (1, 2):
                name = f"textures/models/armor/{material}_{layer}.png"
                armor_maps.append(name)
                if name not in names:
                    failures.append(f"Mapa de armadura ausente: {name}")
                else:
                    with Image.open(BytesIO(pack.read(name))) as image:
                        if image.size != (64, 32):
                            failures.append(f"Mapa UV deve ser 64x32: {name}")
            icon_material = ITEM_MATERIALS[material]
            for piece in PIECES:
                name = f"textures/items/{icon_material}_{piece}.png"
                armor_icons.append(name)
                if name not in names:
                    failures.append(f"Ícone de armadura ausente: {name}")
                else:
                    with Image.open(BytesIO(pack.read(name))) as image:
                        if image.size != (16, 16):
                            failures.append(f"Ícone de armadura deve ser 16x16: {name}")

        weapon_names = (
            "wood_sword", "stone_sword", "iron_sword", "gold_sword",
            "diamond_sword", "netherite_sword", "copper_sword",
            "bow_standby", "bow_pulling_0", "bow_pulling_1", "bow_pulling_2",
            "crossbow_standby", "crossbow_pulling_0", "crossbow_pulling_1",
            "crossbow_pulling_2", "crossbow_arrow", "crossbow_firework",
            "arrow", "trident",
        )
        weapon_icons = []
        for texture_name in weapon_names:
            name = f"textures/items/{texture_name}.png"
            weapon_icons.append(name)
            if name not in names:
                failures.append(f"Textura de item ausente: {name}")
            else:
                with Image.open(BytesIO(pack.read(name))) as image:
                    if image.size != (16, 16):
                        failures.append(f"Textura de item deve ser 16x16: {name}")

        scripts = [
            name for name in names
            if name.lower().endswith((".js", ".ts", ".mcfunction"))
        ]
        if scripts:
            failures.append("Scripts inesperados no Resource Pack")

        report = {
            "arquivo": str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "entradas": len(names),
            "texturas_de_bloco_8x8": len(block_pngs) - len(bad_blocks),
            "troncos": len(log_pngs),
            "mapas_de_armadura_64x32": len(armor_maps),
            "icones_de_armadura_16x16": len(armor_icons),
            "icones_de_itens_pvp_16x16": len(weapon_icons),
            "telas_ui_preservadas": len(UI_FILES),
            "tipos_de_conteineres": len(CONTAINERS),
            "scripts": len(scripts),
        }
    if failures:
        raise ValueError("\n".join(failures))
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pacote", type=Path)
    args = parser.parse_args()
    result = validate(args.pacote)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("Validação estática aprovada; aparência e FPS ainda precisam de teste no Bedrock.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
