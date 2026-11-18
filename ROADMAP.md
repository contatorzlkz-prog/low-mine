# Roadmap

## Phase 1 — Baseline and safety
- [x] Import and inspect the supplied Boosted FPS v2.4.1 package.
- [x] Preserve original author attribution and identify the CC BY-NC 3.0 terms.
- [x] Give the adaptation its own manifest/module UUIDs and LowMine branding.
- [x] Validate every JSON file structurally.
- [ ] Import into Minecraft Bedrock and verify both subpacks load.

## Phase 2 — Reproducible performance tests
- [ ] Establish a clean vanilla baseline and a source-pack baseline.
- [ ] Use the same world, render distance, simulation distance, device, and scene for each run.
- [ ] Record average FPS plus frame-time stability (not FPS alone).
- [ ] Test low-memory devices separately from stronger devices.

## Phase 3 — Targeted optimizations
- [ ] Audit particle definitions and their spawn / lifetime costs.
- [ ] Audit entity render overrides and verify that visual hiding does not break gameplay feedback.
- [ ] Audit fog and biome overrides for redundant files and compatibility risks.
- [ ] Audit UI overrides for unnecessary texture or screen replacements.
- [ ] Compare Lite and PvP variants for file duplication and memory footprint.
- [ ] Make one isolated change per commit and benchmark it against the baseline.

## Phase 4 — Release quality
- [ ] Test supported Bedrock versions on Android, Windows, and any other target actually available.
- [ ] Verify pack import, settings, world loading, multiplayer, and coexistence with common resource packs.
- [ ] Publish a changelog with measured results and known limitations.
