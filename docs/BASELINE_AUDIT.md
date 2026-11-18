# LowMine technical audit — v0.2.0 and v0.3.0

## Source and scope

The supplied source pack was `Boosted FPS v2.4.1.mcpack`, authored by XiaoCraft. LowMine remains an attributed adaptation under the original CC BY-NC 3.0 terms.

This is a static archive audit. It does not launch Minecraft, emulate RenderDragon, verify live UI behavior or measure FPS.

## v0.3.0 archive facts

| Item | v0.2.0 | v0.3.0 |
|---|---:|---:|
| Archive entries | 1,136 | 924 |
| JSON files | 487 | 317 |
| PNG files | 605 | 566 |
| Language files | 29 | 29 |
| Active configurable controls | 9 | 8 |
| Profiles | Lite + PvP | One flattened Ultra Low profile |
| Archive size | 1,206,757 bytes | 662,876 bytes |

The v0.3.0 archive has no `subpacks/` directory and no PvP profile files. The previous Lite subpack contained 288 files; 109 of these replaced same-path base files when flattened. The PvP subpack contained 106 files and was removed.

The compressed archive is 543,881 bytes (45.07%) smaller than v0.2.0. This is a packaging/file-content comparison, not a runtime memory or FPS measurement.

## PNG texture-footprint estimate

- v0.2.0 PNG pixel count: 2,254,921.
- v0.3.0 PNG pixel count: 610,722.
- Pixel-area reduction: 72.92%.
- At four bytes per pixel, a rough uncompressed RGBA estimate is 9.02 MB versus 2.443 MB.

This estimate sums width × height × 4 for PNG images. It is not actual GPU VRAM: Bedrock may atlas, transcode, compress or load textures differently. It is useful only as a consistent image-footprint comparison between these two archives.

Selected images changed:
- Both pack icons: 400×400 to 256×256.
- Title image: 2048×302 to 1024×151.
- Emote wheel images: reduced to 128×119 or 96×96.
- Cloud texture: replaced with a transparent 1×1 PNG.
- Inventory slots, hotbar panels and touch controls: alpha reduced.

Block/item textures were not blindly downscaled. Most source textures were already small (many 16×16 or similarly small sprites); preserving their pixel detail avoids unnecessary blur and keeps the current art style.

## Particles and settings

- Active controls: 8 (one slider and seven toggles).
- Particle amount default: 0%.
- All seven optional toggles default to off.
- The unused geyser toggle was removed because the former Lite profile's geyser particle definitions were already set to `max_particles: 0` and no emitter queried that setting.
- The XP-orb control affects its render controller only; it does not change XP awarding or collection logic.

A setting default of 0/off is an initial preference, not proof that every vanilla particle or entity in the entire game is disabled. Resource-pack overrides only cover the assets/effects included in this pack.

## Fog and biomes

- Root `biomes_client.json`: 94 biome entries.
- Fog JSON files: 104 definitions.
- Custom LowMine fog identifiers referenced by the biome map resolve to definitions.
- The v0.3.0 build sets the `distance.air` fog start/end values to 32/48 in all 104 fog definitions where those fields exist.

This makes distant terrain visually disappear sooner. It is **not** a camera-direction culling system. The fog does not provide a resource-pack instruction to discard all blocks behind the fog, behind the camera or under the world. Do not interpret this as a confirmed CPU/GPU optimization.

## Inventory/chest UI and hotbar

New files:
- `ui/inventory_screen.json`
- `ui/chest_screen.json`
- `ui/data_driven_container_screen.json`

All three are registered in `ui/_ui_defs.json`. Inventory/crafting screens and desktop chest/container screens override the vanilla backdrop alpha to 0.08 while retaining the screen inheritance and pocket-screen branches from the current Mojang sample structure.

Hotbar slot backgrounds, inventory slot fills and mobile touch-control PNG alpha are also reduced. The underlying click regions, slot geometry, item icons and screen layout are not intentionally resized.

These overrides use the classic JSON UI route. Some Bedrock builds or Ore UI modes may ignore or behave differently with resource-pack JSON UI files. Only in-game testing can verify whether the user's exact Bedrock version applies them.

## Static validation

The final v0.3.0 package passed:
- ZIP integrity and unique-path checks.
- 924 archive entries, with no unsafe relative paths.
- 317/317 JSON files parsed.
- Eight active setting IDs match all pack-setting query references.
- All 29 language files include every manifest setting label.
- 94 biome entries and 104 fog definitions; no unresolved custom fog IDs.
- Inventory, chest and data-driven UI overrides are registered and contain the expected alpha/desktop/pocket branches.
- No PvP folder or subpack declarations remain.
- Two builds with identical source inputs produced byte-identical output.

Tools: `tools/build_ultra_low.py` and `tools/validate_pack.py`.

## v0.3.0 artifact identity

- File: `LowMine-Ultra-Low-v0.3.0-TEST.mcpack`
- Size: 662,876 bytes.
- SHA-256: `143c508d67ae25046d7ff782cde36190cacabd0d74f4443071afaea4240003c6`

## Known limitations and next tests

1. Import v0.3.0 into the exact Minecraft Bedrock build in use.
2. Confirm the pack and eight settings appear.
3. Test inventory/crafting, all container screens, hotbar and touch controls.
4. Inspect fog and cloud appearance in several dimensions and biomes.
5. Check world load, gameplay feedback, multiplayer, and content-log messages.
6. Compare vanilla and LowMine in the same world/scene, device, resolution, render distance and simulation distance; record FPS and frame-time stability.

## Original v0.2.0 audit (historical)

The v0.2.0 baseline had 1,136 files, 487 JSON files, 605 PNGs, 29 language files, nine active controls and two subpacks. It is superseded by v0.3.0.
