# LowMine Ultra Low

LowMine is a Minecraft Bedrock resource-pack adaptation for low-end devices. **v0.3.0 removes the PvP profile and keeps one deliberately low-visual profile.** The original work is credited to XiaoCraft and remains subject to CC BY-NC 3.0.

> **Test candidate only.** Static checks pass, but import, UI behavior, compatibility and real FPS/frame-time results still need to be tested in Minecraft.

## v0.3.0 changes

- Removed the PvP subpack and flattened the former Lite profile into the only profile.
- Set custom particle amount to 0% and turned optional visual controls off by default.
- Removed the unused geyser toggle: the Lite profile already hard-disables those geyser emitters, and no pack-setting query used that toggle.
- Added registered desktop and pocket/touch JSON UI overrides for inventory and crafting, plus desktop chest, barrel, shulker and data-driven containers.
- Lowered inventory/chest backdrop alpha to 0.08 where the classic UI exposes the screen background variable.
- Reduced opacity of shared opaque dialog textures, slot backgrounds, hotbar panels and touch-control textures. This shared dialog texture may also make other classic UI dialogs translucent.
- Reduced selected menu images and the emote wheel; replaced the cloud texture with a transparent 1×1 image.
- Tightened the air fog range to 32–48 in 104 fog definitions. This is visual fog, not renderer culling.
- Preserved the existing LowMine UUID identity so Bedrock can treat this as an update to v0.2.0.

No measured FPS gain is claimed. Fog does not guarantee that hidden chunks stop being processed, and transparent UI does not directly make the game world render faster.

## Static package audit

| Property | v0.2.0 | v0.3.0 |
|---|---:|---:|
| Archive entries | 1,136 | 925 |
| JSON files | 487 | 318 |
| PNG files | 605 | 566 |
| Interactive settings | 9 | 8 |
| Profiles | Lite + PvP | One Ultra Low profile |
| PNG pixel count | 2,254,921 | 610,722 |

The summed PNG pixel area is **72.92% lower** than the v0.2.0 archive. At four bytes per pixel, that is a rough uncompressed RGBA estimate of 9.02 MB versus 2.44 MB, not a measurement of actual GPU memory or runtime FPS. The compressed package is 664,342 bytes, about 44.95% smaller than v0.2.0.

Other checks: 318/318 JSON files parsed, 29 language files checked, 94 biome entries and 104 fog definitions checked, with no unresolved custom fog references. See [the complete audit](docs/BASELINE_AUDIT.md).

## Import and test

1. Import `LowMine-Ultra-Low-v0.3.0-TEST.mcpack` into Minecraft Bedrock.
2. Activate **LowMine Ultra Low** in Global Resources or the world's Resource Packs.
3. Open pack settings and confirm the eight active controls appear.
4. Open the player inventory and crafting screen; check backdrop transparency.
5. Open a small chest, large chest, Ender Chest, shulker box and barrel. Check the backdrop and panel transparency.
6. Check the hotbar, item slots and mobile touch controls. Confirm selected/pressed states remain visible and buttons can still be used.
7. Enter a world and check particles, fog, clouds, HUD, chat, water, Nether/End and multiplayer.

Record the exact Bedrock version, device, render distance, simulation distance, selected settings and any content-log messages. Use [the runtime test template](docs/TEST_REPORT_TEMPLATE.md).

The inventory/chest UI work uses classic JSON UI definitions based on Mojang's current sample pack, including a separate pocket inventory screen. Some Bedrock builds/UI modes may ignore or behave differently with resource-pack JSON UI files (including newer Ore UI paths). If the interface stays unchanged or breaks, report the exact Bedrock version and a screenshot; do not assume the override is active just because the JSON parses.

## Build and validate

Requires Python 3.10+ and Pillow:

```bash
python -m pip install Pillow
python tools/build_ultra_low.py "LowMine-Performance-v0.2.0.mcpack" "LowMine-Ultra-Low-v0.3.0.mcpack"
python tools/validate_pack.py "LowMine-Ultra-Low-v0.3.0.mcpack"
```

The v0.2.0 input package is required as the build source and is not committed in this repository. The builder preserves the LowMine UUID identity, writes deterministic ZIP timestamps and removes the PvP folder. The validator checks manifest, JSON, settings, translations, fog links and registered desktop/pocket UI overrides. Static validation is not an in-game compatibility test.

## Rendering limitations

A resource pack cannot patch RenderDragon, install a new Rust renderer, or tell the client to discard all geometry behind the player's camera or beyond a fog color. Bedrock handles chunk render distance inside the game engine. Block Culling applies to faces of custom block geometry, not a universal visibility switch for vanilla terrain. See [rendering limits and feasible optimizations](docs/RENDERING_LIMITS.md).

## Attribution and license

Original work: **Boosted FPS (Optimized Performance) v2.4.1**, by **XiaoCraft**.

- Original project: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance
- License: **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)** — https://creativecommons.org/licenses/by-nc/3.0/

This is an adaptation, not a new original pack or an endorsed project. Keep the original author credit and modification notice. The original non-commercial license terms apply; read [ATTRIBUTION.txt](ATTRIBUTION.txt).
