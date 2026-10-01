# Maestro CLI

CLI tool for [Maestro AI Video Studio](https://platform.acedata.cloud/documents/maestro) via AceDataCloud API.

## Installation

```bash
pip install maestro-cli
```

## Usage

```bash
maestro create "Explain what a vector database is in 20 seconds"
maestro create "Product demo" --aspect 16:9
maestro create "Continue the story" --action extend --ref-task-id <task-id>
maestro task <task-id>
maestro wait <task-id>
```

## Video options

Videos render at 1080p/30fps. Set a duration from 5 to 300 seconds and provide up to four output languages or 20 reference media URLs.

For a restrained product launch:

```bash
maestro create "Launch our product with original UI and a clear CTA" \
  --style apple-launch --aspect 16:9 --duration 30 --audio-mode music \
  --website-url https://studio.acedata.cloud/maestro \
  --assets-file assets.json --brand-file brand.json
```

`assets.json` is an array of `{ "id": "hero", "role": "ui_screenshot", "url": "https://your-public-host/ui.png" }`.
Roles also include logo, product_image, product_video, style_reference, music and reference.
Assets and `--file-url` entries together support at most 20 inputs. A style reference guides
appearance and is not used as your product. `brand.json` accepts name, #RRGGBB colors
(background/foreground/accent), `font_set: "inter-noto-sc"`, and CTA text/URL overrides.

`--audio-mode` accepts auto/narration/music/silent. Music-only and silent cannot pin `--voice`.
`apple-launch` supports auto/narrated; `glass` remains a separate Liquid Glass style.
Unspecified format/style/audio/brand/media inputs inherit on an iteration. An assets JSON `[]`
clears labeled assets, a brand JSON `null` clears overrides, and `--website-url ""` clears the
website source. An explicit brand object replaces the original overrides. Website capture uses public
pages without login and may fail for inaccessible or protected sites.
