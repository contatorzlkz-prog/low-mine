#!/usr/bin/env python3
"""Build LowMine Ultra Low v0.3.1 from the v0.2.0 .mcpack. Requires Pillow.
Static pack edits only: this cannot alter RenderDragon or measure FPS."""
import argparse, hashlib, json, shutil, stat, tempfile, zipfile
from pathlib import Path, PurePosixPath
from PIL import Image

V = "0.3.1"
EN = {
"lowmine.settings.title":"LOWMINE ULTRA LOW  |  v0.3.1",
"lowmine.settings.intro":"Single ultra-low profile. Optional visuals are disabled by default.",
"lowmine.section.particles":"MINIMAL PARTICLES",
"lowmine.setting.particle_amount":"Particle amount (%)",
"lowmine.setting.particle_amount.help":"Controls LowMine custom emitters. 0% is the lowest visual setting.",
"lowmine.setting.potion_effects":"Potion and status effects",
"lowmine.setting.potion_effects.help":"Visual particles from potions and status effects.",
"lowmine.setting.witch_evoker":"Witch and Evoker effects",
"lowmine.setting.witch_evoker.help":"Custom brewing and spell particles.",
"lowmine.setting.arrow_trails":"Arrow trails",
"lowmine.setting.arrow_trails.help":"Custom trails behind tipped arrows.",
"lowmine.setting.cauldron":"Cauldron effects",
"lowmine.setting.cauldron.help":"Custom drips and splashes around filled cauldrons.",
"lowmine.setting.noxious_gas":"Geyser gas",
"lowmine.setting.noxious_gas.help":"Drifting gas particles around geyser fields.",
"lowmine.setting.sulfur":"Sulfur particles",
"lowmine.setting.sulfur.help":"Sulfur bubbles and cubes in sulfur caves.",
"lowmine.section.entities":"ENTITY RENDERING",
"lowmine.setting.xp_orbs":"Experience orbs",
"lowmine.setting.xp_orbs.help":"Hides orb models only. XP collection remains unchanged.",
"lowmine.credit":"Original work by XiaoCraft; adapted by LowMine. See ATTRIBUTION.txt.",
"pack.name":"§dLowMine Ultra Low§r",
"pack.description":"§7Single-profile ultra-low Bedrock resource pack.§r",
"accessibility.chat.howtoemote":"§dLowMine Ultra Low loaded. §7Adapted from XiaoCraft's Boosted FPS."
}
PT = {
"lowmine.settings.title":"LOWMINE ULTRA LOW  |  v0.3.1",
"lowmine.settings.intro":"Perfil único ultra leve. Os efeitos visuais opcionais começam desativados.",
"lowmine.section.particles":"PARTÍCULAS NO MÍNIMO",
"lowmine.setting.particle_amount":"Quantidade de partículas (%)",
"lowmine.setting.particle_amount.help":"Controla os emissores personalizados do LowMine. 0% é o mínimo visual.",
"lowmine.setting.potion_effects":"Efeitos de poções e status",
"lowmine.setting.potion_effects.help":"Partículas visuais de poções e efeitos de status.",
"lowmine.setting.witch_evoker":"Efeitos de bruxas e evocadores",
"lowmine.setting.witch_evoker.help":"Partículas personalizadas de preparo e feitiços.",
"lowmine.setting.arrow_trails":"Rastros de flechas",
"lowmine.setting.arrow_trails.help":"Rastros personalizados de flechas com efeito.",
"lowmine.setting.cauldron":"Efeitos de caldeirões",
"lowmine.setting.cauldron.help":"Gotas e respingos personalizados em caldeirões cheios.",
"lowmine.setting.noxious_gas":"Gás de gêiseres",
"lowmine.setting.noxious_gas.help":"Partículas de gás nas áreas de gêiseres.",
"lowmine.setting.sulfur":"Partículas de enxofre",
"lowmine.setting.sulfur.help":"Bolhas e cubos de enxofre nas cavernas.",
"lowmine.section.entities":"RENDERIZAÇÃO DE ENTIDADES",
"lowmine.setting.xp_orbs":"Orbes de experiência",
"lowmine.setting.xp_orbs.help":"Oculta apenas o modelo dos orbes. A coleta de XP continua normal.",
"lowmine.credit":"Trabalho original de XiaoCraft; adaptação do LowMine. Consulte ATTRIBUTION.txt.",
"pack.name":"§dLowMine Ultra Low§r",
"pack.description":"§7Pacote Bedrock de perfil único ultra leve.§r",
"accessibility.chat.howtoemote":"§dLowMine Ultra Low carregado. §7Adaptação do Boosted FPS de XiaoCraft."
}
def js(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
def extract(z, root):
    seen=set()
    for i in z.infolist():
        p=PurePosixPath(i.filename); mode=(i.external_attr>>16)&0xffff
        if p.is_absolute() or ".." in p.parts or "\\" in i.filename or stat.S_ISLNK(mode):
            raise ValueError(f"Unsafe ZIP entry: {i.filename}")
        if i.filename in seen: raise ValueError(f"Duplicate ZIP entry: {i.filename}")
        seen.add(i.filename)
    z.extractall(root)
def flatten(root):
    base=root/"subpacks"; lite=base/"fps"; pvp=base/"pvp_fps"
    if not lite.is_dir(): raise ValueError("Expected v0.2.0 source with subpacks/fps")
    files=list(lite.rglob("*")); moved=over=0
    for src in files:
        if not src.is_file(): continue
        dst=root/src.relative_to(lite); dst.parent.mkdir(parents=True,exist_ok=True)
        over += int(dst.exists()); shutil.copyfile(src,dst); moved+=1
    removed=sum(p.is_file() for p in pvp.rglob("*")) if p.exists() else 0
    shutil.rmtree(base)
    return {"lite_files_flattened":moved,"base_files_overwritten":over,"pvp_files_removed":removed}
def manifest(root):
    p=root/"manifest.json"; m=json.loads(p.read_text(encoding="utf-8")); h=m["header"]
    h["name"]="§l§dLowMine Ultra Low §r§7v0.3.1"
    h["description"]="§dLowMine Ultra Low§r\n§7Single ultra-low profile for Minecraft Bedrock\n§7Reduced particles, transparent UI and low-resolution textures\n§7Original work by XiaoCraft (CC BY-NC 3.0). See ATTRIBUTION.txt."
    h["version"]=V
    for x in m.get("modules",[]): x["description"]="LowMine Ultra Low — single-profile resource pack"; x["version"]=V
    m.pop("subpacks",None); m["capabilities"]=[x for x in m.get("capabilities",[]) if x!="pbr"]
    out=[]
    removed={"lowmine.section.profiles","lowmine.subpacks.help","lowmine.setting.geysers","lowmine.setting.geysers.help"}
    for x in m.get("settings",[]):
        if x.get("text") in removed or x.get("name")=="lowmine:geysers": continue
        if x.get("name")=="lowmine:particle_amount": x["default"]=0
        if x.get("type")=="toggle": x["default"]=False
        out.append(x)
    # Manifest v3 setting labels are literal text values in the current documented schema.
    for item in out:
        if isinstance(item.get("text"), str) and item["text"] in PT:
            item["text"] = PT[item["text"]]
    m["settings"]=out
    m["metadata"]={"authors":["XiaoCraft (original author)","LowMine Project (adaptation)"],"license":"CC BY-NC 3.0 (adapted source work; see ATTRIBUTION.txt)","url":"https://github.com/contatorzlkz-prog/low-mine","product_type":"addon"}
    js(p,m)
def lang(root):
    remove={"lowmine.section.profiles","lowmine.subpacks.help","lowmine.setting.geysers","lowmine.setting.geysers.help"}
    for p in (root/"texts").glob("*.lang"):
        data=PT if p.name=="pt_BR.lang" else EN
        lines=p.read_text(encoding="utf-8-sig",errors="replace").splitlines()
        lines=[s for s in lines if not ("=" in s and not s.lstrip().startswith("#") and s.split("=",1)[0].strip() in set(data)|remove)]
        while lines and not lines[-1].strip(): lines.pop()
        lines += ["","## LowMine Ultra Low settings"]+[k+"="+v for k,v in data.items()]
        p.write_text("\n".join(lines)+"\n",encoding="utf-8")
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".json",".lang",".ui",".material"}:
            try: s=p.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError: continue
            t=s.replace("LowMine Performance","LowMine Ultra Low").replace("LowMine Lite and LowMine PvP","LowMine Ultra Low").replace("LowMine Lite","LowMine Ultra Low").replace("LowMine PvP","LowMine Ultra Low")
            if t!=s: p.write_text(t,encoding="utf-8")
