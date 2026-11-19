#!/usr/bin/env python3
"""Gera o perfil LOW BATATA 0.6.5 com UI sem fundos e recursos visuais mínimos."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.4.mcpack"
OUTPUT = ROOT / "build" / "LowMine-Batata-8x-v0.6.5.mcpack"

PALETTES = {
    "grass": ("254C27", "3B7138"),
    "dirt": ("573B28", "765238"),
    "stone": ("535A5D", "7B8485"),
    "cobble": ("454B4F", "777E7F"),
    "gravel": ("625F57", "898579"),
    "sand": ("A89068", "C7B284"),
    "planks": ("543923", "8A603A"),
    "oak": ("3C2518", "795032"),
    "spruce": ("202A24", "54634E"),
    "birch": ("877454", "D0BF98"),
    "jungle": ("3A2B20", "795638"),
    "acacia": ("4A2D23", "925D42"),
    "dark_oak": ("2B1C15", "61402A"),
    "mangrove": ("392124", "80423E"),
    "cherry": ("463343", "906680"),
    "pale_oak": ("5C5345", "A69679"),
    "stripped": ("684A31", "B68B5D"),
}

PATTERNS = {
    "grass": (
        "00000000", "00011000", "00011000", "00000000",
        "00110000", "00110000", "00000000", "00000000",
    ),
    "dirt": (
        "00000000", "00000000", "00110000", "00110000",
        "00000000", "00001100", "00001100", "00000000",
    ),
    "stone": (
        "00000000", "00000000", "00011000", "00011000",
        "00000000", "00110000", "00110000", "00000000",
    ),
    "cobble": (
        "00110011", "00110011", "11001100", "11001100",
        "00110011", "00110011", "11001100", "11001100",
    ),
    "gravel": (
        "00000000", "00010000", "00010000", "00000000",
        "00100000", "00110000", "00000000", "00001000",
    ),
    "sand": (
        "00000000", "00000000", "00011000", "00011000",
        "00000000", "00110000", "00110000", "00000000",
    ),
    "planks": (
        "00000000", "11111111", "11111111", "00000000",
        "11111111", "11111111", "00000000", "11111111",
    ),
}
BARK = {
    "oak": (
        "00100000", "00110000", "00010000", "10010000",
        "10000010", "00000110", "00000010", "00000010",
    ),
    "spruce": (
        "00010000", "00110000", "00100000", "00010000",
        "00011000", "00001000", "00000100", "00001100",
    ),
    "birch": (
        "00010000", "00000000", "00100000", "00000000",
        "00001000", "00000000", "00100000", "00000000",
    ),
    "jungle": (
        "00010000", "00110000", "00010000", "00001000",
        "00011000", "00001000", "00100000", "00110000",
    ),
    "acacia": (
        "00010000", "00110000", "00010000", "00001000",
        "00011000", "00001000", "00000100", "00001100",
    ),
    "dark_oak": (
        "00110000", "00010000", "00011000", "10001000",
        "00001000", "00110000", "00100000", "00011000",
    ),
    "mangrove": (
        "00010000", "00110000", "00010000", "00001000",
        "00011000", "00001000", "00100000", "00110000",
    ),
    "cherry": (
        "00100000", "00110000", "00010000", "00001000",
        "00011000", "00001000", "00100000", "00110000",
    ),
    "pale_oak": (
        "00010000", "00110000", "00010000", "00001000",
        "00011000", "00001000", "00100000", "00110000",
    ),
}

ARMOR = {
    "leather": ("4A2F1E", "95653A"),
    "chain": ("414C51", "AAB7BA"),
    "iron": ("404B56", "B8C3CA"),
    "gold": ("6A4A10", "D9AD42"),
    "diamond": ("164F56", "5DC0B8"),
    "netherite": ("282530", "665B6A"),
    "copper": ("573222", "B66A42"),
}
ITEM_ARMOR = {
    "leather": "leather", "chain": "chainmail", "iron": "iron",
    "gold": "gold", "diamond": "diamond", "netherite": "netherite",
    "copper": "copper",
}
PIECES = ("helmet", "chestplate", "leggings", "boots")
MASKS = {
    "helmet": (
        "........", "..####..", ".######.", ".##..##.",
        ".######.", "..####..", "........", "........",
    ),
    "chestplate": (
        "........", ".##..##.", ".######.", ".######.",
        ".######.", "..####..", "..####..", "........",
    ),
    "leggings": (
        "........", "..####..", ".######.", ".##..##.",
        "..##.##.", "..##.##.", "..#..#..", "........",
    ),
    "boots": (
        "........", ".##..##.", ".##..##.", ".######.",
        ".##..##.", ".##..##.", "........", "........",
    ),
}
FLOWERS = {
    "double_plant_syringa_top": (
        "........", "...pp...", "..pPpp..", "...pp...",
        "....g...", "...g....", "...g....", "...g....",
    ),
    "double_plant_syringa_bottom": (
        "........", "........", "...g....", "...g....",
        "..ggg...", "...g....", "...g....", "...g....",
    ),
    "double_plant_grass_top": (
        "........", "....g...", "...gg...", "......g.",
        ".....gg.", "..g.....", ".gg.....", "........",
    ),
    "double_plant_grass_bottom": (
        "........", "........", "........", "...g....",
        "...g....", "..gg....", "...g....", "...g....",
    ),
    "double_plant_fern_top": (
        "........", "..gg....", ".gg.....", "...gg...",
        "....g...", "..gg....", "...g....", "........",
    ),
    "double_plant_fern_bottom": (
        "........", "........", "...g....", "..gg....",
        "...g....", ".gg.....", "..g.....", "...g....",
    ),
    "double_plant_rose_top": (
        "........", "...rr...", "..rRr...", "...r....",
        "....g...", "...g....", "...g....", "........",
    ),
    "double_plant_rose_bottom": (
        "........", "........", "...g....", "...g....",
        "..gg....", "...g....", "...g....", "........",
    ),
    "double_plant_paeonia_top": (
        "........", "..ppp...", ".pPpPp..", "..ppp...",
        "...g....", "...g....", "...g....", "........",
    ),
    "double_plant_paeonia_bottom": (
        "........", "........", "...g....", "..gg....",
        "...g....", "....g...", "...g....", "........",
    ),
    "double_plant_sunflower_top": (
        "........", "...yy...", "..yYy...", "...yy...",
        "...g....", "...g....", "...g....", "........",
    ),
    "double_plant_sunflower_bottom": (
        "........", "........", "...g....", "...g....",
        "..gg....", "...g....", "...g....", "........",
    ),
}
FLOWER_COLORS = {
    "g": (37, 91, 39, 255),
    "p": (113, 66, 119, 255),
    "P": (151, 91, 153, 255),
    "r": (112, 49, 48, 255),
    "R": (161, 67, 62, 255),
    "y": (160, 130, 43, 255),
    "Y": (211, 177, 65, 255),
}
UI_TEXTURES = (
    "Black", "background", "background_panel", "background_with_border",
    "background_indent_no_top", "dark_bg", "panel_outline", "header_bar",
    "header_bar_2", "cell_image", "cell_image_normal", "cell_image_invert",
    "cell_image_red", "cell_image_darkgrey", "cell_image_selected",
    "dialog_background_opaque", "dialog_background_opaque_overlap_bottom",
    "dialog_background_hollow_1", "dialog_background_hollow_2",
    "dialog_background_hollow_3", "dialog_background_hollow_4",
    "dialog_background_hollow_4_thin", "dialog_background_hollow_5",
    "dialog_background_hollow_6", "dialog_background_hollow_7",
    "dialog_background_hollow_8", "screen_background", "slots_bg",
    "toolbar_background", "hotbar_start_cap", "hotbar_end_cap",
    "player_preview_border", "highlight_slot", "focus_border_white",
    "TabTopBack", "TabTopBackHover", "TabTopBackLeftMost",
    "TabTopBackLeftMostHover", "TabTopBackRightMost", "TabTopBackRightMostHover",
    "TabTopBackRightMostDark", "TabTopBackRightMostDarkHover",
    "TabTopFront", "TabTopFrontHover", "TabTopFrontLeftMost",
    "TabTopFrontLeftMostHover", "TabTopFrontRightMost",
    "TabTopFrontRightMostHover", "TabLeftBack", "TabLeftBackHover",
    "TabLeftBackBottomMost", "TabLeftBackBottomMostHover",
    "TabLeftBackTopMost", "TabLeftBackTopMostHover",
    "TabLeftFront", "TabLeftFrontHover", "TabLeftFrontBottomMost",
    "TabLeftFrontBottomMostHover", "TabLeftFrontTopMost",
    "TabLeftFrontTopMostHover", "TabRightBack", "TabRightBackHover",
    "TabRightBackBottomMost", "TabRightBackBottomMostHover",
    "TabRightBackTopMost", "TabRightBackTopMostHover",
    "TabRightFront", "TabRightFrontHover", "TabRightFrontBottomMost",
    "TabRightFrontBottomMostHover", "TabRightFrontTopMost",
    "TabRightFrontTopMostHover", "XTab",
    "hotbar_0", "hotbar_1", "hotbar_2", "hotbar_3", "hotbar_4",
    "hotbar_5", "hotbar_6", "hotbar_7", "hotbar_8",
)

def rgb(hex_color: str) -> tuple[int, int, int]:
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def png(image: Image.Image) -> bytes:
    out = io.BytesIO()
    image.save(out, format="PNG", optimize=True)
    return out.getvalue()

def patterned(rows: tuple[str, ...], palette: tuple[str, str]) -> Image.Image:
    colors = [rgb(palette[0]) + (255,), rgb(palette[1]) + (255,)]
    image = Image.new("RGBA", (8, 8), colors[0])
    px = image.load()
    for y, row in enumerate(rows):
        for x, value in enumerate(row):
            px[x, y] = colors[int(value)]
    return image

def species(name: str) -> str:
    for key in ("birch", "spruce", "jungle", "acacia", "dark_oak",
                "mangrove", "cherry", "pale_oak"):
        if key in name:
            return key
    return "oak"

def wood_texture(name: str, top: bool) -> Image.Image:
    kind = "stripped" if "stripped" in name else species(name)
    palette = PALETTES[kind]
    if not top:
        return patterned(BARK[kind], (palette[1], palette[0]))
    image = Image.new("RGBA", (8, 8), rgb(palette[0]) + (255,))
    px = image.load()
    for y in range(8):
        for x in range(8):
            if 2 <= x <= 5 and 2 <= y <= 5:
                px[x, y] = rgb(palette[1]) + (255,)
    return image

def flower_texture(rows: tuple[str, ...]) -> Image.Image:
    image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    px = image.load()
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char in FLOWER_COLORS:
                px[x, y] = FLOWER_COLORS[char]
    return image

def apply_world_textures(files: dict[str, bytes]) -> int:
    changed = 0
    for path in list(files):
        if not path.startswith("textures/blocks/") or not path.lower().endswith(".png"):
            continue
        stem = Path(path).stem.lower()
        image = None
        if "log" in stem or stem.startswith("stripped_"):
            image = wood_texture(stem, stem.endswith("_top"))
        elif stem in ("grass_top", "grass_block_top", "grass_top_carried"):
            image = patterned(PATTERNS["grass"], PALETTES["grass"])
        elif stem in ("grass_side", "grass_block_side"):
            image = Image.new("RGBA", (8, 8), rgb(PALETTES["dirt"][0]) + (255,))
            px = image.load()
            for y in range(2):
                for x in range(8):
                    px[x, y] = rgb(PALETTES["grass"][0 if x in (0, 7) else 1]) + (255,)
            for x in (2, 3, 6):
                px[x, 2] = rgb(PALETTES["grass"][0]) + (255,)
        elif "cobble" in stem or "cobblestone" in stem:
            image = patterned(PATTERNS["cobble"], PALETTES["cobble"])
        elif "gravel" in stem:
            image = patterned(PATTERNS["gravel"], PALETTES["gravel"])
        elif "sand" in stem:
            image = patterned(PATTERNS["sand"], PALETTES["sand"])
        elif "planks" in stem:
            image = patterned(PATTERNS["planks"], PALETTES["planks"])
        elif "stone" in stem or stem in ("andesite", "granite", "diorite"):
            image = patterned(PATTERNS["stone"], PALETTES["stone"])
        elif "dirt" in stem or "podzol" in stem or "mycelium" in stem:
            image = patterned(PATTERNS["dirt"], PALETTES["dirt"])
        elif "leaves" in stem:
            with Image.open(io.BytesIO(files[path])) as original:
                alpha = original.convert("RGBA").getchannel("A")
            image = patterned(
                ("00000000", "00011000", "00011000", "00000000",
                 "00110000", "00110000", "00000000", "00000000"),
                ("194A24", "2D642F"),
            )
            image.putalpha(alpha)
        elif "fern" in stem or "tall_grass" in stem or stem.endswith("_plant"):
            rows = (
                "........", "........", "...1....", "..11....",
                "...1....", ".1.1....", "..1.....", "...1....",
            )
            image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
            px = image.load()
            for y, row in enumerate(rows):
                for x, char in enumerate(row):
                    if char == "1":
                        px[x, y] = (42, 102, 45, 255)
        if image is not None:
            files[path] = png(image)
            changed += 1

    for stem, rows in FLOWERS.items():
        files["textures/blocks/" + stem + ".png"] = png(flower_texture(rows))
    return changed

def draw_face(image: Image.Image, rect, dark, light, style: str) -> None:
    x0, y0, width, height = rect
    for y in range(height):
        for x in range(width):
            edge = x == 0 or y == 0 or x == width - 1 or y == height - 1
            color = dark if edge else light
            if style == "leather" and y == height // 2:
                color = dark
            if style == "chain" and x in (1, width - 2) and y in (1, height - 2):
                color = dark
            if style == "plate" and height > 6 and y == height // 2:
                color = dark
            image.putpixel((x0 + x, y0 + y), color + (255,))

def armor_box(image, u, v, width, height, depth, dark, light, style) -> None:
    faces = (
        (u + depth, v, width, depth),
        (u + depth + width, v, width, depth),
        (u, v + depth, depth, height),
        (u + depth, v + depth, width, height),
        (u + depth + width + depth, v + depth, width, height),
        (u + depth + width, v + depth, depth, height),
    )
    for rect in faces:
        draw_face(image, rect, dark, light, style)

def armor_map(material: str, layer: int) -> Image.Image:
    dark = rgb(ARMOR[material][0])
    light = rgb(ARMOR[material][1])
    style = "leather" if material == "leather" else "chain" if material == "chain" else "plate"
    image = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    if layer == 1:
        armor_box(image, 0, 0, 8, 8, 8, dark, light, style)
        armor_box(image, 32, 0, 8, 8, 8, dark, light, style)
        armor_box(image, 16, 16, 8, 12, 4, dark, light, style)
        armor_box(image, 40, 16, 4, 12, 4, dark, light, style)
        armor_box(image, 0, 16, 4, 12, 4, dark, light, style)
    else:
        armor_box(image, 16, 16, 8, 12, 4, dark, light, style)
        armor_box(image, 0, 16, 4, 12, 4, dark, light, style)
    return image

def armor_icon(material: str, piece: str) -> Image.Image:
    dark, light = map(rgb, ARMOR[material])
    mask = MASKS[piece]
    image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    px = image.load()
    for y, row in enumerate(mask):
        for x, char in enumerate(row):
            if char == "#":
                edge = any(
                    nx < 0 or ny < 0 or nx >= 8 or ny >= 8 or mask[ny][nx] == "."
                    for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))
                )
                px[x, y] = (dark if edge else light) + (255,)
    return image.resize((16, 16), Image.Resampling.NEAREST)

def apply_armors(files: dict[str, bytes]) -> int:
    count = 0
    for material in ARMOR:
        for layer in (1, 2):
            files[f"textures/models/armor/{material}_{layer}.png"] = png(armor_map(material, layer))
            count += 1
        for piece in PIECES:
            name = ITEM_ARMOR[material]
            files[f"textures/items/{name}_{piece}.png"] = png(armor_icon(material, piece))
            count += 1
    return count

def transparent_png() -> bytes:
    return png(Image.new("RGBA", (8, 8), (0, 0, 0, 0)))

def disable_particle_file(path: str, original: bytes | None = None) -> bytes:
    version = "1.10.0"
    identifier = "minecraft:" + Path(path).stem
    basic = {"material": "particles_alpha", "texture": "textures/particle/particles"}
    if original:
        data = json.loads(original.decode("utf-8-sig"))
        version = data.get("format_version", version)
        desc = data.get("particle_effect", {}).get("description", {})
        identifier = desc.get("identifier", identifier)
        basic = desc.get("basic_render_parameters", basic)
    disabled = {
        "format_version": version,
        "particle_effect": {
            "description": {
                "identifier": identifier,
                "basic_render_parameters": basic,
            },
            "components": {
                "minecraft:emitter_lifetime_expression": {
                    "activation_expression": 0,
                    "expiration_expression": 1,
                },
                "minecraft:emitter_rate_manual": {"max_particles": 0},
            },
        },
    }
    return (json.dumps(disabled, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def disable_particles(files: dict[str, bytes]) -> int:
    paths = [
        path for path in files
        if path.startswith("particles/") and path.lower().endswith(".json")
    ]
    for path in paths:
        files[path] = disable_particle_file(path, files[path])
    for path in ("particles/block_destruct.json", "particles/block_slide.json"):
        if path not in files:
            files[path] = disable_particle_file(path)
            paths.append(path)
    return len(paths)

def common_ui() -> dict:
    blank = "textures/ui/lowmine_transparent"
    return {
        "namespace": "common",
        "screen_background": {
            "type": "image", "texture": blank, "layer": -10,
            "$screen_background_alpha|default": 0.0, "alpha": 0.0,
        },
        "dialog_background_common": {
            "type": "image", "texture": blank, "layer": 1, "alpha": 0.0,
        },
        "dialog_background_hollow_common@dialog_background_common": {
            "layer": 2, "$fill_alpha|default": 0.0,
            "$dialog_background_texture|default": blank,
            "controls": [{"control": {
                "type": "image", "texture": blank, "layer": -1,
                "size": ["100% - 8px", "100% - 8px"], "alpha": 0.0,
            }}],
        },
        "dialog_background_opaque@dialog_background_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_1@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_2@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_3@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_4@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_4_thin@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_5@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_6@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_7@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "dialog_background_hollow_8@dialog_background_hollow_common": {"texture": blank, "alpha": 0.0},
        "cell_image": {"type": "image", "texture": blank, "layer": 1, "alpha": 0.0},
        "cell_image_selected": {"type": "image", "texture": blank, "layer": 1, "alpha": 0.0},
        "highlight_slot": {"type": "image", "texture": blank, "alpha": 0.0},
        "white_border_slot": {"type": "image", "texture": blank, "alpha": 0.0},
        "container_item": {"$background_images": "common.empty_panel"},
    }

def crafting_ui() -> dict:
    blank = "textures/ui/lowmine_transparent"
    return {
        "namespace": "crafting",
        "container_cell_images": {"type": "panel", "controls": []},
        "crafting_container_cell_images@crafting.container_cell_images": {"controls": []},
        "recipe_container_cell_images@crafting.container_cell_images": {"controls": []},
        "cell_image": {"type": "image", "texture": blank, "alpha": 0.0},
        "cell_image_classic@crafting.cell_image": {"texture": blank, "alpha": 0.0},
        "cell_image_normal@crafting.cell_image": {"texture": blank, "alpha": 0.0},
        "cell_image_invert@crafting.cell_image": {"texture": blank, "alpha": 0.0},
        "cell_image_red@crafting.cell_image": {"texture": blank, "alpha": 0.0},
        "cell_image_selected@crafting.cell_image": {"texture": blank, "alpha": 0.0},
        "cell_image_darkgrey@crafting.cell_image": {"texture": blank, "alpha": 0.0},
        "player_bg": {"type": "image", "texture": blank, "alpha": 0.0},
        "player_preview_border": {"type": "image", "texture": blank, "alpha": 0.0},
    }

def tabs_ui() -> dict:
    return {
        "namespace": "common_tabs",
        "tab_image": {
            "type": "image", "texture": "textures/ui/lowmine_transparent",
            "alpha": 0.0,
        },
    }

def pocket_ui() -> dict:
    blank = "textures/ui/lowmine_transparent"
    return {
        "namespace": "pocket_containers",
        "header_panel": {
            "type": "panel", "layer": 1, "size": ["50%", "27px"],
            "anchor_from": "top_left", "anchor_to": "top_left",
            "controls": [
                {"header_background": {"type": "image", "texture": blank, "alpha": 0.0}},
                {"title_label@generic_label": {
                    "text": "$header_label", "localize": "$localize_title",
                    "enable_profanity_filter": True,
                }},
            ],
        },
        "dark_bg": {"type": "image", "texture": blank, "layer": 3, "alpha": 0.0},
        "panel_outline": {"type": "image", "texture": blank, "alpha": 0.0},
        "background_panel": {
            "type": "image", "size": ["100%", "100%"],
            "texture": blank, "layer": 2, "alpha": 0.0,
        },
    }

def install_ui(files: dict[str, bytes]) -> None:
    files["textures/ui/lowmine_transparent.png"] = transparent_png()
    definitions = {
        "ui_common_lowmine.json": common_ui(),
        "ui_crafting_lowmine.json": crafting_ui(),
        "ui_tabs_lowmine.json": tabs_ui(),
        "ui_pocket_lowmine.json": pocket_ui(),
    }
    for filename, data in definitions.items():
        files["ui/" + filename] = (
            json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")

    defs_path = "ui/_ui_defs.json"
    defs = json.loads(files[defs_path].decode("utf-8-sig"))
    registered = list(defs.get("ui_defs", []))
    for filename in definitions:
        entry = "ui/" + filename
        if entry not in registered:
            registered.append(entry)
    defs["ui_defs"] = registered
    files[defs_path] = (json.dumps(defs, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    for path in ("ui/inventory_screen.json", "ui/inventory_screen_pocket.json", "ui/chest_screen.json"):
        data = json.loads(files[path].decode("utf-8-sig"))
        def zero_alpha(value):
            if isinstance(value, dict):
                for key in list(value):
                    if key == "$screen_background_alpha":
                        value[key] = 0.0
                    else:
                        zero_alpha(value[key])
            elif isinstance(value, list):
                for item in value:
                    zero_alpha(item)
        zero_alpha(data)
        files[path] = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    # Real texture overrides: make all menu panels, slot borders and category tabs invisible.
    blank = transparent_png()
    for name in UI_TEXTURES:
        files["textures/ui/" + name + ".png"] = blank

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=INPUT)
    parser.add_argument("--saida", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if not args.base.is_file():
        raise SystemExit("Pacote base v0.6.4 não encontrado: " + str(args.base))

    with zipfile.ZipFile(args.base, "r") as source:
        bad = source.testzip()
        if bad is not None:
            raise SystemExit("CRC inválido no arquivo-base: " + bad)
        files = {item.filename: source.read(item.filename)
                 for item in source.infolist() if not item.is_dir()}

    manifest = json.loads(files["manifest.json"].decode("utf-8-sig"))
    manifest["format_version"] = 2
    manifest["header"]["version"] = [0, 6, 5]
    manifest["header"]["name"] = "LowMine Batata 8x v0.6.5"
    manifest["header"]["description"] = (
        "LOW BATATA: texturas mínimas, menus transparentes e partículas desativadas."
    )
    for module in manifest.get("modules", []):
        module["version"] = [0, 6, 5]
    manifest.pop("settings", None)
    files["manifest.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    block_count = apply_world_textures(files)
    armor_count = apply_armors(files)
    particle_count = disable_particles(files)
    install_ui(files)

    texture_list_path = "textures/textures_list.json"
    if texture_list_path in files:
        texture_list = json.loads(files[texture_list_path].decode("utf-8-sig"))
        additions = {"textures/ui/lowmine_transparent"}
        additions.update("textures/blocks/" + stem for stem in FLOWERS)
        files[texture_list_path] = (
            json.dumps(sorted(set(texture_list) | additions),
                       ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")

    # Remove PBR helper maps if included; they are not needed by this flat 8x pack.
    pbr = [name for name in list(files)
           if name.lower().endswith(("_mers.tga", "_normal.tga", "_heightmap.tga",
                                     ".texture_set.json"))]
    for name in pbr:
        del files[name]

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.saida, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as target:
        for name in sorted(files):
            target.writestr(name, files[name])

    print(json.dumps({
        "arquivo": str(args.saida),
        "bytes": args.saida.stat().st_size,
        "texturas_de_bloco_alteradas": block_count,
        "plantas_minimalistas_8x8": len(FLOWERS),
        "arquivos_de_armadura": armor_count,
        "arquivos_de_particulas_desativados": particle_count,
        "texturas_de_interface_transparentes": len(UI_TEXTURES) + 1,
        "mapas_PBR_removidos": len(pbr),
        "manifest_format": manifest["format_version"],
        "manifest_version": manifest["header"]["version"],
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
