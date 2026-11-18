#!/usr/bin/env python3
"""Validador estático do LowMine Equilibrado 8x v0.6.0."""
from __future__ import annotations
import base64, sys, zlib
from pathlib import Path
TOOLS = Path(__file__).resolve().parent
SOURCE = TOOLS / "validar_v060_impl.py"
BUNDLE = TOOLS / "validar_v060_impl.zlib.b64"
try:
    code = zlib.decompress(base64.b64decode(BUNDLE.read_text(encoding="ascii"))).decode("utf-8")
except Exception as exc:
    raise SystemExit(f"Não foi possível carregar o validador v0.6.0: {exc}") from exc
sys.argv = [str(SOURCE), *sys.argv[1:]]
scope = {"__name__": "__main__", "__file__": str(SOURCE)}
exec(compile(code, str(SOURCE), "exec"), scope)
