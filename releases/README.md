# Release artifacts

Place distributable Bedrock packages in this directory before publishing GitHub releases.

## 0.3.0 — Ultra Low test candidate

Expected filename: `LowMine-Ultra-Low-v0.3.0-TEST.mcpack`

- Size: 662,876 bytes.
- SHA-256: `143c508d67ae25046d7ff782cde36190cacabd0d74f4443071afaea4240003c6`

The archive passed static validation: ZIP integrity, 317 JSON files, eight setting-query references, all 29 language files, 94 biome entries, 104 fog definitions and the registered inventory/chest UI override structure. It has not yet been imported or FPS-tested in Minecraft. The binary is delivered separately for the user's test and has not yet been committed here.

Before a public GitHub release:
1. Upload the exact `.mcpack` under this directory.
2. Verify the uploaded SHA-256.
3. Test import, inventory/chest UI, hotbar, touch controls and the single profile in Minecraft.
4. Update the changelog with runtime results and known issues.

## 0.2.0 — Rebrand baseline

Superseded by the single-profile v0.3.0 test candidate.
