#!/usr/bin/env python3
"""Finaliza o LowMine para Bedrock estável e remove fundos/bordas da interface."""
from __future__ import annotations
import argparse
import io
import json
import re
import zipfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.3.mcpack"
DEFAULT_OUTPUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.4.mcpack"

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
    "ui/inventory_screen.json",
    "ui/inventory_screen_pocket.json",
    "ui/chest_screen.json",
)

def transparent_png(data: bytes, name: str) -> bytes:
    with Image.open(io.BytesIO(data)) as source:
        image = source.convert("RGBA")
    image.putalpha(Image.new("L", image.size, 0))
    output = io.BytesIO()
    image.save(output, format="PNG", optimize=True)
    with Image.open(io.BytesIO(output.getvalue())) as check:
        if check.getchannel("A").getbbox() is not None:
            raise RuntimeError(f"A textura {name} ainda possui pixels opacos.")
    return output.getvalue()

def clear_screen_alpha(value):
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if key == "$screen_background_alpha":
                value[key] = 0.0
            else:
                clear_screen_alpha(child)
    elif isinstance(value, list):
        for child in value:
            clear_screen_alpha(child)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--saida", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not args.base.is_file():
        raise SystemExit(f"Pacote de entrada não encontrado: {args.base}")

    with zipfile.ZipFile(args.base, "r") as source:
        bad = source.testzip()
        if bad is not None:
            raise SystemExit(f"CRC inválido no arquivo de entrada: {bad}")
        files = {item.filename: source.read(item.filename)
                 for item in source.infolist() if not item.is_dir()}

    if "manifest.json" not in files:
        raise SystemExit("manifest.json ausente na raiz do pacote.")
    manifest = json.loads(files["manifest.json"].decode("utf-8-sig"))
    header = manifest.get("header", {})
    modules = manifest.get("modules", [])
    if not isinstance(header, dict) or not isinstance(modules, list) or not modules:
        raise SystemExit("Seções header/modules inválidas no manifesto.")

    # Formato 2 é a estrutura estável para Resource Packs Bedrock.
    manifest["format_version"] = 2
    header["version"] = [0, 6, 4]
    header["min_engine_version"] = [1, 26, 40]
    header["name"] = re.sub(r"v0\.(?:5\.0|6\.[23])", "v0.6.4",
                            header.get("name", "LowMine Equilibrado 8x"))
    header["description"] = (
        "LowMine Equilibrado 8x v0.6.4 - texturas 8x8 e interface totalmente transparente."
    )
    for module in modules:
        if not isinstance(module, dict):
            raise SystemExit("Foi encontrado um módulo inválido no manifesto.")
        module["version"] = [0, 6, 4]
    # A seção settings pertence ao formato 3 Preview e não é necessária à renderização.
    manifest.pop("settings", None)
    files["manifest.json"] = (
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    ).encode("utf-8")

    for path in UI_JSON:
        if path not in files:
            raise SystemExit(f"Arquivo de UI ausente: {path}")
        data = json.loads(files[path].decode("utf-8-sig"))
        clear_screen_alpha(data)
        files[path] = (
            json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")

    for path in UI_SURFACES:
        if path not in files:
            raise SystemExit(f"Textura de interface ausente: {path}")
        files[path] = transparent_png(files[path], path)

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.saida, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as target:
        for name in sorted(files):
            target.writestr(name, files[name])
    print(json.dumps({
        "arquivo": str(args.saida),
        "bytes": args.saida.stat().st_size,
        "manifest_format": manifest["format_version"],
        "header_version": header["version"],
        "module_versions": [module["version"] for module in modules],
        "experimental_settings_removed": "settings" not in manifest,
        "background_alpha": 0,
        "ui_surface_textures_fully_transparent": len(UI_SURFACES),
        "ui_json_background_alpha": 0,
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
