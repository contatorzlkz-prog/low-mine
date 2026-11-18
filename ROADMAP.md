# Roadmap

## Phase 1 — Audit and safe rebrand
- [x] Inspect the supplied Boosted FPS v2.4.1 archive and inventory its structure.
- [x] Preserve XiaoCraft attribution and the original CC BY-NC 3.0 terms.
- [x] Give the adaptation its own stable manifest/module UUIDs.
- [x] Rename internal settings and custom fog identifiers to the LowMine namespace.
- [x] Add LowMine pack art, title art, subpack names and localized labels.
- [x] Validate all 487 JSON files, nine setting references, 29 language files and biome fog links.
- [x] Add a reproducible builder and static validator.

## Phase 2 — Minecraft runtime test (waiting for user test)
- [ ] Import v0.2.0 into Bedrock and verify it appears without warnings.
- [ ] Confirm the settings screen opens and all nine controls work.
- [ ] Test Lite and PvP separately.
- [ ] Check fog on several biomes, water, Nether and End.
- [ ] Check potion particles, geysers, sulfur, cauldrons, arrow trails and XP-orb visibility.
- [ ] Check HUD, chat, title screen, multiplayer and world reload.
- [ ] Record Bedrock version and content-log errors.

## Phase 3 — Performance baseline
- [ ] Measure vanilla with the same world and scene.
- [ ] Measure the original source pack and LowMine v0.2.0 under the same conditions.
- [ ] Record average FPS and frame-time stability, not FPS alone.
- [ ] Keep device, render distance, simulation distance, resolution and scene identical.
- [ ] Separate low-memory devices from stronger devices.

## Phase 4 — Targeted optimization
- [ ] Review high-cost particle spawn rates and particle lifetimes.
- [ ] Check whether entity overrides can be reduced without removing useful gameplay feedback.
- [ ] Review fog overrides only after visual compatibility testing.
- [ ] Review UI overrides and duplicated assets.
- [ ] Compare Lite and PvP memory footprint and file overlap.
- [ ] Make one isolated change per commit and benchmark it against v0.2.0.

## Phase 5 — Release quality
- [ ] Test on the Bedrock versions and devices actually supported.
- [ ] Publish only verified compatibility statements and measured results.
- [ ] Keep a changelog and known-issues list for every release.
