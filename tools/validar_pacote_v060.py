#!/usr/bin/env python3
"""Validador estático do LowMine Equilibrado 8x v0.6.0."""
from __future__ import annotations
import base64, sys, zlib
from pathlib import Path
TOOLS = Path(__file__).resolve().parent
SOURCE = TOOLS / "validar_v060_impl.py"
PARTS = TOOLS / "validator_v060_parts"
try:
    encoded = "".join(p.read_text(encoding="ascii").strip() for p in sorted(PARTS.glob("*.b64")))
    code = zlib.decompress(base64.b64decode(encoded)).decode("utf-8")
except Exception as exc:
    raise SystemExit(f"Não foi possível carregar o validador v0.6.0: {exc}") from exc
sys.argv = [str(SOURCE), *sys.argv[1:]]
scope = {"__name__": "__main__", "__file__": str(SOURCE)}
exec(compile(code, str(SOURCE), "exec"), scope)
