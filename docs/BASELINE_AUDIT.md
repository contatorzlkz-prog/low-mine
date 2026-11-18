# LowMine technical audit — v0.3.2

## Import failure root cause

The v0.3.0 test package used JSON arrays such as `[0, 3, 0]` for the manifest `header.version` and module `version` fields. Bedrock manifest format version 3 requires SemVer strings such as `"0.3.2"`. That mismatch explains the import screen's unknown name, zero UUID and version 0.0.0. v0.3.2 uses strings for header and module versions and is checked by the validator.

The v0.3.2 manifest also removes experimental custom pack settings. All included LowMine particle emitters are disabled directly in their definitions instead of depending on custom settings-query support.

## Package identity

- File: `LowMine-Ultra-Low-v0.3.2-FIXED.mcpack`
- Size: 655,459 bytes.
- SHA-256: `89bd88e7351943abede9ea0f8a49fe1cc3ff224b7a005302cd60622b471905b2`
- Manifest format: 3.
- Header version: string `"0.3.2"`.
- Module version: string `"0.3.2"`.
- UUIDs: valid, unique and retained from the LowMine identity.
- No custom `settings`, `subpacks` or PvP files.

## Static archive audit

| Item | Count/result |
|---|---:|
| ZIP entries | 925 |
| JSON files | 318 |
| Invalid JSON | 0 |
| PNG files | 566 |
| Total PNG pixel area | 610,722 |
| Biome entries | 94 |
| Fog JSON files | 104 |
| Particle JSON definitions | 188 |
| `max_particles` fields set to 0 | 177 |
| `num_particles` fields set to `"0"` | 11 |
| Desktop/pocket/chest UI files registered | 4 |
| Custom fog IDs unresolved | 0 |

All 188 particle definitions shipped with LowMine are statically disabled. This does not disable built-in effects that are not provided by this pack and does not imply a measured FPS gain.

## UI changes

The package retains the desktop inventory/crafting, pocket inventory, chest (small/large/Ender/shulker/barrel) and data-driven container UI overrides. These are registered via `ui/_ui_defs.json` and use current Mojang sample screen names/parents and a desktop backdrop alpha of 0.08.

Shared dialog-panel PNG alpha is reduced. This can affect other classic UI dialogs that use the same shared textures. UI JSON overrides are version-sensitive and must be tested in the exact Bedrock build.

## Texture footprint and performance interpretation

- The v0.2.0 PNG pixel area was 2,254,921; v0.3.2 is 610,722, a 72.92% reduction in summed pixel area.
- A rough RGBA estimate is pixels × 4 bytes: about 9.02 MB vs 2.44 MB.
- This is not actual GPU VRAM: Bedrock can atlas, transcode, load or retain textures differently.
- 566 PNG files is not the same as 566 GPU texture handles; block textures can be combined into atlases.
- The compressed package is much smaller than the source archive, but archive size is not runtime FPS.

Microsoft's current guidance says loaded textures are typically uncompressed in memory, texture handles have per-texture overhead, block textures can be atlas exceptions, too many files add overhead, and add-ons should target fewer than 800 texture handles. It also recommends keeping texture dimensions/usage lean and simplifying costly particle systems:
https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable

The official texture-budget reference explains the texel × 4 estimate and platform performance tiers:
https://learn.microsoft.com/en-us/minecraft/creator/documents/texturebudgets?view=minecraft-bedrock-stable

## Renderer limitations

Fog is visual and does not itself guarantee engine culling. Bedrock's Block Culling feature targets covered faces of custom block geometry, not universal vanilla terrain/behind-camera culling. A .mcpack cannot inject Rust into the client or replace RenderDragon.

See [RENDERING_LIMITS.md](RENDERING_LIMITS.md).

## Static validation result

The local v0.3.2 validator passed:
- ZIP CRC/integrity check.
- Unique, safe archive paths.
- Manifest format 3 and correct string versions.
- Valid/unique manifest UUIDs and XiaoCraft/CC BY-NC metadata.
- No experimental settings and no PvP content.
- 318/318 JSON files parsed.
- 188 particle definitions all statically disabled.
- No experimental pack-setting Molang queries remaining.
- XP orb render disabled; no orb billboard animation script.
- 94 biomes and 104 fog files; all LowMine fog identifiers resolve.
- All four custom UI files are registered and have expected screen structure.
- Translucent dialog textures and required assets exist.

Static validation does not launch Bedrock. The user must verify import, UI rendering and game performance in Minecraft.
