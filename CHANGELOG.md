# Changelog

## 0.3.0 — Single Ultra Low profile test candidate
- Removed the PvP subpack and promoted the former Lite profile to the pack root.
- Removed the unused geyser control; the Lite geyser emitters were already hard-disabled.
- Set particle amount to 0% and all seven remaining toggles off by default.
- Audited all 188 included particle definitions: 177 have zero max particles and 11 are gated by the 0% default slider.
- Added desktop and pocket inventory/crafting UI overrides, plus chest and data-driven container overrides.
- Registered all four UI files in `ui/_ui_defs.json`.
- Reduced opacity of shared dialog panel textures, inventory slots, hotbar and touch controls. Selected/pressed states retain more opacity.
- Reduced selected menu textures and the cloud texture.
- Tightened the air fog range to 32–48 in 104 fog definitions (visual-only; no engine culling).
- Removed the unused PBR capability.
- Static validation: 318/318 JSON files valid; 8 active setting IDs resolve; all 29 language files contain required labels; 94 biome entries and 104 fog definitions checked; no missing custom fog IDs.
- Reproducible build check passed: two builds produced byte-identical output.
- No Minecraft runtime or FPS improvement is claimed until tested.

## 0.2.0 — Rebrand and audited test candidate
- Rebranded the pack as LowMine Performance.
- Established LowMine UUIDs and the `lowmine:` namespace.
- Added nine configurable controls and Brazilian Portuguese text.
- Added pack builder, validator and audit documentation.

## 0.1.0 — Initial repository baseline
- Created the LowMine repository and recorded the original attribution/license.
