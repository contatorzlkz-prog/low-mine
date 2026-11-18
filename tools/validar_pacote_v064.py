#!/usr/bin/env python3
"""Validação do LowMine Equilibrado 8x v0.6.4 para Bedrock estável."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from io import BytesIO
from pathlib import Path
from PIL import Image

UI_SURFACES = (
    "textures/ui/screen_background.png",
    "textures/ui/dialog_background_opaque.png",
    "textures/ui/dialog_background_opaque_overlap_bottom.png",
    "textures/ui/slots_bg.png",
    "textures/ui/toolbar_background.png",
    "textures/ui/hotbar_start_cap.png",
    "textures/ui/hotbar_end_cap.png",
)
UI_JSON = (
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

def check_alpha(data, path):
    with Image.open(BytesIO(data)) as image:
        if image.convert("RGBA").getchannel("A").getbbox() is not None:
            raise ValueError(f"Fundo/borda ainda não está 100% transparente: {path}")

def check_screen_alpha(value, path="$"):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$screen_background_alpha":
                found.append(child)
                if child != 0 and child != 0.0:
                    raise ValueError(f"{path}.{key} deveria ser 0, recebeu {child!r}")
            else:
                found.extend(check_screen_alpha(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            found.extend(check_screen_alpha(child, f"{path}[{i}]"))
    return found

def validate(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    with zipfile.ZipFile(path, "r") as pack:
        bad = pack.testzip()
        if bad is not None:
            raise ValueError(f"CRC inválido: {bad}")
        listed = pack.namelist()
        names = set(listed)
        if len(names) != len(listed):
            raise ValueError("O pacote contém caminhos duplicados.")
        if "manifest.json" not in names:
            raise ValueError("manifest.json ausente na raiz.")
        manifest = json.loads(pack.read("manifest.json").decode("utf-8-sig"))
        if manifest.get("format_version") != 2:
            raise ValueError("O manifesto não está no formato estável 2.")
        header = manifest.get("header", {})
        if header.get("version") != [0, 6, 4]:
            raise ValueError("A versão do cabeçalho deveria ser [0, 6, 4].")
        if header.get("min_engine_version") != [1, 26, 40]:
            raise ValueError("min_engine_version deveria ser [1, 26, 40].")
        modules = manifest.get("modules", [])
        if not modules or any(m.get("version") != [0, 6, 4] for m in modules):
            raise ValueError("Uma ou mais versões de módulo estão incorretas.")
        if "settings" in manifest:
            raise ValueError("O manifesto ainda contém settings do formato 3 Preview.")

        for ui_path in UI_JSON:
            if ui_path not in names:
                raise ValueError(f"Arquivo de UI ausente: {ui_path}")
            data = json.loads(pack.read(ui_path).decode("utf-8-sig"))
            if ui_path != "ui/_ui_defs.json":
                check_screen_alpha(data, ui_path)

        defs = json.loads(pack.read("ui/_ui_defs.json").decode("utf-8-sig"))
        registered = set(defs.get("ui_defs", []))
        for ui_path in UI_JSON[1:]:
            if ui_path not in registered:
                raise ValueError(f"Arquivo de UI não registrado em _ui_defs.json: {ui_path}")

        chest = json.loads(pack.read("ui/chest_screen.json").decode("utf-8-sig"))
        for container in CONTAINERS:
            if container not in chest:
                raise ValueError(f"Override de contêiner ausente: {container}")

        for ui_surface in UI_SURFACES:
            if ui_surface not in names:
                raise ValueError(f"Textura de UI ausente: {ui_surface}")
            check_alpha(pack.read(ui_surface), ui_surface)

        block_pngs = [name for name in names
                      if name.startswith("textures/blocks/") and name.lower().endswith(".png")]
        for name in block_pngs:
            with Image.open(BytesIO(pack.read(name))) as image:
                if image.size != (8, 8):
                    raise ValueError(f"Textura de bloco fora de 8x8: {name} ({image.size})")

        armor = []
        for material in ("leather", "chain", "iron", "gold", "diamond", "netherite", "copper"):
            for layer in (1, 2):
                name = f"textures/models/armor/{material}_{layer}.png"
                if name not in names:
                    raise ValueError(f"Mapa de armadura ausente: {name}")
                with Image.open(BytesIO(pack.read(name))) as image:
                    if image.size != (64, 32):
                        raise ValueError(f"Mapa UV fora de 64x32: {name}")
                armor.append(name)

        scripts = [name for name in names
                   if name.lower().endswith((".js", ".ts", ".mcfunction"))]
        if scripts:
            raise ValueError("O Resource Pack contém scripts executáveis.")

        return {
            "arquivo": str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "manifest_format": manifest["format_version"],
            "manifest_version": header["version"],
            "engine_min": header["min_engine_version"],
            "textures_8x8": len(block_pngs),
            "armor_maps_64x32": len(armor),
            "transparent_ui_surfaces": len(UI_SURFACES),
            "valid_ui_json": len(UI_JSON),
            "container_overrides": len(CONTAINERS),
            "scripts": len(scripts),
        }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pacote", type=Path)
    args = parser.parse_args()
    report = validate(args.pacote)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Validação estrutural aprovada; a importação final deve ser confirmada no Bedrock.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
