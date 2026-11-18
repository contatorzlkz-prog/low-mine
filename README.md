# LowMine Performance

**LowMine** is a Minecraft Bedrock performance resource-pack project focused on low-end devices. The initial baseline is an explicitly credited adaptation of **Boosted FPS (Optimized Performance) v2.4.1 by XiaoCraft**.

> This repository baseline does not claim a measured FPS increase. Runtime testing and repeatable benchmarks are required before calling any change an optimization.

## Current baseline

- Minecraft Bedrock resource pack (`.mcpack`).
- Minimum engine version carried over from the source manifest: `1.26.40`.
- Two subpacks: **LowMine Lite** (adapted from `Pure FPS`) and **LowMine PvP** (adapted from `PvP + FPS`).
- Nine configurable controls in the manifest: eight toggles and one slider.
- 94 biome entries in the base biome configuration.
- 1,136 files in the adapted package archive (including the attribution notice).

## Package

The first adapted build is named `LowMine-Performance-v0.1.0.mcpack`. It is packaged with the resource-pack manifest at the archive root and includes an `ATTRIBUTION.txt` notice. The binary package is supplied separately from this initial documentation commit; it still needs to be attached to the repository as a release asset or committed under `releases/`.

To import a build, open the `.mcpack` file with Minecraft Bedrock, then activate it under Global Resources or a world's Resource Packs settings. Select the desired subpack in the pack settings.

## Development status

| Area | Status |
|---|---|
| Repository setup and attribution | Complete |
| Baseline package identity and UI rename | Complete in local build |
| Structural JSON validation | Complete |
| Compatibility testing in Bedrock | Pending |
| Controlled FPS / frame-time benchmarks | Pending |
| Actual optimization changes | Pending |

See [the baseline audit](docs/BASELINE_AUDIT.md), [roadmap](ROADMAP.md), and [changelog](CHANGELOG.md).

## Attribution and license

Original work: **Boosted FPS (Optimized Performance) v2.4.1**, by **XiaoCraft**.

Source: https://www.curseforge.com/minecraft-bedrock/texture-packs/boosted-fps-optimized-performance

The original work is listed under **Creative Commons Attribution-NonCommercial 3.0 Unported (CC BY-NC 3.0)**: https://creativecommons.org/licenses/by-nc/3.0/. This adaptation identifies its changes, retains attribution, and must stay within the original non-commercial license terms. It is not endorsed by or affiliated with XiaoCraft. Read [ATTRIBUTION.txt](ATTRIBUTION.txt) before redistributing.

## Project principles

1. Preserve Bedrock compatibility before changing assets.
2. Measure frame time and stability instead of assuming that removing visual effects always improves FPS.
3. Keep changes modular and reversible, with separate profiles where useful.
4. Avoid unnecessary resource overrides and preserve the vanilla visual identity where possible.
5. Document every optimization, its trade-offs, and the game versions / devices tested.
