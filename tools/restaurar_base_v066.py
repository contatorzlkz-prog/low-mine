#!/usr/bin/env python3
"""Reempacota a base conhecida 0.6.4 sem alterar assets, UI ou partículas."""
from __future__ import annotations
import argparse, json, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.4.mcpack"
DEFAULT_OUT = ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.6.mcpack"
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--saida", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    if not args.base.is_file():
        raise SystemExit("Base 0.6.4 não encontrada: " + str(args.base))
    with zipfile.ZipFile(args.base, "r") as source:
        bad = source.testzip()
        if bad is not None:
            raise SystemExit("CRC inválido na base: " + bad)
        files = {item.filename: source.read(item.filename)
                 for item in source.infolist() if not item.is_dir()}
    if "manifest.json" not in files:
        raise SystemExit("manifest.json ausente.")
    manifest = json.loads(files["manifest.json"].decode("utf-8-sig"))
    if manifest.get("format_version") != 2 or manifest.get("header", {}).get("version") != [0, 6, 4]:
        raise SystemExit("A base não é exatamente a versão estável 0.6.4.")
    manifest["header"]["version"] = [0, 6, 6]
    manifest["header"]["name"] = "LowMine Equilibrado 8x v0.6.6"
    manifest["header"]["description"] = "Pacote de recuperação baseado nos assets conhecidos da versão 0.6.4."
    for module in manifest.get("modules", []):
        module["version"] = [0, 6, 6]
    files["manifest.json"] = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.saida, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as target:
        for name in sorted(files):
            target.writestr(name, files[name])
    print(json.dumps({
        "arquivo": str(args.saida), "bytes": args.saida.stat().st_size,
        "base": "0.6.4", "nova_versao": manifest["header"]["version"],
        "somente_manifesto_alterado": True, "assets_preservados": True
    }, ensure_ascii=False, indent=2))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
