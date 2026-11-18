# Bedrock rendering: what LowMine can and cannot change

This document separates resource-pack adjustments from client-engine behavior.

## What a resource pack can affect

A Bedrock resource pack can replace visual assets and resource definitions that the game exposes:
- Particle definitions and custom particle amounts, where the pack owns or overrides those definitions.
- Texture dimensions, texture choices, UI images and alpha/transparency.
- Resource-pack fog definitions, which change what the player sees at a distance.
- Some model and render-controller definitions for assets included in the pack.

These changes may reduce asset memory use or the number of visual effects generated. Their actual FPS impact depends on the device, scene and game version and must be measured.

Microsoft's performance guidance recommends controlling texture sizes, minimizing unnecessary texture assets and keeping particle systems simple. Texture resolution affects memory requirements; it does not automatically prove lower CPU/GPU time in every scene:
https://learn.microsoft.com/en-us/minecraft/creator/documents/practices/improvingperformanceandresourceusage?view=minecraft-bedrock-stable

## What fog does not do

Resource-pack fog is a visual distance effect. It blends distant scene content into fog colors. A fog range of 32–48 blocks can make the visible world look much shorter, but it does not provide a general instruction to stop the engine from processing everything beyond that visual range.

Fog is not a camera-facing culling mask:
- It does not selectively hide only objects behind the player.
- It does not guarantee blocks under the terrain stop being processed.
- It does not replace chunk loading or the game's visibility pipeline.

LowMine's current short fog is intentionally a visual setting. It is not advertised as a CPU/GPU culling implementation.

## What Block Culling means in Bedrock

Bedrock's Block Culling feature concerns faces of custom block geometry that are covered by adjacent blocks. It can remove hidden faces from those custom models. It is not a universal switch for frustum culling, occlusion culling, all vanilla terrain, entities or arbitrary content behind the camera.

Reference: https://wiki.bedrock.dev/blocks/block-culling

## RenderDragon and Rust

RenderDragon is the rendering engine used by modern Minecraft Bedrock clients. A `.mcpack` is a resource package; it is not a native engine plug-in or executable patch. Resource-pack files cannot inject Rust code into the client renderer or replace RenderDragon.

Rust could be used for separate tooling (for example, a pack inspector, asset optimizer or benchmark log analyzer) or compatible server-side software. It cannot be used through a normal Bedrock resource pack to take over client rendering.

## Actual engine controls available to players

The game's own video settings control render distance and simulation distance. Lowering render distance is the supported way to ask the client to draw fewer distant chunks; a resource pack cannot reliably override that engine setting. Simulation distance changes how far gameplay simulation is active and is distinct from a resource pack texture or fog.

## LowMine's safe optimization scope

1. Keep particle emitters conservative and disable pack-owned visual effects the player does not need.
2. Reduce excessive texture dimensions while preserving item/block readability.
3. Remove duplicate subpack assets and unnecessary overrides.
4. Reduce UI texture opacity/complexity without removing input regions or selection feedback.
5. Measure vanilla versus LowMine in the same world, scene and settings, using average FPS and frame-time stability.

The current v0.3.0 test candidate is a resource-pack optimization only. Runtime import, UI behavior and any performance effect still require testing in Minecraft.
