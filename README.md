# LowMine Performance

LowMine is a Minecraft Bedrock resource-pack project for low-end devices. The current test candidate is an attributed adaptation of **Boosted FPS (Optimized Performance) v2.4.1 by XiaoCraft**.

> **v0.2.0 is a test candidate, not a benchmarked release.** Static validation is complete; Minecraft import, in-game behavior, compatibility and FPS measurements still need to be tested.

## v0.2.0 changes

- Rebranded pack name, icons, title image, profile labels and localized settings.
- Assigned new stable manifest/module UUIDs and a dedicated `lowmine:` namespace for settings and custom fog identifiers.
- Added nine configurable controls: one particle slider and eight toggles.
- Set particle amount to 50% by default; optional visual effects start disabled, while potion/status visuals stay enabled.
- Reduced the menu title texture from 4096×604 to 2048×302 (75% fewer pixels for that image only).
- Preserved the original Lite/PvP structure, fog behavior, HUD overrides, PBR capability and original creator credits.
- Added static validation and reproducible-build tooling.

No measured FPS increase is claimed. Reducing one menu texture does not establish an in-game FPS gain.

## Package baseline

| Property | Audited value |
|---|---:|
| Minecraft Bedrock manifest | format version 3 |
| Minimum engine version in source manifest | 1.26.40 |
| Profiles | LowMine Lite, LowMine PvP |
| Configurable controls | 9 |
| JSON files | 487 |
| Valid JSON files | 487 |
| Base biome entries | 94 |
| Fog definitions per base/Lite set | 104 |
| Archive entries in v0.2.0 | 1,136 |

See [the technical audit](docs/BASELINE_AUDIT.md), [roadmap](ROADMAP.md) and [changelog](CHANGELOG.md).

## Test instructions

1. Import `LowMine-Performance-v0.2.0.mcpack` into Minecraft Bedrock.
2. Confirm the pack appears as **LowMine Performance v0.2.0**.
3. Activate it and open its settings using the gear icon.
4. Check that the nine controls appear with readable labels.
5. Test **LowMine Lite** and **LowMine PvP** separately. Lite is the stronger visual-reduction profile; PvP preserves its extra HUD and a longer view.
6. Check particles, potion visuals, XP-orb visibility, biome fog, chat/HUD and world loading.

Record the exact Bedrock version, device, selected profile, render distance and any content-log errors. See the audit document for the test checklist.

## Build and validation

Requires Python 3.10+.

```bash
python tools/build_pack.py "Boosted FPS v2.4.1.mcpack" "LowMine-Performance-v0.2.0.mcpack" --icon assets/lowmine-pack-icon.png --title assets/lowmine-title.png
python tools/validate_pack.py "LowMine-Performance-v0.2.0.mcpack"
```

Before rebuilding, create the two branding inputs in assets/: extract pack_icon.png from the v0.2.0 package as assets/lowmine-pack-icon.png, and textures/ui/title.png as assets/lowmine-title.png. The builder uses stable UUIDs and fixed ZIP timestamps so identical inputs produce identical output bytes. The validator checks ZIP integrity, manifest IDs, JSON syntax, settings references, translations, subpack folders, fog references and required assets. These checks do not emulate Minecraft.

The v0.2.0 .mcpack binary is currently delivered as a test artifact outside this repository; it must be uploaded to releases/ manually before a GitHub release can be published.

## Compatibility note

This pack uses manifest format version 3 and resource-pack setting queries such as `query.get_pack_setting` and `query.is_pack_setting_enabled`. Microsoft documents pack settings and their Molang integration, but the feature documentation still describes the capability as subject to change. Test it on the exact Bedrock release you use: [Microsoft custom pack settings guide](https://github.com/MicrosoftDocs/minecraft-creator/blob/main/creator/Documents/AddOns/CustomPackSettings.md).

## Attribution and license

Original work: **Boosted FPS (Optimized Performance) v2.4.1**, by **XiaoCraft**.

- Original project: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance
- License: **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)** — https://creativecommons.org/licenses/by-nc/3.0/

This is an adaptation, not an original replacement or an endorsed project. Original author credit and modification notices are retained. The original non-commercial license conditions must be respected; do not distribute or use this adaptation for commercial advantage. Read [ATTRIBUTION.txt](ATTRIBUTION.txt).
