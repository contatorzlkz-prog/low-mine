# Changelog

## 0.3.2 — import fix and static low-particle profile
- Fixed the import failure caused by using version arrays for manifest v3. Header and module versions are now SemVer strings.
- Removed manifest custom pack settings; the ultra-low profile no longer depends on experimental settings queries or a settings screen.
- Set all 188 included particle definitions to zero spawn count / maximum (177 max-particle caps and 11 instant-spawn counts).
- Kept XP-orb rendering hidden without altering XP collection.
- Preserved single flattened profile, inventory/chest UI transparency, hotbar/touch edits and short visual fog.
- Static checks passed: 925 archive entries, 318 valid JSON files, 94 biome entries, 104 fog definitions and all UI overrides registered.
- No in-game FPS result is claimed until benchmarked.

## 0.3.0 — failed import test candidate (superseded)
- Removed PvP and added UI/texture changes.
- Import failed because manifest v3 version values were emitted as arrays; do not use this package.

## 0.2.0 — rebrand baseline
- Established LowMine branding, identifiers and tooling.
