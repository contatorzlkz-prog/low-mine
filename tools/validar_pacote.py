#!/usr/bin/env python3
"""Validador estático do LowMine Equilibrado v0.4.0. Não abre o Minecraft nem mede FPS."""
from __future__ import annotations
import argparse, collections, hashlib, json, os, stat, sys, uuid, zipfile
from pathlib import PurePosixPath
from io import BytesIO
from PIL import Image

VERSAO="0.4.0"
UUID_PACOTE="21ca0070-fc45-5c56-8812-4b1cda3172a8"
UUID_MODULO="006202c4-abf5-58cc-8640-9c11d742a01d"
PARTICULAS={
 "arrowspell.json":"1","cauldronspell.json":"1","evoker_spell.json":"1",
 "mobspell.json":"1","mobspell_ambient.json":"1","mobspell_lingering.json":"2",
 "noxious_gas_particle.json":"0","splashpotionspell.json":"4",
 "sulfur_bubble_particle.json":"0","sulfur_cube_particle.json":"0","witchspell.json":"1"
}
VEGETACAO=[
 "textures/blocks/tallgrass.png","textures/blocks/fern.png",
 "textures/blocks/double_plant_grass_top.png","textures/blocks/double_plant_grass_bottom.png",
 "textures/blocks/double_plant_fern_top.png","textures/blocks/double_plant_fern_bottom.png",
 "textures/blocks/short_dry_grass.png","textures/blocks/tall_dry_grass.png"
]
TELAS=[
 "ui/inventory_screen.json","ui/inventory_screen_pocket.json",
 "ui/chest_screen.json","ui/data_driven_container_screen.json"
]

