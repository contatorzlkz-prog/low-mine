#!/usr/bin/env python3
"""Validador estático para LowMine Batata 8x v0.6.5."""
from __future__ import annotations
import argparse
import hashlib
import json
import zipfile
from io import BytesIO
from pathlib import Path
from PIL import Image

UI_TEXTURES = (
    "lowmine_transparent", "Black", "background", "background_panel",
    "background_with_border", "background_indent_no_top", "dark_bg",
    "panel_outline", "header_bar", "cell_image", "cell_image_normal",
    "cell_image_invert", "cell_image_red", "cell_image_darkgrey",
    "cell_image_selected", "dialog_background_opaque",
    "screen_background", "slots_bg", "toolbar_background",
    "hotbar_start_cap", "hotbar_end_cap", "player_preview_border",
    "TabTopBack", "TabTopFront", "TabLeftBack", "TabLeftFront",
    "TabRightBack", "TabRightFront",
)
FLOWERS = (
    "double_plant_syringa_top", "double_plant_syringa_bottom",
    "double_plant_grass_top", "double_plant_grass_bottom",
    "double_plant_fern_top", "double_plant_fern_bottom",
    "double_plant_rose_top", "double_plant_rose_bottom",
    "double_plant_paeonia_top", "double_plant_paeonia_bottom",
    "double_plant_sunflower_top", "double_plant_sunflower_bottom",
)

def validate(path: Path) -> dict:
    with zipfile.ZipFile(path, "r") as pack:
        if pack.testzip() is not None:
            raise ValueError("CRC inválido no pacote.")
        names_list = pack.namelist()
        names = set(names_list)
        if len(names) != len(names_list):
            raise ValueError("Caminhos duplicados no ZIP.")
        manifest = json.loads(pack.read("manifest.json").decode("utf-8-sig"))
        if manifest.get("format_version") != 2:
            raise ValueError("Manifesto não está no formato estável 2.")
        if manifest["header"].get("version") != [0, 6, 5]:
            raise ValueError("Versão do manifesto inválida.")
        if any(m.get("version") != [0, 6, 5] for m in manifest.get("modules", [])):
            raise ValueError("Versão de módulo inválida.")
        if "settings" in manifest:
            raise ValueError("Bloco de configurações Preview ainda existe.")

        defs = json.loads(pack.read("ui/_ui_defs.json").decode("utf-8-sig"))
        registered = set(defs.get("ui_defs", []))
        for file in ("ui_common_lowmine.json", "ui_crafting_lowmine.json",
                     "ui_tabs_lowmine.json", "ui_pocket_lowmine.json"):
            path_ui = "ui/" + file
            if path_ui not in names or path_ui not in registered:
                raise ValueError("Override UI ausente ou não registrado: " + path_ui)
            json.loads(pack.read(path_ui).decode("utf-8-sig"))

        for texture in UI_TEXTURES:
            path_texture = "textures/ui/" + texture + ".png"
            if path_texture not in names:
                raise ValueError("Textura de UI ausente: " + path_texture)
            with Image.open(BytesIO(pack.read(path_texture))) as image:
                rgba = image.convert("RGBA")
                if rgba.getchannel("A").getbbox() is not None:
                    raise ValueError("Fundo ou borda ainda não está transparente: " + path_texture)

        blocks = [n for n in names if n.startswith("textures/blocks/") and n.endswith(".png")]
        for name in blocks:
            with Image.open(BytesIO(pack.read(name))) as image:
                if image.size != (8, 8):
                    raise ValueError("Textura de bloco fora de 8x8: " + name)
        for stem in FLOWERS:
            name = "textures/blocks/" + stem + ".png"
            if name not in names:
                raise ValueError("Sprite de planta ausente: " + name)
            with Image.open(BytesIO(pack.read(name))) as image:
                if image.size != (8, 8) or image.mode not in ("RGBA", "LA"):
                    raise ValueError("Sprite de planta inválido: " + name)

        armor_count = 0
        for material in ("leather", "chain", "iron", "gold", "diamond", "netherite", "copper"):
            for layer in (1, 2):
                name = f"textures/models/armor/{material}_{layer}.png"
                with Image.open(BytesIO(pack.read(name))) as image:
                    if image.size != (64, 32):
                        raise ValueError("Mapa UV de armadura não está em 64x32: " + name)
                armor_count += 1

        particles = [n for n in names if n.startswith("particles/") and n.endswith(".json")]
        for name in particles:
            data = json.loads(pack.read(name).decode("utf-8-sig"))
            components = data.get("particle_effect", {}).get("components", {})
            if components.get("minecraft:emitter_rate_manual", {}).get("max_particles") != 0:
                raise ValueError("Emissor pode gerar partículas: " + name)
            if components.get("minecraft:emitter_lifetime_expression", {}).get("activation_expression") != 0:
                raise ValueError("Emissor não está desativado: " + name)

        return {
            "arquivo": str(path),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "manifesto": manifest["header"]["version"],
            "texturas_de_bloco_8x8": len(blocks),
            "plantas_8x8": len(FLOWERS),
            "mapas_de_armadura_64x32": armor_count,
            "texturas_de_UI_com_alfa_zero": len(UI_TEXTURES),
            "arquivos_de_UI_registrados": 4,
            "emissores_desativados": len(particles),
        }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pacote", type=Path)
    args = parser.parse_args()
    report = validate(args.pacote)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("Validação estrutural aprovada. Confirme o visual e FPS no Minecraft.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
