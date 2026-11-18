#!/usr/bin/env python3
"""Validador estático do LowMine Equilibrado 8x v0.5.0."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
import uuid
import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath
from PIL import Image

VERSAO = "0.5.0"
UUID_PACOTE = "21ca0070-fc45-5c56-8812-4b1cda3172a8"
UUID_MODULO = "006202c4-abf5-58cc-8640-9c11d742a01d"
TELAS = [
    "ui/inventory_screen.json",
    "ui/inventory_screen_pocket.json",
    "ui/chest_screen.json",
]
ESPECIES = [
    "leaves_oak", "leaves_oak_opaque",
    "leaves_birch", "leaves_birch_opaque",
    "leaves_spruce", "leaves_spruce_opaque",
    "leaves_jungle", "leaves_jungle_opaque",
    "leaves_acacia", "leaves_acacia_opaque",
    "leaves_big_oak", "leaves_big_oak_opaque",
    "leaves_mangrove", "leaves_mangrove_opaque",
    "leaves_cherry", "leaves_cherry_opaque",
    "leaves_azalea", "leaves_azalea_opaque",
    "azalea_leaves_flowers", "azalea_leaves_flowers_opaque",
]
TEXTURAS = [
    "grass_top", "grass_side", "dirt", "stone", "cobblestone", "gravel",
    "sand", "planks_oak", "log_oak", "log_oak_top", "tallgrass", "fern",
    "double_plant_grass_top", "double_plant_grass_bottom",
    "double_plant_fern_top", "double_plant_fern_bottom",
    "short_dry_grass", "tall_dry_grass",
] + ESPECIES

def validar(arquivo: Path) -> dict:
    if not arquivo.is_file():
        raise FileNotFoundError(arquivo)
    rel = {"arquivo": str(arquivo), "bytes": arquivo.stat().st_size}
    erros = []
    with zipfile.ZipFile(arquivo) as z:
        if z.testzip() is not None:
            erros.append("CRC do ZIP inválido")
        infos = [i for i in z.infolist() if not i.is_dir()]
        nomes = [i.filename for i in infos]
        conjunto = set(nomes)
        if len(nomes) != len(conjunto):
            erros.append("Caminhos duplicados no ZIP")
        for nome in nomes:
            p = PurePosixPath(nome)
            if p.is_absolute() or ".." in p.parts or "\\" in nome:
                erros.append(f"Caminho inseguro: {nome}")
        jsons = {}
        for nome in nomes:
            if nome.endswith(".json"):
                try:
                    jsons[nome] = json.loads(z.read(nome).decode("utf-8-sig"))
                except Exception as exc:
                    erros.append(f"JSON inválido em {nome}: {exc}")
        rel["entradas"] = len(nomes)
        rel["json"] = len(jsons)
        rel["png"] = sum(n.lower().endswith(".png") for n in nomes)
        if len(nomes) != 69:
            erros.append(f"Esperadas 69 entradas; encontradas {len(nomes)}")
        if len(jsons) != 21:
            erros.append(f"Esperados 21 JSON; encontrados {len(jsons)}")

        m = jsons.get("manifest.json")
        if not isinstance(m, dict):
            erros.append("manifest.json ausente ou inválido")
            m = {}
        h = m.get("header", {})
        mods = m.get("modules", [])
        if m.get("format_version") != 3:
            erros.append("Manifesto precisa usar format_version 3")
        if h.get("version") != VERSAO or not isinstance(h.get("version"), str):
            erros.append("Versão do cabeçalho diferente de 0.5.0")
        if not isinstance(h.get("min_engine_version"), str):
            erros.append("min_engine_version deve ser uma string SemVer")
        if h.get("uuid") != UUID_PACOTE:
            erros.append("UUID do pacote mudou inesperadamente")
        if not mods or mods[0].get("uuid") != UUID_MODULO:
            erros.append("UUID do módulo está ausente ou incorreto")
        if any(x.get("version") != VERSAO or not isinstance(x.get("version"), str) for x in mods):
            erros.append("Versão do módulo inválida")
        if m.get("subpacks") or any(n.startswith("subpacks/") for n in nomes):
            erros.append("O pacote não deve conter subpacotes")
        if "capabilities" in m:
            erros.append("Capacidades gráficas extras não são necessárias neste pacote")
        try:
            uuid.UUID(h.get("uuid", ""))
            uuid.UUID(mods[0].get("uuid", ""))
        except (ValueError, IndexError, AttributeError):
            erros.append("UUID inválido no manifesto")

        # Confere a relação entre definições de partículas e controles declarados.
        particle_files = [n for n in jsons if n.startswith("particles/") and n.endswith(".json")]
        if len(particle_files) != 14:
            erros.append(f"Esperadas 14 definições de partículas; encontradas {len(particle_files)}")
        references = set()
        for nome in particle_files:
            raw = z.read(nome).decode("utf-8", errors="replace")
            if "opt:" in raw:
                erros.append(f"Namespace antigo opt: encontrado em {nome}")
            references.update(re.findall(r"lowmine:[A-Za-z0-9_]+", raw))
        settings = {
            item.get("name")
            for item in m.get("settings", [])
            if isinstance(item, dict) and item.get("type") in ("slider", "toggle")
        }
        if len(settings) != 9:
            erros.append(f"Esperados 9 controles editáveis; encontrados {len(settings)}")
        if not references.issubset(settings):
            erros.append(f"Referências Molang sem controle no manifesto: {sorted(references - settings)}")
        if not settings.issubset(references):
            erros.append(f"Controles sem referência nos recursos: {sorted(settings - references)}")
        rel["particulas"] = len(particle_files)
        rel["controles_editaveis"] = len(settings)

        water = jsons.get("water/water.json", {}).get("minecraft:water_settings", {})
        if water.get("description", {}).get("identifier") != "minecraft:default_water":
            erros.append("Identificador da água incorreto")
        if water.get("caustics", {}).get("enabled") is not False:
            erros.append("Cáusticas da água precisam estar desativadas")
        if water.get("waves", {}).get("enabled") is not False:
            erros.append("Ondas da água precisam estar desativadas")
        concentrations = water.get("particle_concentrations", {})
        if any(concentrations.get(k) != 0.0 for k in ("chlorophyll", "suspended_sediment", "cdom")):
            erros.append("Concentrações de partículas da água não estão no perfil LowMine")
        shadows = jsons.get("shadows/global.json", {}).get("minecraft:shadow_settings", {})
        if shadows.get("shadow_style") != "blocky_shadows" or shadows.get("texel_size") != 16:
            erros.append("Configuração de sombras blocadas está ausente ou incorreta")

        ui_defs = jsons.get("ui/_ui_defs.json", {}).get("ui_defs", [])
        for tela in TELAS:
            if tela not in conjunto or tela not in ui_defs:
                erros.append(f"Tela de UI ausente ou não registrada: {tela}")
        if "ui/_ui_defs.json" not in conjunto:
            erros.append("ui/_ui_defs.json ausente")
        chest = jsons.get("ui/chest_screen.json", {})
        for name in (
            "small_chest_screen@common.inventory_screen_common",
            "large_chest_screen@common.inventory_screen_common",
            "ender_chest_screen@common.inventory_screen_common",
            "shulker_box_screen@chest.small_chest_screen",
            "barrel_screen@chest.small_chest_screen",
        ):
            if name not in chest:
                erros.append(f"Contêiner sem override de transparência: {name}")

        block_textures = [f"textures/blocks/{name}.png" for name in TEXTURAS]
        for nome in block_textures:
            if nome not in conjunto:
                erros.append(f"Textura de bloco ausente: {nome}")
                continue
            try:
                with Image.open(BytesIO(z.read(nome))) as im:
                    if im.size != (8, 8):
                        erros.append(f"Textura não é 8×8: {nome} ({im.size})")
            except Exception as exc:
                erros.append(f"PNG inválido em {nome}: {exc}")
        rel["texturas_bloco_8x8"] = len(block_textures) - sum(
            1 for e in erros if e.startswith("Textura de bloco ausente")
        )

        for obrigatorio in ("CREDITOS.txt", "LEIA-ME.txt", "pack_icon.png"):
            if obrigatorio not in conjunto:
                erros.append(f"Arquivo obrigatório ausente: {obrigatorio}")
        creditos = z.read("CREDITOS.txt").decode("utf-8", errors="replace") if "CREDITOS.txt" in conjunto else ""
        if "XiaoCraft" not in creditos or "CC BY-NC 3.0" not in creditos:
            erros.append("Créditos/licença do conteúdo adaptado não foram encontrados")
        if "PotatoCraft" not in creditos or "Embeddium" not in creditos or "Vanilla" not in creditos:
            erros.append("As referências estudadas não estão identificadas nos créditos")

        scripts = [n for n in nomes if n.lower().endswith((".js", ".ts", ".mcfunction"))]
        if scripts:
            erros.append(f"O Resource Pack não deve incluir scripts: {scripts[:8]}")
        behaviors = [n for n in nomes if n.startswith("functions/") or n.startswith("scripts/")]
        if behaviors:
            erros.append(f"Arquivos de lógica não esperados no Resource Pack: {behaviors[:8]}")

    rel["sha256"] = hashlib.sha256(arquivo.read_bytes()).hexdigest()
    if erros:
        raise ValueError("\n".join(erros))
    return rel

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("pacote", type=Path, help="Arquivo .mcpack para validar")
    args = ap.parse_args()
    try:
        resultado = validar(args.pacote)
    except Exception as exc:
        print(f"FALHA NA VALIDAÇÃO: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    print("Validação estática aprovada; teste visual e desempenho ainda são necessários no Minecraft.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
