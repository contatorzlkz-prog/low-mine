#!/usr/bin/env python3
"""Gera LowMine Equilibrado v0.4.0 a partir do pacote v0.3.2. Requer Pillow."""
from __future__ import annotations
import argparse, hashlib, json, shutil, stat, tempfile, zipfile
from pathlib import Path, PurePosixPath
from PIL import Image

VERSAO="0.4.0"
UUID_PACOTE="21ca0070-fc45-5c56-8812-4b1cda3172a8"
UUID_MODULO="006202c4-abf5-58cc-8640-9c11d742a01d"
CONTAGENS={
 "arrowspell.json":"1","cauldronspell.json":"1","evoker_spell.json":"1",
 "mobspell.json":"1","mobspell_ambient.json":"1","mobspell_lingering.json":"2",
 "noxious_gas_particle.json":"0","splashpotionspell.json":"4",
 "sulfur_bubble_particle.json":"0","sulfur_cube_particle.json":"0","witchspell.json":"1"
}
VERDE={"escuro":(54,91,39,255),"medio":(77,125,48,255),"claro":(111,151,57,255),"ponta":(143,168,66,255)}
SAMAMBAIA={"escuro":(47,88,40,255),"medio":(66,119,48,255),"claro":(91,143,60,255),"ponta":(123,160,73,255)}
SECO={"escuro":(103,94,48,255),"medio":(139,125,61,255),"claro":(169,151,76,255),"ponta":(193,170,91,255)}

def salvar_json(caminho,obj):
 caminho.parent.mkdir(parents=True,exist_ok=True)
 caminho.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def extrair_seguro(zip_origem,raiz):
 vistos=set()
 for item in zip_origem.infolist():
  nome=item.filename; p=PurePosixPath(nome); modo=(item.external_attr>>16)&0xffff
  if p.is_absolute() or ".." in p.parts or "\\" in nome or stat.S_ISLNK(modo):
   raise ValueError(f"Caminho inseguro: {nome}")
  if nome in vistos: raise ValueError(f"Entrada duplicada: {nome}")
  vistos.add(nome)
 zip_origem.extractall(raiz)

def pixel(im,x,y,cor):
 if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y),cor)

def grama_curta():
 im=Image.new("RGBA",(16,16),(0,0,0,0)); p=VERDE
 trilhas=[
  [(7,15,"escuro"),(7,14,"medio"),(7,13,"medio"),(6,12,"claro"),(6,11,"claro"),(5,10,"ponta"),(5,9,"ponta"),(4,8,"claro"),(4,7,"ponta")],
  [(8,15,"escuro"),(8,14,"medio"),(8,13,"medio"),(8,12,"claro"),(9,11,"claro"),(9,10,"ponta"),(10,9,"ponta"),(10,8,"claro"),(11,7,"ponta")],
  [(9,14,"medio"),(10,13,"claro"),(11,12,"ponta"),(6,14,"medio"),(5,13,"claro"),(4,12,"ponta")]
 ]
 for trilha in trilhas:
  for x,y,c in trilha: pixel(im,x,y,p[c])
 return im

def samambaia(top=False,seco=False):
 im=Image.new("RGBA",(16,16),(0,0,0,0)); p=SECO if seco else SAMAMBAIA
 if top:
  eixo=list(range(15,0,-1)); niveis=[(13,6),(10,5),(7,6),(4,7),(2,8)]
 else:
  eixo=list(range(15,4,-1)); niveis=[(13,5),(10,4),(7,5)]
 for i,y in enumerate(eixo): pixel(im,8,y,p["escuro"] if i<3 else p["medio"])
 for y,ponta_esq in niveis:
  for j,(x,yy) in enumerate([(7,y),(6,y-1),(5,y-2)]): pixel(im,x,yy,p["medio"] if j==0 else p["claro"])
  for j,(x,yy) in enumerate([(9,y),(10,y-1),(11 if y>5 else 10,y-2)]): pixel(im,x,yy,p["medio"] if j==0 else p["claro"])
  pixel(im,ponta_esq,y-3,p["ponta"]); pixel(im,min(14,16-ponta_esq),y-3,p["ponta"])
 pixel(im,8,0 if top else 4,p["ponta"])
 return im

