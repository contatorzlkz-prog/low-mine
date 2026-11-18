#!/usr/bin/env python3
"""Etapa reproduzível que aplica o redesign LowMine 0.6.0."""
from __future__ import annotations
import base64, sys, zlib
from pathlib import Path
TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
SOURCE = TOOLS / "redesenhar_v060_impl.py"
PARTS = TOOLS / "redesign_v060_parts"
try:
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in sorted(PARTS.glob("*.b64")))
    code = zlib.decompress(base64.b64decode(encoded)).decode("utf-8")
except Exception as exc:
    raise SystemExit(f"Não foi possível carregar a implementação v0.6.0: {exc}") from exc
args = sys.argv[1:]
if not args:
    args = ["--base", str(ROOT / "build" / "LowMine-Equilibrado-8x-v0.5.0.mcpack"),
            "--saida", str(ROOT / "build" / "LowMine-Equilibrado-8x-v0.6.0.mcpack"),
            "--previa", str(ROOT / "build" / "LowMine-Texturas-8x8-v0.6.0.png")]
sys.argv = [str(SOURCE), *args]
scope = {"__name__": "__main__", "__file__": str(SOURCE)}
exec(compile(code, str(SOURCE), "exec"), scope)
