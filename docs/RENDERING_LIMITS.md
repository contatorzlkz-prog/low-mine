# Bedrock rendering: what LowMine can and cannot change

This document separates resource-pack changes from client-engine behavior.

## Developer guidance that directly applies to LowMine

Microsoft's current performance guide says:
- Textures are generally loaded into memory uncompressed when a world loads.
- A 1024×1024 texture can use 16 times the memory of a 256×256 texture.
- Reduce wasted texture space and avoid loading unnecessary textures.
- Texture handles carry overhead. Block textures may be packed into atlases, so PNG file count is not equal to GPU texture handle count.
- Too many resource files add overhead; Microsoft recommends staying below 800 texture handles for add-ons.
- Complex/high-volume particles can hurt performance, and lower-end devices should be tested early.

Source: [Improving performance and resource usage](https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable)

The official [Texture Budgets](https://learn.microsoft.com/en-us/minecraft/creator/documents/texturebudgets?view=minecraft-bedrock-stable) guide estimates uncompressed texture memory from total texels × 4 bytes and lists separate budgets for add-ons, resource packs and worlds. These are budget estimates, not direct FPS measurements.

LowMine follows the measurable parts of this advice: it reduces selected high-resolution UI images and sets every included LowMine particle emitter to zero. Most block/item sprites were not blindly blurred or resized; item readability matters, and their pixel cost is not automatically the main bottleneck.

## What a resource pack can affect

A Bedrock resource pack can replace visual assets and resource definitions exposed by the game:
- Particle definitions included in or overridden by the pack.
- Texture dimensions, texture choices, UI images and alpha/transparency.
- Resource-pack fog definitions.
- Some custom model and render-controller definitions.

These changes can reduce the amount of pack-owned visual data or effects. Real FPS impact depends on scene/device/game version and must be measured.

## What fog does not do

Fog changes visual distance blending. A fog range of 32–48 blocks makes terrain disappear sooner, but does not instruct RenderDragon to stop processing geometry beyond the fog.

It does not:
- Hide only objects behind the camera.
- Guarantee that underground or occluded blocks stop being processed.
- Replace chunk loading, frustum culling or occlusion culling.

## Block Culling

Bedrock's Block Culling targets faces of custom block geometry that are covered by adjacent blocks. It is not a global switch for all vanilla terrain, entities or everything behind the player.

Reference: [Bedrock Wiki — Block Culling](https://wiki.bedrock.dev/blocks/block-culling).

## RenderDragon and Rust

RenderDragon is the Bedrock client renderer. A `.mcpack` is a resource package, not a native client plug-in. It cannot inject Rust into the game's renderer or replace RenderDragon.

Rust can be useful for separate LowMine tools: package inspection, image/atlas analysis, build automation, duplicate-file detection and benchmark-log analysis. It does not turn into client-side culling through a resource pack.

## Safe engine-side settings

Use the game's own video settings to lower render distance; that is the supported way to request fewer distant chunks. Simulation distance is separate and controls gameplay simulation, not texture dimensions or fog.

## LowMine's optimization method

1. Keep every included particle definition cheap or disabled if it is not needed.
2. Reduce oversized textures and unnecessary unique texture files.
3. Remove duplicate subpack files and unused overrides.
4. Keep inventory/hotbar controls readable and clickable after alpha changes.
5. Benchmark vanilla against LowMine in the same world, camera position, device, resolution, render distance and simulation distance.
6. Compare average FPS and frame-time stability; do not claim a gain from ZIP size or a texture-pixel estimate alone.

The v0.3.2 candidate passed static checks only. Import, UI behavior and performance still require in-game verification.