def grama_alta(top,seco=False):
 im=Image.new("RGBA",(16,16),(0,0,0,0)); p=SECO if seco else VERDE
 if top:
  trilhas=[
   [(6,15,"escuro"),(6,13,"medio"),(5,11,"medio"),(4,9,"claro"),(3,7,"ponta"),(2,6,"ponta")],
   [(8,15,"escuro"),(8,13,"medio"),(8,11,"medio"),(9,9,"claro"),(10,7,"ponta"),(11,6,"ponta")],
   [(9,14,"medio"),(10,12,"claro"),(11,10,"ponta")]
  ]
 else:
  trilhas=[
   [(6,0,"ponta"),(6,2,"claro"),(7,4,"medio"),(7,6,"medio"),(7,8,"escuro"),(7,10,"escuro")],
   [(9,0,"ponta"),(9,2,"claro"),(8,4,"medio"),(8,6,"medio"),(8,8,"escuro"),(8,10,"escuro")],
   [(5,4,"claro"),(4,3,"ponta"),(10,4,"claro"),(11,3,"ponta")]
  ]
 for trilha in trilhas:
  for x,y,c in trilha: pixel(im,x,y,p[c])
 return im

def criar_texturas(raiz):
 arquivos={
  "textures/blocks/tallgrass.png":grama_curta(),
  "textures/blocks/fern.png":samambaia(),
  "textures/blocks/double_plant_grass_top.png":grama_alta(True),
  "textures/blocks/double_plant_grass_bottom.png":grama_alta(False),
  "textures/blocks/double_plant_fern_top.png":samambaia(True),
  "textures/blocks/double_plant_fern_bottom.png":samambaia(False),
  "textures/blocks/short_dry_grass.png":grama_curta(),
  "textures/blocks/tall_dry_grass.png":grama_alta(True,seco=True)
 }
 for nome,im in arquivos.items():
  p=raiz/nome; p.parent.mkdir(parents=True,exist_ok=True); im.save(p,format="PNG",optimize=True)
 return len(arquivos)

def ajustar_alpha(caminho,maximo=None,multiplicador=None):
 if not caminho.exists(): return
 with Image.open(caminho) as fonte: im=fonte.convert("RGBA")
 canal=im.getchannel("A")
 if maximo is not None:
  topo=canal.getextrema()[1] or 1
  canal=canal.point(lambda v:round(v*maximo/topo))
 elif multiplicador is not None:
  canal=canal.point(lambda v:max(0,min(255,round(v*multiplicador))))
 im.putalpha(canal); im.save(caminho,format="PNG",optimize=True)

def ajustar_interface(raiz):
 ui=raiz/"textures/ui"
 alphas={"screen_background.png":38,"dialog_background_opaque.png":38,
         "dialog_background_opaque_overlap_bottom.png":38,"slots_bg.png":50,
         "toolbar_background.png":46,"hotbar_start_cap.png":55,"hotbar_end_cap.png":55}
 for nome,valor in alphas.items(): ajustar_alpha(ui/nome,maximo=valor)
 for p in ui.glob("slot_enabled*.png"): ajustar_alpha(p,multiplicador=.78 if "hover" not in p.stem else .92)
 for p in ui.glob("slot_disabled*.png"): ajustar_alpha(p,multiplicador=.78 if "hover" not in p.stem else .92)
 controles=raiz/"textures/gui/controls"
 if controles.exists():
  for p in controles.glob("*.png"): ajustar_alpha(p,multiplicador=.90 if "pressed" not in p.stem else .98)

def ajustar_json_interface(raiz):
 arquivos=["ui/inventory_screen.json","ui/inventory_screen_pocket.json","ui/chest_screen.json","ui/data_driven_container_screen.json"]
 for nome in arquivos:
  p=raiz/nome
  if not p.exists(): continue
  dados=json.loads(p.read_text(encoding="utf-8-sig"))
  def visitar(node):
   if isinstance(node,dict):
    if node.get("$screen_background_alpha")==0.08: node["$screen_background_alpha"]=0.05
    for v in node.values(): visitar(v)
   elif isinstance(node,list):
    for v in node: visitar(v)
  visitar(dados); salvar_json(p,dados)

def ajustar_particulas(raiz):
 for nome,valor in CONTAGENS.items():
  p=raiz/"particles"/nome
  dados=json.loads(p.read_text(encoding="utf-8-sig")); achados=0
  def visitar(node):
   nonlocal achados
   if isinstance(node,dict):
    for k,v in list(node.items()):
     if k=="num_particles": node[k]=valor; achados+=1
     else: visitar(v)
   elif isinstance(node,list):
    for v in node: visitar(v)
  visitar(dados)
  if achados!=1: raise ValueError(f"Esperado um campo num_particles em {nome}; encontrado {achados}")
  salvar_json(p,dados)

def ajustar_neblina(raiz):
 total=0
 for p in (raiz/"fogs").glob("*.json"):
  dados=json.loads(p.read_text(encoding="utf-8-sig"))
  ar=dados.get("minecraft:fog_settings",{}).get("distance",{}).get("air",{})
  if "fog_start" in ar and "fog_end" in ar:
   ar["fog_start"]=64; ar["fog_end"]=96; salvar_json(p,dados); total+=1
 return total