def validar(arquivo):
 erros=[]; relatorio={}
 try: z=zipfile.ZipFile(arquivo)
 except (OSError,zipfile.BadZipFile) as e: return [f"Não foi possível abrir o .mcpack: {e}"],relatorio
 with z:
  if z.testzip(): erros.append("Falha de integridade CRC no ZIP")
  infos=[i for i in z.infolist() if not i.is_dir()]
  nomes=[i.filename for i in infos]; unicos=set(nomes)
  if len(nomes)!=len(unicos): erros.append("Há caminhos duplicados no ZIP")
  for nome in nomes:
   p=PurePosixPath(nome); modo=(z.getinfo(nome).external_attr>>16)&0xffff
   if p.is_absolute() or ".." in p.parts or "\\" in nome or stat.S_ISLNK(modo):
    erros.append(f"Caminho inseguro: {nome}")
  relatorio["arquivos"]=len(nomes)
  if "manifest.json" not in unicos: return erros+["manifest.json não está na raiz"],relatorio
  jsons={}; invalidos=[]
  for nome in nomes:
   if nome.lower().endswith(".json"):
    try: jsons[nome]=json.loads(z.read(nome).decode("utf-8-sig"))
    except (UnicodeDecodeError,json.JSONDecodeError) as e: invalidos.append(f"{nome}: {e}")
  erros.extend("JSON inválido: "+x for x in invalidos)
  relatorio["json"]={"total":len(jsons),"invalidos":len(invalidos)}
  m=jsons.get("manifest.json",{}); h=m.get("header",{}); mods=m.get("modules",[])
  if m.get("format_version")!=3: erros.append("format_version precisa ser 3")
  if not isinstance(h.get("version"),str) or h.get("version")!=VERSAO: erros.append("header.version precisa ser a string SemVer 0.4.0")
  if not isinstance(h.get("min_engine_version"),str): erros.append("min_engine_version deve ser string no manifesto v3")
  if h.get("uuid")!=UUID_PACOTE: erros.append("UUID principal mudou inesperadamente")
  if not mods or mods[0].get("uuid")!=UUID_MODULO: erros.append("UUID do módulo mudou inesperadamente")
  if any(not isinstance(x.get("version"),str) or x.get("version")!=VERSAO for x in mods): erros.append("Versão de módulo inválida")
  if m.get("subpacks") or any(n.startswith("subpacks/") or "pvp_fps" in n.lower() for n in nomes): erros.append("Foi encontrado conteúdo PvP/subpack")
  if m.get("settings"): erros.append("O pacote não deve depender de configurações experimentais")
  ids=[h.get("uuid")]+[x.get("uuid") for x in mods]
  if len(ids)!=len(set(ids)): erros.append("UUIDs repetidos no manifesto")
  try:
   for value in ids: uuid.UUID(str(value))
  except (ValueError,TypeError): erros.append("UUID ausente ou inválido")
  meta=m.get("metadata",{})
  if "XiaoCraft" not in " ".join(meta.get("authors",[])): erros.append("Crédito de XiaoCraft ausente no metadata")
  if "CC BY-NC 3.0" not in str(meta.get("license","")): erros.append("Licença CC BY-NC 3.0 ausente no metadata")

  pfiles=[n for n in jsons if n.startswith("particles/") and n.endswith(".json")]
  campos=collections.Counter(); valores={}; excessos=[]
  for nome in pfiles:
   def andar(node):
    if isinstance(node,dict):
     for k,v in node.items():
      if k=="max_particles":
       campos[k]+=1
       if v!=0: excessos.append((nome,k,v))
      elif k=="num_particles":
       campos[k]+=1; valores[nome.split("/")[-1]]=v
      else: andar(v)
    elif isinstance(node,list):
     for v in node: andar(v)
   andar(jsons[nome])
  if len(pfiles)!=188: erros.append(f"Esperadas 188 definições de partículas, encontradas {len(pfiles)}")
  if campos["max_particles"]!=177: erros.append(f"Esperados 177 max_particles, encontrados {campos['max_particles']}")
  if campos["num_particles"]!=11: erros.append(f"Esperados 11 num_particles, encontrados {campos['num_particles']}")
  if excessos: erros.append(f"Há max_particles diferentes de zero: {excessos[:8]}")
  for nome,esperado in PARTICULAS.items():
   if valores.get(nome)!=esperado: erros.append(f"Contagem inesperada em {nome}: {valores.get(nome)!r}")
  relatorio["particulas"]={"arquivos":len(pfiles),"max_particles_zero":campos["max_particles"],"num_particles":valores}

  biomas=jsons.get("biomes_client.json",{}).get("biomes",{})
  fogs=[n for n in jsons if n.startswith("fogs/") and n.endswith(".json")]
  ids_fog={jsons[n].get("minecraft:fog_settings",{}).get("description",{}).get("identifier") for n in fogs}
  faltando=[v.get("fog_identifier") for v in biomas.values() if isinstance(v,dict) and str(v.get("fog_identifier","")).startswith("lowmine:") and v.get("fog_identifier") not in ids_fog]
  if len(biomas)!=94: erros.append(f"Esperados 94 biomas, encontrados {len(biomas)}")
  if len(fogs)!=104: erros.append(f"Esperados 104 arquivos de neblina, encontrados {len(fogs)}")
  if faltando: erros.append(f"Referências de neblina ausentes: {faltando[:8]}")
  for nome in fogs:
   ar=jsons[nome].get("minecraft:fog_settings",{}).get("distance",{}).get("air",{})
   if "fog_start" in ar and (ar.get("fog_start")!=64 or ar.get("fog_end")!=96): erros.append(f"Neblina fora do padrão 64–96 em {nome}")
  relatorio["biomas_neblina"]={"biomas":len(biomas),"arquivos":len(fogs),"referencias_faltando":faltando}

  registro=jsons.get("ui/_ui_defs.json",{}).get("ui_defs",[])
  for nome in TELAS:
   if nome not in registro or nome not in jsons: erros.append(f"Tela ausente/não registrada: {nome}")
   alphas=[]
   def buscar(node):
    if isinstance(node,dict):
     if "$screen_background_alpha" in node: alphas.append(node["$screen_background_alpha"])
     for v in node.values(): buscar(v)
    elif isinstance(node,list):
     for v in node: buscar(v)
   buscar(jsons.get(nome,{}))
   if not alphas or any(x!=0.05 for x in alphas): erros.append(f"Transparência de tela incorreta em {nome}: {alphas}")
  relatorio["telas_ui"]=[x for x in TELAS if x in registro]

  for nome in VEGETACAO:
   if nome not in unicos: erros.append(f"Textura de vegetação ausente: {nome}"); continue
   im=Image.open(BytesIO(z.read(nome))).convert("RGBA")
   if im.size!=(16,16): erros.append(f"Textura não é 16x16: {nome}")
   if im.getchannel("A").getextrema()[0]!=0: erros.append(f"Fundo não transparente: {nome}")
  relatorio["texturas_vegetacao"]=[x for x in VEGETACAO if x in unicos]

  for nome,limite in [
   ("textures/ui/screen_background.png",45),
   ("textures/ui/dialog_background_opaque.png",45),
   ("textures/ui/dialog_background_opaque_overlap_bottom.png",45)
  ]:
   if nome not in unicos: erros.append(f"Textura de interface ausente: {nome}")
   else:
    im=Image.open(BytesIO(z.read(nome))).convert("RGBA")
    if im.getchannel("A").getextrema()[1]>limite: erros.append(f"Textura ainda muito opaca: {nome}")
  for nome in ["ATTRIBUTION.txt","pack_icon.png","textures/ui/pack_icon.png","textures/ui/title.png"]:
   if nome not in unicos: erros.append(f"Arquivo obrigatório ausente: {nome}")
  atribuicao=z.read("ATTRIBUTION.txt").decode("utf-8",errors="replace") if "ATTRIBUTION.txt" in unicos else ""
  if "XiaoCraft" not in atribuicao or "CC BY-NC 3.0" not in atribuicao: erros.append("Créditos/licença ausentes do ATTRIBUTION.txt")
  relatorio["tamanho_bytes"]=os.path.getsize(arquivo)
  relatorio["sha256"]=hashlib.sha256(open(arquivo,"rb").read()).hexdigest()
 return erros,relatorio

def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("pacote",help="Arquivo .mcpack")
 args=ap.parse_args(); erros,relatorio=validar(args.pacote)
 print(json.dumps(relatorio,ensure_ascii=False,indent=2))
 if erros:
  print("\nFALHAS NA VALIDAÇÃO:",file=sys.stderr)
  for e in erros: print("- "+str(e),file=sys.stderr)
  return 1
 print("\nValidação estática aprovada. Ainda é necessário importar e testar no Minecraft.")
 return 0

if __name__=="__main__": raise SystemExit(main())
