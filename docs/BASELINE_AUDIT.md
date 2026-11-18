# Baseline audit — Boosted FPS v2.4.1

## Package facts
- Supplied input: `Boosted FPS v2.4.1.mcpack`
- Original archive entries: 1,135
- Adapted archive entries: 1,136 (includes `ATTRIBUTION.txt`)
- File counts in the original package:
  - 605 PNG images
  - 487 JSON files
  - 29 language files
  - 11 TGA images
  - 2 UI files
  - 1 material file
- Base biome entries: 94
- `subpacks/fps/`: 288 files
- `subpacks/pvp_fps/`: 106 files
- Configurable controls: 9 (8 toggles, 1 slider)
- Manifest minimum engine version: `1.26.40`

## Static checks
- JSON files checked: 487
- Invalid JSON files found: 0
- `manifest.json` is at the archive root.
- `subpacks/fps/biomes_client.json` exists.
- Both declared subpack folders exist.
- New header and module UUIDs are distinct from the source package.

## Important discrepancy
The imported pack description says `89-biome fog coverage`, but the actual base `biomes_client.json` contains **94 biome entries**. LowMine records the measured file count and does not assume that count alone proves every biome has correct in-game fog behavior.

## What this audit does not prove
Static JSON validation does not prove that Minecraft will load the pack, that every setting works, or that FPS improves. Those require in-game compatibility and benchmark tests.

## First adapted build
- Filename: `LowMine-Performance-v0.1.0.mcpack`
- Output size: 1,154,514 bytes
- SHA-256: `2fbab50c33115b5f1e884b8ce076a7731c91f0586cfde21f663522c73c7b996a`
- Source archive SHA-256: `9f1e49cad7eae648b0e8bd76e7453fbd1bb633b33aeb6c3128eeea8472886bea`

The generated package passed ZIP integrity testing and all included JSON files parsed successfully. No Minecraft runtime test has been performed.