def alpha(p, factor):
    with Image.open(p) as im: im=im.convert("RGBA")
    im.putalpha(im.getchannel("A").point(lambda a: max(0,min(255,round(a*factor)))))
    im.save(p,format="PNG",optimize=True)
def resize(p, size):
    with Image.open(p) as im: im=im.convert("RGBA").resize(size,Image.Resampling.LANCZOS)
    im.save(p,format="PNG",optimize=True)
def images(root):
    sizes={"pack_icon.png":(256,256),"textures/ui/pack_icon.png":(256,256),"textures/ui/title.png":(1024,151),"textures/ui/emote_wheel_base.png":(128,119)}
    sizes.update({f"textures/ui/emote_wheel_select_{i}.png":(128,119) for i in range(6)})
    sizes.update({f"textures/ui/emote_wheel_updated_select_{i}.png":(96,96) for i in range(4)})
    changed=[]
    for name,size in sizes.items():
        p=root/name
        if p.exists(): resize(p,size); changed.append((name,*size))
    ui=root/"textures/ui"
    for p in ui.glob("slot_enabled*.png"): alpha(p,.68 if "hover" in p.stem else .38)
    for p in ui.glob("slot_disabled*.png"): alpha(p,.62 if "hover" in p.stem else .34)
    for name,f in [("slots_bg.png",.34),("toolbar_background.png",.34),("hotbar_start_cap.png",.38),("hotbar_end_cap.png",.38)]:
        p=ui/name
        if p.exists(): alpha(p,f)
    for p in ui.glob("hotbar_*.png"):
        if p.stem not in {"hotbar_start_cap","hotbar_end_cap"}: alpha(p,.38)
    # Shared vanilla dialog-panel textures: lower their fill opacity while retaining edges.
    for name in ["dialog_background_opaque.png","dialog_background_opaque_overlap_bottom.png"]:
        p=ui/name
        if p.exists(): alpha(p,.28)
    c=root/"textures/gui/controls"
    if c.exists():
        for p in c.glob("*.png"): alpha(p,.68 if "pressed" in p.stem else .48)
    p=ui/"screen_background.png"
    if p.exists():
        with Image.open(p) as im: im=im.convert("RGBA")
        im.putpixel((0,0),(0,0,0,48)); im.save(p,format="PNG",optimize=True)
    p=root/"textures/environment/clouds.png"
    if p.exists(): Image.new("RGBA",(1,1),(255,255,255,0)).save(p,format="PNG",optimize=True); changed.append(("textures/environment/clouds.png",1,1))
    return changed
