#!/usr/bin/env python3
"""Valida um pacote LowMine Equilibrado 8x sem iniciar o Minecraft."""
from __future__ import annotations
import base64
import zlib
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / "validar_pacote_impl_v050.zlib.b64"
if not ARQUIVO.is_file():
    raise SystemExit(f"Implementação ausente: {ARQUIVO}")
try:
    codigo = zlib.decompress(base64.b64decode(ARQUIVO.read_text(encoding="ascii"))).decode("utf-8")
except Exception as exc:
    raise SystemExit(f"Não foi possível carregar o validador: {exc}") from exc
nome_fonte = PASTA / "validar_pacote_impl_v050.py"
escopo = {"__name__": "__main__", "__file__": str(nome_fonte)}
exec(compile(codigo, str(nome_fonte), "exec"), escopo)
