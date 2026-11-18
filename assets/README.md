# Branding asset inputs

The v0.2.0 build uses two PNG inputs:

- `lowmine-pack-icon.png`: extract `pack_icon.png` from the built `.mcpack`.
- `lowmine-title.png`: extract `textures/ui/title.png` from the built `.mcpack`.

Place them in this folder with those exact filenames before running `tools/build_pack.py`. The `.mcpack` format is a ZIP archive, so a normal ZIP utility can inspect it.

The builder intentionally takes branding files as explicit inputs; it does not silently reuse or overwrite art from the original author.