def fog(root):
    count=0
    for p in (root/"fogs").glob("*.json"):
        d=json.loads(p.read_text(encoding="utf-8")); a=d.get("minecraft:fog_settings",{}).get("distance",{}).get("air",{})
        if "fog_start" in a and "fog_end" in a: a["fog_start"],a["fog_end"]=32,48; js(p,d); count+=1
    return count
def ui(root):
    js(root/"ui/inventory_screen.json",{"namespace":"crafting","crafting_screen@crafting.inventory_screen_base":{"$screen_background_alpha":.08},"inventory_screen@crafting.inventory_screen_base":{"$screen_background_alpha":.08}})
    # Pocket/mobile inventory uses a separate screen definition in current Bedrock samples.
    js(root/"ui/inventory_screen_pocket.json",{"namespace":"crafting_pocket","inventory_screen_pocket@crafting_pocket.inventory_screen_pocket_base":{"$screen_background_alpha":.08}})
    c={"namespace":"chest"}
    variants=[("small_chest_screen","chest.small_chest_panel","pocket_containers.small_chest_panel","common.inventory_screen_common"),("large_chest_screen","chest.large_chest_panel","pocket_containers.large_chest_panel","common.inventory_screen_common"),("ender_chest_screen","chest.ender_chest_panel","pocket_containers.ender_chest_panel","common.inventory_screen_common"),("shulker_box_screen","chest.shulker_box_panel","pocket_containers.shulker_box_panel","chest.small_chest_screen"),("barrel_screen","chest.barrel_panel","pocket_containers.barrel_panel","chest.small_chest_screen")]
    for key,desk,pocket,parent in variants:
        c[key+"@"+parent]={"$close_on_player_hurt|default":True,"$use_custom_pocket_toast|default":False,"close_on_player_hurt":"$close_on_player_hurt","use_custom_pocket_toast":"$use_custom_pocket_toast","variables":[{"requires":"$desktop_screen","$screen_content":desk,"$screen_bg_content":"common.screen_background","$screen_background_alpha":.08},{"requires":"$pocket_screen","$use_custom_pocket_toast":True,"$screen_content":pocket}]}
    js(root/"ui/chest_screen.json",c)
    js(root/"ui/data_driven_container_screen.json",{"namespace":"data_driven_container","screen@common.inventory_screen_common":{"$close_on_player_hurt|default":True,"$use_custom_pocket_toast|default":False,"close_on_player_hurt":"$close_on_player_hurt","use_custom_pocket_toast":"$use_custom_pocket_toast","variables":[{"requires":"$desktop_screen","$screen_content":"data_driven_container.desktop_panel","$screen_bg_content":"common.screen_background","$screen_background_alpha":.08},{"requires":"$pocket_screen","$use_custom_pocket_toast":True,"$screen_content":"pocket_containers.data_driven_container_panel"}]}})
    p=root/"ui/_ui_defs.json"; d=json.loads(p.read_text(encoding="utf-8-sig")) if p.exists() else {"ui_defs":[]}
    for n in ["ui/inventory_screen.json","ui/inventory_screen_pocket.json","ui/chest_screen.json","ui/data_driven_container_screen.json"]:
        if n not in d.setdefault("ui_defs",[]): d["ui_defs"].append(n)
    js(p,d)
