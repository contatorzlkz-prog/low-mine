# LowMine Ultra Low

LowMine is an attributed Minecraft Bedrock resource-pack adaptation for low-end devices. **v0.3.2 fixes the v0.3.0 import failure** and keeps a single Ultra Low profile; the PvP subpack is removed.

> **Test candidate, not a measured FPS release.** The package passed static validation. Import and performance still need to be tested inside Minecraft Bedrock.

## v0.3.2 — import fix and harder low profile

- Corrected manifest v3 header and module version fields to SemVer strings (`"0.3.2"`). v0.3.0 used arrays, which caused the import screen to show unknown name, zero UUID and version 0.0.0.
- Removed experimental custom pack settings instead of relying on them for particle reduction.
- Hard-disabled all 188 particle definitions included by LowMine: 177 `max_particles` fields set to 0 and 11 `num_particles` fields set to `"0"`.
- Kept XP-orb drawing disabled but preserved the game's XP collection behavior.
- Kept the single flattened Lite profile, with no PvP subpack.
- Kept translucent inventory/crafting/chest/desktop/pocket UI overrides and hotbar/touch texture edits.
- Preserved the LowMine UUID identity so v0.3.2 is an update to the same pack rather than a second pack.

## Static audit

| Check | Result |
|---|---:|
| Manifest format | 3 |
| Header/module versions | SemVer string 0.3.2 |
| Archive entries | 925 |
| JSON files | 318 valid, 0 invalid |
| Particle definitions | 188 disabled |
| Biomes | 94 |
| Fog definitions | 104 |
| PNG files | 566 |
| Total PNG pixel area | 610,722 |
| Settings/subpacks | None |
| PvP content | Removed |

The PNG pixel area is a texture-footprint proxy, not a VRAM or FPS measurement. Microsoft notes that loaded textures are typically held uncompressed and that each texture handle carries overhead; atlas textures are an exception. Microsoft recommends add-ons stay below 800 texture handles and minimizing unnecessary files/texture area. The number of PNG files is not identical to the number of GPU texture handles. See [Microsoft's performance and resource-use guidance](https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable).

## Import

1. Use the file `LowMine-Ultra-Low-v0.3.2-FIXED.mcpack`.
2. Open it with Minecraft Bedrock.
3. Confirm the import screen shows **LowMine Ultra Low v0.3.2**, not unknown name/version.
4. Activate the single **LowMine Ultra Low** resource pack.
5. Check inventory, crafting, small/large chest, Ender Chest, shulker, barrel, hotbar and touch controls.
6. Enter a world and check fog, clouds, potion visuals, particles, XP collection, HUD and chat.

The pack has no settings menu by design; its included emitters are statically disabled. Effects not defined by this pack may still appear.

Use [the runtime test report](docs/TEST_REPORT_TEMPLATE.md) and [the v0.3.2 technical audit](docs/BASELINE_AUDIT.md). If Minecraft rejects it, send the exact import message and the Bedrock version.

## Build and validate

Requires Python 3.10+ and Pillow:

```bash
python -m pip install Pillow
python tools/build_ultra_low.py "LowMine-Performance-v0.2.0.mcpack" "LowMine-Ultra-Low-v0.3.2-FIXED.mcpack"
python tools/validate_pack.py "LowMine-Ultra-Low-v0.3.2-FIXED.mcpack"
```

The v0.2.0 adapted source package is the input to the builder and is not committed in this repository. The builder uses stable ZIP timestamps, so identical inputs produce byte-identical outputs.

## Actual engine limitations

Fog is visual only; it does not stop RenderDragon from processing geometry. Block Culling only targets covered faces of custom block geometry, not a universal behind-camera or underground culler. A resource pack cannot inject Rust into the Bedrock client or replace RenderDragon. See [rendering limits and verified possibilities](docs/RENDERING_LIMITS.md).

## Attribution and license

Original work: **Boosted FPS (Optimized Performance) v2.4.1**, by **XiaoCraft**.

- Original project: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance
- License: **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)** — https://creativecommons.org/licenses/by-nc/3.0/

This is an adaptation, not a new original pack or an endorsed project. Keep the original author credit and modification notice. The original non-commercial license terms apply; see [ATTRIBUTION.txt](ATTRIBUTION.txt).
