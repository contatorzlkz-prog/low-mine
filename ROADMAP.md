# Roadmap

## Phase 1 — Audit and single-profile conversion
- [x] Inspect the supplied Boosted FPS v2.4.1 archive.
- [x] Preserve XiaoCraft attribution and CC BY-NC 3.0 terms.
- [x] Keep the LowMine header/module UUID identity between versions.
- [x] Remove the PvP subpack and flatten the former Lite profile.
- [x] Remove the unused geyser toggle and set optional particle controls to minimum.
- [x] Add translucent inventory/chest/hotbar/touch UI overrides and register the UI files.
- [x] Reduce selected menu/UI textures and the cloud texture.
- [x] Add the v0.3 builder and version-aware static validator.
- [x] Pass static validation: JSON, settings, localization, fog links, UI registrations and archive integrity.

## Phase 2 — Minecraft runtime test (waiting for user test)
- [ ] Import v0.3.0 into the exact Bedrock version in use.
- [ ] Confirm the pack loads and the settings menu shows eight controls.
- [ ] Confirm the player's inventory and crafting screen open correctly.
- [ ] Check small/large chest, Ender Chest, shulker box, barrel and other containers.
- [ ] Check backdrop transparency on desktop and touch/pocket UI.
- [ ] Check hotbar and item slots remain readable/usable in normal, selected and pressed states.
- [ ] Check touch controls remain easy to operate.
- [ ] Inspect fog on plains, forests, caves, water, Nether and End.
- [ ] Check HUD, chat, clouds, particles, XP collection, multiplayer and world reload.
- [ ] Record exact Bedrock version, content-log messages, missing textures and UI regressions.

## Phase 3 — Controlled performance comparison
- [ ] Measure vanilla without LowMine.
- [ ] Measure v0.3.0 in the same world/scene.
- [ ] Keep device, resolution, render distance, simulation distance and scene constant.
- [ ] Record average FPS and frame-time stability, not just a single FPS reading.
- [ ] Compare memory/RAM behavior where the platform exposes it.
- [ ] Do not treat smaller ZIP size or PNG pixel count as a measured FPS result.

## Phase 4 — Further safe resource-pack optimization
- [ ] Inspect any remaining high-resolution textures before resizing them.
- [ ] Review remaining entity/particle overrides for redundancy.
- [ ] Keep readability and item recognition as explicit constraints.
- [ ] Make one change per build so regressions can be identified.

## Engine-level features outside resource-pack scope
- RenderDragon frustum/occlusion/chunk culling cannot be replaced by a resource pack.
- Rust can be used for separate tools or supported server software, not injected as the Bedrock client renderer through a .mcpack.
- Revisit these only if official Bedrock APIs expose an appropriate renderer/visibility hook.