def main():
    a=argparse.ArgumentParser(description=__doc__); a.add_argument("source",type=Path); a.add_argument("output",type=Path); x=a.parse_args()
    if not x.source.is_file(): a.error("Source .mcpack not found")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/"p"; root.mkdir()
        with zipfile.ZipFile(x.source) as z:
            if z.testzip(): raise ValueError("Source archive CRC error")
            extract(z,root)
        flat=flatten(root); manifest(root); lang(root); changed=images(root); fogged=fog(root); ui(root)
        (root/"ATTRIBUTION.txt").write_text(
"LowMine Ultra Low v0.3.1 — attribution and license\n\nThis package is an adaptation of:\n  Boosted FPS (Optimized Performance) v2.4.1\n  Original author: XiaoCraft\n  Original project: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance\n\nChanges made by the LowMine Project in v0.3.1:\n  - Removed the separate PvP subpack and flattened the former Lite profile as the only pack.\n  - Reduced particle defaults to the minimum and disabled optional visual toggles by default.\n  - Made inventory/chest screen backdrops and hotbar/touch UI textures more transparent.\n  - Reduced selected menu textures and removed visible cloud texture detail.\n  - Tightened the visual fog range; this is not renderer occlusion culling.\n\nThis is an adaptation, not an original replacement for the source work. No measured FPS improvement is claimed. Runtime testing is required.\n\nThe original work is listed under the Creative Commons Attribution-NonCommercial 3.0 Unported license (CC BY-NC 3.0):\n  https://creativecommons.org/licenses/by-nc/3.0/\n\nThe original author and project are credited above. This adaptation is not endorsed by or affiliated with XiaoCraft. The license prohibits use primarily intended for commercial advantage or private monetary compensation. Keep attribution and license notices with redistributed copies.\n",encoding="utf-8")
        x.output.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(x.output,"w") as z:
            for p in sorted(q for q in root.rglob("*") if q.is_file()):
                i=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2020,1,1,0,0,0)); i.compress_type=zipfile.ZIP_DEFLATED; i.create_system=3; i.external_attr=(0o100644&0xffff)<<16
                z.writestr(i,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    with zipfile.ZipFile(x.output) as z:
        if z.testzip(): raise ValueError("Built archive CRC error")
        if any(n.startswith("subpacks/") for n in z.namelist()): raise ValueError("Unexpected subpacks remain")
        for n in z.namelist():
            if n.endswith(".json"): json.loads(z.read(n).decode("utf-8-sig"))
    print(json.dumps({"flatten":flat,"images_changed":changed,"fog_files_updated":fogged,"bytes":x.output.stat().st_size,"sha256":hashlib.sha256(x.output.read_bytes()).hexdigest()},indent=2))
if __name__=="__main__": main()
