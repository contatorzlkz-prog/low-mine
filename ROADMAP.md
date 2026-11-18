# Roadmap

## Completed — v0.3.2 import repair and Ultra Low profile
- [x] Preserve original XiaoCraft attribution and CC BY-NC 3.0 terms.
- [x] Keep one profile; remove PvP/subpack content.
- [x] Correct manifest v3 versions to strings.
- [x] Remove experimental custom pack settings.
- [x] Hard-disable all 188 particle definitions included in LowMine.
- [x] Hide XP orb rendering without changing XP awarding/collection.
- [x] Keep desktop/pocket inventory and chest/container UI overrides.
- [x] Validate all 318 JSON files, fog references, UI registrations and ZIP integrity.

## Next — Minecraft runtime test
- [ ] Import v0.3.2 and confirm the pack name, UUID and version appear correctly.
- [ ] Open inventory, crafting, chests, Ender Chest, shulker, barrel and pocket UI.
- [ ] Confirm hotbar slot, touch controls, item icons and pressed states remain usable.
- [ ] Test the world, fog, clouds, effects, XP and multiplayer.
- [ ] Record exact Bedrock version, content-log errors and screenshots.

## Performance comparison
- [ ] Compare vanilla and LowMine in the same world, scene, resolution and render/simulation distances.
- [ ] Record average FPS and frame-time stability, not a single FPS counter reading.
- [ ] Compare memory where the platform exposes it.
- [ ] Change one optimization at a time and keep a known-good build.

## Engine-level ideas outside resource packs
- Frustum/occlusion/chunk culling is owned by the Bedrock client renderer.
- Resource-pack fog does not discard geometry or guarantee less CPU/GPU work.
- Block Culling is limited to covered faces of custom block geometry.
- Rust can support separate asset/build/analysis tools, not replace RenderDragon via a .mcpack.
