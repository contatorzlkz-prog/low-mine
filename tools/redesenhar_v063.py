#!/usr/bin/env python3
"""Aplica o refinamento LowMine 0.6.3 a partir do pacote 0.6.2."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.2.mcpack"
DEFAULT_OUTPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.3.mcpack"
DEFAULT_PREVIEW = ROOT / "build" / "LowMine-Preview-v0.6.3.png"

def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

# Quatro tons por madeira: sombra profunda, sombra, base e luz.
WOOD = {
    "oak":       ["2B1B12", "503321", "805638", "B18459"],
    "spruce":    ["171D19", "303B32", "56634D", "859071"],
    "birch":     ["493B2B", "8C7959", "D1C29B", "EEE3C8"],
    "jungle":    ["281D16", "4B3828", "79563A", "A47C52"],
    "acacia":    ["30201A", "59382D", "895842", "BD8460"],
    "dark_oak":  ["1B1410", "35231A", "5B3B27", "896044"],
    "mangrove":  ["24191D", "4B292B", "793E3C", "B36554"],
    "cherry":    ["30232D", "573B4C", "855B71", "B98298"],
    "pale_oak":  ["39342D", "6C6050", "A19178", "D0C0A2"],
}
STRIPPED = ["4C3827", "816044", "B58A5B", "D9B98A"]

# Padrões próprios 8x8. As quebras e marcas curtas evitam faixas verticais contínuas.
BARK = {
    "oak": (
        "22212222", "22122212", "23212222", "22203222",
        "22222122", "12222222", "22232212", "21212222",
    ),
    "spruce": (
        "21222122", "12212222", "22221221", "21212222",
        "12221222", "22212212", "21222221", "12221222",
    ),
    "birch": (
        "22322232", "23222222", "22232222", "32222232",
        "22223222", "23222222", "22232222", "32222232",
    ),
    "jungle": (
        "22121222", "21222212", "32212222", "22210222",
        "22122212", "12222232", "22212222", "21222221",
    ),
    "acacia": (
        "22212232", "21222212", "22231222", "12222222",
        "23222122", "22221222", "21222232", "22212221",
    ),
    "dark_oak": (
        "21222122", "12212212", "22221222", "21202221",
        "12222122", "22212212", "21222221", "12221222",
    ),
    "mangrove": (
        "21222122", "12222212", "22212222", "21203221",
        "22222122", "12221222", "22212212", "21222221",
    ),
    "cherry": (
        "22212222", "21222212", "23212222", "22210222",
        "22122232", "12222222", "22212212", "21222222",
    ),
    "pale_oak": (
        "22232222", "21222212", "23222222", "22212232",
        "22222122", "12222222", "22232212", "21222222",
    ),
}
STRIPPED_BARK = (
    "22232222", "23222212", "22212222", "12222232",
    "22222122", "32222222", "22232212", "21222222",
)

# Padrões 8x8 de baixa frequência para blocos já presentes na base.
BLOCKS = {
    "dirt": {
        "palette": ["493124", "69452E", "8B603B", "AD8152"],
        "pattern": (
            "22122222", "21222232", "22212222", "32222122",
            "22221222", "12222223", "22222122", "23222212",
        ),
    },
    "stone": {
        "palette": ["343A3D", "535C60", "747E80", "9BA3A0"],
        "pattern": (
            "22222222", "22122222", "22222212", "22212222",
            "22222222", "12222222", "22222212", "22222222",
        ),
    },
    "cobble": {
        "palette": ["343638", "53585A", "747A79", "A0A39B"],
        "pattern": (
            "00122001", "11222110", "22201222", "12222112",
            "01122210", "12220221", "22211222", "01222100",
        ),
    },
    "gravel": {
        "palette": ["615E56", "827E73", "A39D8D", "C1B9A6"],
        "pattern": (
            "22212222", "12222232", "22221222", "32222212",
            "22212222", "21223222", "22222122", "23222212",
        ),
    },
    "sand": {
        "palette": ["A58F68", "C0AA7B", "D6C18F", "E7D7AA"],
        "pattern": (
            "22222232", "22212222", "32222222", "22222212",
            "22232222", "21222222", "22222232", "22212222",
        ),
    },
    "planks": {
        "palette": ["49301F", "704A2D", "96683D", "BD8B57"],
        "pattern": (
            "22222232", "22122222", "22212222", "23222212",
            "22222122", "12222222", "22232222", "22221222",
        ),
    },
}

ARMOR = {
    "leather":   {"icon": "leather",   "palette": ["3C281D", "775033", "AE7A4C", "D4A16B"], "style": "leather"},
    "chain":     {"icon": "chainmail", "palette": ["303B42", "657780", "AAB9BE", "E0E7E7"], "style": "chain"},
    "iron":      {"icon": "iron",      "palette": ["343D48", "6D7B87", "AEBBC3", "E8EEF0"], "style": "plate"},
    "gold":      {"icon": "gold",      "palette": ["63400D", "A87918", "E0B949", "FFE49A"], "style": "plate"},
    "diamond":   {"icon": "diamond",   "palette": ["14545A", "258E91", "66D5D0", "C0FFF0"], "style": "plate"},
    "netherite": {"icon": "netherite", "palette": ["211D2A", "42384D", "71637A", "B49EAA"], "style": "plate"},
    "copper":    {"icon": "copper",    "palette": ["54301F", "9C542F", "D8884B", "80A99A"], "style": "plate"},
}
ICON_MASKS = {
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

def species_for(name: str) -> str:
    value = name.lower()
    for key in ("birch", "spruce", "jungle", "acacia", "dark_oak",
                "mangrove", "cherry", "pale_oak"):
        if key in value:
            return key
    if "big_oak" in value:
        return "dark_oak"
    return "oak"

def as_palette(values: list[str]) -> list[tuple[int, int, int, int]]:
    return [rgb(value) + (255,) for value in values]

def side_log(name: str) -> Image.Image:
    seed = int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:8], 16)
    stripped = "stripped" in name.lower()
    species = species_for(name)
    palette = as_palette(STRIPPED if stripped else WOOD[species])
    pattern = STRIPPED_BARK if stripped else BARK[species]
    flip = seed & 1
    row_shift = (seed >> 2) & 1
    image = Image.new("RGBA", (8, 8), palette[2])
    pixels = image.load()
    for y in range(8):
        for x in range(8):
            sx = 7 - x if flip else x
            sy = (y + row_shift) % 8
            pixels[x, y] = palette[int(pattern[sy][sx])]

    # Pequenas cicatrizes de galho, sem formar olhos ou listras repetidas.
    if not stripped and species in ("oak", "jungle", "dark_oak", "mangrove"):
        cx = 2 + ((seed >> 5) % 4)
        cy = 2 + ((seed >> 9) % 4)
        marks = ((0, 0, 0), (-1, 0, 1), (1, 0, 2), (0, -1, 1), (0, 1, 1))
        for dx, dy, color in marks:
            px, py = cx + dx, cy + dy
            if 0 <= px < 8 and 0 <= py < 8:
                pixels[px, py] = palette[color]
    return image

def top_log(name: str) -> Image.Image:
    seed = int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:4], 16)
    stripped = "stripped" in name.lower()
    palette = as_palette(STRIPPED if stripped else WOOD[species_for(name)])
    image = Image.new("RGBA", (8, 8), palette[2])
    pixels = image.load()
    cx = 3.0 + (seed % 3) * 0.5
    cy = 3.0 + ((seed // 3) % 3) * 0.5
    for y in range(8):
        for x in range(8):
            distance = max(abs(x - cx), abs(y - cy))
            if distance >= 3:
                index = 0 if (x + y + seed) % 5 else 1
            elif distance >= 2:
                index = 1 if (x + y) % 4 else 2
            elif distance >= 1:
                index = 2 if (x * 3 + y + seed) % 5 else 1
            else:
                index = 3
            pixels[x, y] = palette[index]
    return image

def block_kind(path: str) -> str | None:
    stem = Path(path).stem.lower()
    if "cobble" in stem:
        return "cobble"
    if stem in ("stone", "smooth_stone", "andesite", "granite", "diorite"):
        return "stone"
    if "gravel" in stem:
        return "gravel"
    if "sand" in stem:
        return "sand"
    if "dirt" in stem or stem == "grass_path":
        return "dirt"
    if "planks" in stem or stem.startswith("wood_"):
        return "planks"
    return None

def block_texture(path: str, kind: str) -> Image.Image:
    data = BLOCKS[kind]
    seed = int(hashlib.sha256(path.encode("utf-8")).hexdigest()[:4], 16)
    palette = as_palette(data["palette"])
    pattern = data["pattern"]
    image = Image.new("RGBA", (8, 8), palette[2])
    pixels = image.load()
    mirror = seed & 1
    offset = (seed >> 3) & 1
    for y in range(8):
        for x in range(8):
            sx = 7 - x if mirror else x
            sy = (y + offset) % 8
            pixels[x, y] = palette[int(pattern[sy][sx])]
    return image

def paint_face(image: Image.Image, rect: tuple[int, int, int, int],
               palette: list[tuple[int, int, int]], seed: int, style: str) -> None:
    x0, y0, width, height = rect
    if width <= 0 or height <= 0:
        return
    for y in range(height):
        for x in range(width):
            edge = x == 0 or y == 0 or x == width - 1 or y == height - 1
            if edge:
                index = 0
            elif style == "chain":
                index = 1 if (x + y + seed) % 2 else 2
                if (x + 2 * y + seed) % 9 == 0:
                    index = 3
            else:
                index = 2
                if y == 1 and (x + seed) % 3 != 0:
                    index = 3
                elif x == 1 and (y + seed) % 4 == 0:
                    index = 3
                elif x == width - 2:
                    index = 1
                if style == "leather":
                    if y == height // 2 or (x == width // 2 and y > 2):
                        index = 1
                    if (x + y + seed) % 13 == 0:
                        index = 3
                elif style == "plate":
                    if height >= 6 and y == height // 2 and x not in (1, width - 2):
                        index = 1
                    if width >= 4 and (x + 2 * y + seed) % 17 == 0:
                        index = 3
            image.putpixel((x0 + x, y0 + y), palette[index] + (255,))

def paint_box(image: Image.Image, u: int, v: int, width: int,
              height: int, depth: int, palette: list[tuple[int, int, int]],
              seed: int, style: str) -> None:
    faces = (
        (u + depth, v, width, depth),
        (u + depth + width, v, width, depth),
        (u, v + depth, depth, height),
        (u + depth, v + depth, width, height),
        (u + depth + width + depth, v + depth, width, height),
        (u + depth + width, v + depth, depth, height),
    )
    for index, rect in enumerate(faces):
        paint_face(image, rect, palette, seed + index * 3, style)

def armor_map(material: str, layer: int) -> Image.Image:
    data = ARMOR[material]
    palette = [rgb(value) for value in data["palette"]]
    style = data["style"]
    image = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    if layer == 1:
        paint_box(image, 0, 0, 8, 8, 8, palette, 2, style)
        paint_box(image, 32, 0, 8, 8, 8, palette, 5, style)
        paint_box(image, 16, 16, 8, 12, 4, palette, 8, style)
        paint_box(image, 40, 16, 4, 12, 4, palette, 11, style)
        paint_box(image, 0, 16, 4, 12, 4, palette, 14, style)
    else:
        paint_box(image, 16, 16, 8, 12, 4, palette, 21, style)
        paint_box(image, 0, 16, 4, 12, 4, palette, 26, style)
    return image

def armor_icon(material: str, piece: str) -> Image.Image:
    palette = [rgb(value) for value in ARMOR[material]["palette"]]
    mask = ICON_MASKS[piece]
    image = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    for y, row in enumerate(mask):
        for x, cell in enumerate(row):
            if cell == ".":
                continue
            edge = any(
                nx < 0 or ny < 0 or nx >= 8 or ny >= 8 or mask[ny][nx] == "."
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
            )
            if edge:
                color = palette[0]
            elif (x + y) % 5 == 0:
                color = palette[3]
            elif ARMOR[material]["style"] == "chain" and (x + y) % 2:
                color = palette[1]
            else:
                color = palette[2]
            if piece == "helmet" and y == 4:
                color = palette[0] if x in (2, 5) else palette[1]
            image.putpixel((x, y), color + (255,))
    return image.resize((16, 16), Image.Resampling.NEAREST)

def encode_png(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--saida", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--previa", type=Path, default=DEFAULT_PREVIEW)
    args = parser.parse_args()

    if not args.base.is_file():
        raise SystemExit(f"Pacote-base não encontrado: {args.base}")
    with zipfile.ZipFile(args.base, "r") as source:
        if source.testzip() is not None:
            raise SystemExit("O pacote-base falhou no teste CRC.")
        files = {
            item.filename: source.read(item.filename)
            for item in source.infolist() if not item.is_dir()
        }

    log_names = sorted(
        name for name in files
        if name.startswith("textures/blocks/") and name.lower().endswith(".png")
        and (
            Path(name).stem.lower().startswith("log_")
            or Path(name).stem.lower().startswith("stripped_")
            or "_log" in Path(name).stem.lower()
        )
    )
    if not log_names:
        raise SystemExit("Nenhuma textura de tronco foi encontrada.")
    for name in log_names:
        stem = Path(name).stem.lower()
        result = top_log(stem) if stem.endswith("_top") else side_log(stem)
        files[name] = encode_png(result)

    block_paths = []
    for name in sorted(files):
        if not name.startswith("textures/blocks/") or not name.lower().endswith(".png"):
            continue
        kind = block_kind(name)
        if kind is None:
            continue
        with Image.open(io.BytesIO(files[name])) as old_image:
            if old_image.size != (8, 8):
                continue
        files[name] = encode_png(block_texture(name, kind))
        block_paths.append(name)

    armor_paths = []
    for material in ARMOR:
        for layer in (1, 2):
            path = f"textures/models/armor/{material}_{layer}.png"
            files[path] = encode_png(armor_map(material, layer))
            armor_paths.append(path)
        for piece in ICON_MASKS:
            path = f"textures/items/{ARMOR[material]['icon']}_{piece}.png"
            files[path] = encode_png(armor_icon(material, piece))
            armor_paths.append(path)

    manifest_path = "manifest.json"
    if manifest_path not in files:
        raise SystemExit("manifest.json ausente.")
    manifest = json.loads(files[manifest_path].decode("utf-8-sig"))
    manifest["header"]["version"] = "0.6.3"
    for module in manifest.get("modules", []):
        module["version"] = "0.6.3"
    manifest["header"]["description"] = (
        "LowMine Equilibrado 8x 0.6.3 - madeira natural, blocos compactos, armaduras e UI transparente."
    )
    files[manifest_path] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    list_path = "textures/textures_list.json"
    if list_path in files:
        texture_list = json.loads(files[list_path].decode("utf-8-sig"))
        additions = sorted(path[:-4] for path in armor_paths)
        files[list_path] = (
            json.dumps(sorted(set(texture_list) | set(additions)),
                       ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")

    note = (
        "\nLowMine 0.6.3: troncos 8x8 com marcas orgânicas e quatro tons; "
        "blocos selecionados redesenhados em 8x8; sete conjuntos de armaduras "
        "com painéis e contornos compactos. A interface transparente e os "
        "visuais de itens já existentes foram preservados.\n"
    ).encode("utf-8")
    for note_path in ("LEIA-ME.txt", "CREDITOS.txt"):
        if note_path in files and b"LowMine 0.6.3" not in files[note_path]:
            files[note_path] += note

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.saida, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as target:
        for name in sorted(files):
            target.writestr(name, files[name])

    preview = Image.new("RGB", (640, 360), (24, 26, 31))
    draw = ImageDraw.Draw(preview)
    draw.text((12, 10), "LOWMINE 0.6.3 | TRONCOS E BLOCOS 8x8", fill=(235, 235, 235))
    x, y = 12, 38
    for name in log_names[:12]:
        with Image.open(io.BytesIO(files[name])) as source_image:
            thumb = source_image.convert("RGBA").resize((48, 48), Image.Resampling.NEAREST)
            preview.paste(thumb, (x, y), thumb)
        x += 52
        if x > 590:
            x = 12
            y += 52
    draw.text((12, 205), "ARMADURAS | MAPA UV 64x32", fill=(235, 235, 235))
    x = 12
    for material in ARMOR:
        with Image.open(io.BytesIO(files[f"textures/models/armor/{material}_1.png"])) as source_image:
            thumb = source_image.resize((80, 40), Image.Resampling.NEAREST)
            preview.paste(thumb, (x, 228))
        x += 88
    args.previa.parent.mkdir(parents=True, exist_ok=True)
    preview.save(args.previa, format="PNG", optimize=True)

    print(json.dumps({
        "arquivo": str(args.saida),
        "bytes": args.saida.stat().st_size,
        "troncos_redesenhados": len(log_names),
        "blocos_redesenhados": len(block_paths),
        "texturas_armadura": len(armor_paths),
        "conjuntos_armadura": len(ARMOR),
        "resolucao_blocos_e_troncos": "8x8",
        "mapas_uv_armadura": "64x32",
        "icones_armadura": "16x16 (pixel art 8x8 ampliada por nearest-neighbor)",
        "ui": "preservada: desktop, mobile, baús, Ender, shulker e barril",
        "previa": str(args.previa),
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
