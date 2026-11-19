#!/usr/bin/env python3
"""Confere que 0.6.6 é a base 0.6.4 intacta, exceto pelo manifesto."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
def read_pack(path: Path):
    if not path.is_file():
        raise FileNotFoundError(path)
    with zipfile.ZipFile(path, "r") as z:
        bad = z.testzip()
        if bad is not None:
            raise ValueError(f"CRC inválido em {path}: {bad}")
        return {item.filename: z.read(item.filename)
                for item in z.infolist() if not item.is_dir()}
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base", type=Path)
    parser.add_argument("pacote", type=Path)
    args = parser.parse_args()
    base, new = read_pack(args.base), read_pack(args.pacote)
    if set(base) != set(new):
        raise ValueError("Os caminhos dos assets mudaram em relação à base 0.6.4.")
    changed = {name for name in base if base[name] != new[name]}
    if changed != {"manifest.json"}:
        raise ValueError("Foram alterados arquivos além do manifesto: " + ", ".join(sorted(changed)[:20]))
    old = json.loads(base["manifest.json"].decode("utf-8-sig"))
    manifest = json.loads(new["manifest.json"].decode("utf-8-sig"))
    if old.get("format_version") != 2 or manifest.get("format_version") != 2:
        raise ValueError("Formato inesperado.")
    if old["header"].get("version") != [0, 6, 4] or manifest["header"].get("version") != [0, 6, 6]:
        raise ValueError("Versões de manifesto inesperadas.")
    if len(manifest.get("modules", [])) != len(old.get("modules", [])):
        raise ValueError("Quantidade de módulos foi alterada.")
    if any(m.get("version") != [0, 6, 6] for m in manifest.get("modules", [])):
        raise ValueError("Versão de módulo incorreta.")
    assets = {k:v for k,v in base.items() if k != "manifest.json"}
    if assets != {k:v for k,v in new.items() if k != "manifest.json"}:
        raise ValueError("Os assets não são idênticos à base.")
    print(json.dumps({
        "arquivo": str(args.pacote), "bytes": args.pacote.stat().st_size,
        "sha256": hashlib.sha256(args.pacote.read_bytes()).hexdigest(),
        "versao": manifest["header"]["version"],
        "arquivos_preservados": len(assets),
        "assets_alterados": 0, "resultado": "aprovado"
    }, ensure_ascii=False, indent=2))
    print("Aprovado: UI, texturas, partículas e demais assets são idênticos à versão 0.6.4.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
