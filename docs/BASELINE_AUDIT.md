# LowMine technical audit — v0.2.0

## Source and scope

The input supplied for this project was `Boosted FPS v2.4.1.mcpack`. The package manifest identifies its original project as Boosted FPS and its author as XiaoCraft. LowMine is an adaptation; the original attribution and CC BY-NC 3.0 terms are retained.

This audit is static. It reads the archive, JSON, manifest, language files and image dimensions. It does not launch Minecraft, emulate a device, verify every render path or measure FPS.

## Archive inventory

| File type | Count |
|---|---:|
| JSON | 487 |
| PNG | 605 |
| TGA | 11 |
| Language files | 29 |
| UI files | 2 |
| Material files | 1 |
| Attribution notice | 1 |
| Total v0.2.0 entries | 1,136 |

The source archive contained 1,135 entries. LowMine v0.2.0 has 1,136 because it adds `ATTRIBUTION.txt`. There are no duplicate archive paths or unsafe relative paths in the generated build.

## Manifest and profiles

- Manifest format version: 3.
- Minimum engine version carried over from the supplied manifest: `1.26.40`.
- Profiles: **LowMine Lite** (source folder `fps`) and **LowMine PvP** (source folder `pvp_fps`).
- Nine configurable controls: one slider and eight toggles.
- All manifest/module UUIDs are valid and unique.
- All custom setting identifiers use the `lowmine:` namespace.
- All setting references found in the resource files resolve to a declared manifest setting.

### Setting defaults

| Setting | Default | Effect described by the source definitions |
|---|---:|---|
| Particle amount | 50% | Scales configurable custom emitters |
| Potion/status effects | On | Keeps potion/status particle visuals |
| Witch/Evoker effects | Off | Custom brewing and spell particles |
| Arrow trails | Off | Custom arrow-trail particles |
| Cauldron effects | Off | Custom cauldron drips and splashes |
| Geysers | Off | Custom geyser columns, plumes and puffs |
| Geyser gas | Off | Gas particles around geyser fields |
| Sulfur particles | Off | Sulfur cave bubbles and cubes |
| XP orbs | Off | Hides the orb model; does not alter XP collection logic |

The slider controls the custom particle definitions that query it. It is not a global Minecraft particle setting.

## Particle/profile audit

- LowMine Lite contains 177 particle override JSON files whose emitter maximum is set to zero.
- LowMine PvP contains 48 such files.
- The nine settings are wired into particle definitions or the XP-orb render controller; all nine have at least one matching query reference.
- These counts describe file overrides, not a measured count of all particle instances removed during gameplay.

## Fog and biomes

- Base `biomes_client.json`: 94 biome entries and 94 fog references.
- Lite `biomes_client.json`: 94 biome entries and 94 fog references.
- Base fog directory: 104 definitions.
- Lite fog directory: 104 definitions.
- Every custom `lowmine:fog_...` reference in the base and Lite biome lists resolves to a corresponding fog definition.
- The remaining fog definitions include identifiers intended for vanilla fog behavior; their presence is not proof that they are unused in-game.

For the Plains example, the base profile uses a distant air fog range of 1032–1064, while Lite uses 60–88. Exact distances and colors vary by biome and medium. PvP has no separate fog override directory and uses the base fog set.

## Branding and texture footprint

- Main pack icon: 400×400 PNG.
- In-pack icon: 400×400 PNG.
- Title image: 2048×302 PNG, changed from the source's 4096×604.
- The title image now has 75% fewer pixels. This is a menu/UI asset reduction only; it is not evidence of higher in-world FPS.
- Existing entity, particle, HUD, chat, material and PBR-related assets were retained pending runtime testing rather than removed speculatively.

## Localization

- All 29 language files contain the manifest setting labels.
- Brazilian Portuguese strings were added to `pt_BR.lang`.
- English fallback strings were added to the remaining language files.
- Original work is still named in the attribution/credit strings.

## Validation result

The v0.2.0 candidate passed the static validator:
- ZIP integrity test passed.
- 1,136 unique archive entries.
- 487 JSON files parsed successfully; 0 invalid.
- 9 configurable setting identifiers checked.
- 29 language files checked; no missing setting labels.
- Base and Lite fog references checked; no missing custom fog IDs.
- Required icon, title and attribution files present.
- Builder was run twice with identical inputs; the output bytes and SHA-256 matched.

The validation script is `tools/validate_pack.py`. The builder is `tools/build_pack.py`.

## Known limitations and next tests

1. Import the pack into the exact Minecraft Bedrock version being used.
2. Confirm manifest v3 pack settings appear and respond correctly.
3. Test both profiles and all nine controls.
4. Inspect water, Nether/End fog and multiple biomes for visual problems.
5. Test world loading, multiplayer, HUD/chat and interactions with other packs.
6. Benchmark vanilla, source and LowMine using the same scene, device and settings.

Manifest custom pack settings are documented by Microsoft for resource packs and are read through Molang, but the feature documentation notes that the capability may change. See the [official custom pack settings guide](https://github.com/MicrosoftDocs/minecraft-creator/blob/main/creator/Documents/AddOns/CustomPackSettings.md).

No runtime test or FPS claim is included in this audit.