def atualizar_manifesto(raiz):
 p=raiz/"manifest.json"; m=json.loads(p.read_text(encoding="utf-8-sig"))
 if m["header"].get("uuid")!=UUID_PACOTE: raise ValueError("UUID principal diferente da base LowMine")
 m["format_version"]=3
 h=m["header"]; h["name"]=f"§l§dLowMine Equilibrado §r§7v{VERSAO}"
 h["description"]="§dLowMine Equilibrado§r\\n§7Perfil único para PCs de baixo desempenho\\n§7Vegetação simplificada e interface translúcida\\n§7Créditos: XiaoCraft. Consulte ATTRIBUTION.txt."
 h["version"]=VERSAO
 for mod in m.get("modules",[]):
  if mod.get("uuid")!=UUID_MODULO: raise ValueError("UUID do módulo diferente da base LowMine")
  mod["version"]=VERSAO; mod["description"]="LowMine Equilibrado — pacote de recursos para Bedrock"
 m.pop("settings",None); m.pop("subpacks",None)
 m["metadata"]={"authors":["XiaoCraft (autor original)","Projeto LowMine (adaptação)"],
                "license":"CC BY-NC 3.0 (obra original adaptada; consulte ATTRIBUTION.txt)",
                "url":"https://github.com/contatorzlkz-prog/low-mine","product_type":"addon"}
 salvar_json(p,m)

def atualizar_atribuicao(raiz):
 texto=f"""LowMine Equilibrado v{VERSAO} — créditos e licença

Este pacote é uma adaptação de:
  Boosted FPS (Optimized Performance) v2.4.1
  Autor original: XiaoCraft
  Projeto original: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance

Alterações feitas pelo projeto LowMine na versão {VERSAO}:
  - Mantido um único perfil; o subpacote PvP continua removido.
  - Mantidos 177 limites de partículas em zero e reduzidas 11 contagens para valores baixos.
  - Criadas oito texturas 16x16 simplificadas para grama, samambaia e versões secas.
  - Ajustada a transparência do inventário, crafting, baús e hotbar.
  - Ajustada a neblina visual para 64–96 blocos; isso não é culling do motor.
  - Mantidos os UUIDs e atualizado o manifesto v3.

Esta é uma adaptação, não uma substituição da obra original. Não há promessa de aumento de FPS sem medição no jogo.

A obra original está licenciada sob Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0):
  https://creativecommons.org/licenses/by-nc/3.0/

O autor e o projeto originais são creditados acima. Esta adaptação não é endossada nem afiliada a XiaoCraft. A licença original proíbe uso principalmente destinado a vantagem comercial ou compensação monetária privada. Mantenha os créditos e respeite os termos completos da licença.
"""
 (raiz/"ATTRIBUTION.txt").write_text(texto,encoding="utf-8")

def compilar(origem:Path,destino:Path):
 if not origem.is_file() or not zipfile.is_zipfile(origem): raise ValueError("Pacote v0.3.2 inválido")
 with tempfile.TemporaryDirectory(prefix="lowmine-040-") as tmp:
  raiz=Path(tmp)/"pack"; raiz.mkdir()
  with zipfile.ZipFile(origem) as z:
   if z.testzip(): raise ValueError("CRC inválido no pacote de origem")
   extrair_seguro(z,raiz)
  atualizar_manifesto(raiz)
  ajustar_particulas(raiz)
  ajustar_neblina(raiz)
  ajustar_interface(raiz)
  ajustar_json_interface(raiz)
  texturas=criar_texturas(raiz)
  atualizar_atribuicao(raiz)
  destino.parent.mkdir(parents=True,exist_ok=True)
  with zipfile.ZipFile(destino,"w") as z:
   for p in sorted(x for x in raiz.rglob("*") if x.is_file()):
    info=zipfile.ZipInfo(p.relative_to(raiz).as_posix(),date_time=(2020,1,1,0,0,0))
    info.compress_type=zipfile.ZIP_DEFLATED; info.create_system=3; info.external_attr=(0o100644&0xffff)<<16
    z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(destino) as z:
  if z.testzip(): raise ValueError("CRC inválido no pacote gerado")
  for nome in z.namelist():
   if nome.endswith(".json"): json.loads(z.read(nome).decode("utf-8-sig"))
  m=json.loads(z.read("manifest.json"))
  assert m["header"]["version"]==VERSAO and isinstance(m["header"]["version"],str)
  assert "subpacks" not in m and "settings" not in m
 return {"arquivo":str(destino),"bytes":destino.stat().st_size,"sha256":hashlib.sha256(destino.read_bytes()).hexdigest(),"texturas_vegetacao":texturas}

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument("origem",type=Path,help="Pacote LowMine v0.3.2")
 ap.add_argument("destino",type=Path,help="Arquivo .mcpack de saída")
 a=ap.parse_args()
 print(json.dumps(compilar(a.origem,a.destino),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
