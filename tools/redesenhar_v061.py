#!/usr/bin/env python3
"""Aplica o refinamento visual LowMine 0.6.1 sem alterar a estrutura do pack."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import random
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.5.0.mcpack"
DEFAULT_OUTPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.1.mcpack"
DEFAULT_PREVIEW = ROOT / "build" / "LowMine-Preview-v0.6.1.png"

def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

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
    "helmet": [
        "........", "..####..", ".######.", ".##..##.",
        ".######.", "..####..", "........", "........",
    ],
    "chestplate": [
        "........", ".##..##.", ".######.", ".######.",
        ".######.", "..####..", "..####..", "........",
    ],
    "leggings": [
        "........", "..####..", ".######.", ".##..##.",
        "..##.##.", "..##.##.", "..#..#..", "........",
    ],
    "boots": [
        "........", ".##..##.", ".##..##.", ".######.",
        ".##..##.", ".##..##.", "........", "........",
    ],
}

def species_for(name: str) -> str:
    value = name.lower()
    if "birch" in value:
        return "birch"
    if "spruce" in value:
        return "spruce"
    if "jungle" in value:
        return "jungle"
    if "acacia" in value:
        return "acacia"
    if "dark_oak" in value or "big_oak" in value:
        return "dark_oak"
    if "mangrove" in value:
        return "mangrove"
    if "cherry" in value:
        return "cherry"
    if "pale_oak" in value:
        return "pale_oak"
    return "oak"

def side_log(name: str) -> Image.Image:
    seed = int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:8], 16)
    rng = random.Random(seed)
    palette_hex = STRIPPED if "stripped" in name.lower() else WOOD[species_for(name)]
    palette = [rgb(c) + (255,) for c in palette_hex]
    image = Image.new("RGBA", (8, 8), palette[2])
    birch = species_for(name) == "birch" and "stripped" not in name.lower()
    ridges = [rng.randint(0, 7), rng.randint(1, 6), rng.randint(2, 7)]
    pixels = image.load()

    for y in range(8):
        for i in range(len(ridges)):
            if rng.random() < 0.72:
                ridges[i] = max(0, min(7, ridges[i] + rng.choice((-1, 0, 1))))
        for x in range(8):
            if birch:
                index = 2 if (x + y + seed) % 5 else 3
                if rng.random() < 0.17:
                    index = 0
                elif rng.random() < 0.22:
                    index = 1
            else:
                distance = min(abs(x - ridge) for ridge in ridges)
                if distance == 0:
                    index = 0 if rng.random() < 0.76 else 1
                elif distance == 1:
                    index = 1 if rng.random() < 0.70 else 2
                else:
                    index = 2 if rng.random() < 0.76 else 3
                if rng.random() < 0.055:
                    index = rng.choice((0, 3))
            pixels[x, y] = palette[index]

    if not birch:
        for cx, cy in ((1 + seed % 5, 2 + (seed // 7) % 4), (5, 5)):
            for y in range(8):
                for x in range(8):
                    distance = abs(x - cx) + abs(y - cy)
                    if distance == 1:
                        pixels[x, y] = palette[0]
                    elif distance == 2 and (x + y + seed) % 2 == 0:
                        pixels[x, y] = palette[1]
    return image

def top_log(name: str) -> Image.Image:
    palette_hex = STRIPPED if "stripped" in name.lower() else WOOD[species_for(name)]
    palette = [rgb(c) + (255,) for c in palette_hex]
    seed = int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:4], 16)
    cx = 3.0 + (seed % 3) * 0.5
    cy = 3.0 + ((seed // 3) % 3) * 0.5
    image = Image.new("RGBA", (8, 8), palette[2])
    pixels = image.load()
    for y in range(8):
        for x in range(8):
            distance = max(abs(x - cx), abs(y - cy))
            if distance >= 3:
                index = 2 if (x + y + seed) % 4 else 3
            elif distance >= 2:
                index = 1
            elif distance >= 1:
                index = 0 if (x + y) % 3 else 1
            else:
                index = 3
            pixels[x, y] = palette[index]
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
                if (x + 2 * y + seed) % 7 == 0:
                    index = 3
            else:
                index = 2
                if (x + 2 * y + seed) % 9 == 0:
                    index = 3
                elif (2 * x + y + seed) % 11 == 0:
                    index = 1
                if style == "leather" and (x == 1 or x == width - 2):
                    index = 1
            image.putpixel((x0 + x, y0 + y), palette[index] + (255,))
    if width >= 4 and height >= 6:
        image.putpixel((x0 + 1, y0 + 1), palette[3] + (255,))
        image.putpixel((x0 + width - 2, y0 + height - 2), palette[1] + (255,))

def paint_box(image: Image.Image, u: int, v: int, width: int,
              height: int, depth: int, palette: list[tuple[int, int, int]],
              seed: int, style: str) -> None:
    faces = [
        (u + depth, v, width, depth),
        (u + depth + width, v, width, depth),
        (u, v + depth, depth, height),
        (u + depth, v + depth, width, height),
        (u + depth + width + depth, v + depth, width, height),
        (u + depth + width, v + depth, depth, height),
    ]
    for index, rect in enumerate(faces):
        paint_face(image, rect, palette, seed + index * 3, style)

def armor_map(material: str, layer: int) -> Image.Image:
    data = ARMOR[material]
    palette = [rgb(c) for c in data["palette"]]
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
    palette = [rgb(c) for c in ARMOR[material]["palette"]]
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
        files = {item.filename: source.read(item.filename)
                 for item in source.infolist() if not item.is_dir()}

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
        raise SystemExit("Nenhuma textura de tronco foi encontrada em textures/blocks.")
    for name in log_names:
        stem = Path(name).stem.lower()
        image = top_log(stem) if stem.endswith("_top") else side_log(stem)
        files[name] = encode_png(image)

    armor_paths: list[str] = []
    for material in ARMOR:
        for layer in (1, 2):
            path = f"textures/models/armor/{material}_{layer}.png"
            files[path] = encode_png(armor_map(material, layer))
            armor_paths.append(path)
        icon_material = ARMOR[material]["icon"]
        for piece in ICON_MASKS:
            path = f"textures/items/{icon_material}_{piece}.png"
            files[path] = encode_png(armor_icon(material, piece))
            armor_paths.append(path)

    manifest_path = "manifest.json"
    if manifest_path not in files:
        raise SystemExit("manifest.json ausente no pacote-base.")
    manifest = json.loads(files[manifest_path].decode("utf-8-sig"))
    manifest["header"]["version"] = "0.6.1"
    for module in manifest.get("modules", []):
        module["version"] = "0.6.1"
    manifest["header"]["description"] = (
        "LowMine Equilibrado 8x 0.6.1 - troncos naturais, armaduras pixel art e UI transparente."
    )
    files[manifest_path] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    list_path = "textures/textures_list.json"
    if list_path in files:
        texture_list = json.loads(files[list_path].decode("utf-8-sig"))
        additions = sorted({path[:-4] for path in armor_paths})
        files[list_path] = (json.dumps(sorted(set(texture_list) | set(additions)),
                                       ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    note = (
        "\nLowMine 0.6.1: troncos com veios irregulares em 8x8 e paletas compactas; "
        "sete conjuntos de armaduras redesenhados em mapas UV 64x32 e ícones pixel art. "
        "Inventário, telas mobile e contêineres mantêm os fundos transparentes.\n"
    ).encode("utf-8")
    for note_path in ("LEIA-ME.txt", "CREDITOS.txt"):
        if note_path in files and b"LowMine 0.6.1" not in files[note_path]:
            files[note_path] += note

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.saida, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as target:
        for name in sorted(files):
            target.writestr(name, files[name])

    preview = Image.new("RGB", (640, 320), (24, 26, 31))
    draw = ImageDraw.Draw(preview)
    draw.text((12, 10), "LOWMINE 0.6.1  |  TRONCOS 8x8", fill=(235, 235, 235))
    x, y = 12, 38
    for name in log_names[:12]:
        with Image.open(io.BytesIO(files[name])) as source_image:
            thumb = source_image.convert("RGBA").resize((48, 48), Image.Resampling.NEAREST)
            preview.paste(thumb, (x, y), thumb)
        x += 52
        if x > 590:
            x = 12
            y += 52
    draw.text((12, 205), "ARMADURAS  |  MAPA UV 64x32", fill=(235, 235, 235))
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
        "texturas_armadura": len(armor_paths),
        "conjuntos_armadura": len(ARMOR),
        "resolucao_troncos": "8x8",
        "mapas_uv_armadura": "64x32",
        "icones_armadura": "16x16 (pixel art 8x8 ampliada por nearest-neighbor)",
        "ui": "preservada: inventário desktop/mobile, baús, Ender, shulker e barril",
        "previa": str(args.previa),
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
