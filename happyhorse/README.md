# HappyHorse by Ace Data Cloud — source CLI

A command-line tool for AI video generation using HappyHorse through the AceDataCloud platform.

## Installation status

The HappyHorse MCP package is publicly available at [mcp-happyhorse](https://pypi.org/project/mcp-happyhorse/) from [AceDataCloud/HappyHorseMCP](https://github.com/AceDataCloud/HappyHorseMCP). This CLI is maintained in the Clis source repository; a PyPI release named `happyhorse-cli` and a standalone HappyHorseCli mirror were **not published when checked on 2026-10-18**. Use the existing published MCP if you need a registry-distributed integration.

For the source CLI, use the pinned source below in an isolated Python environment; it is a local source installation, not a PyPI release. [中文安装与密钥指南](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES_zh-CN.md)

The [publication checklist](https://github.com/AceDataCloud/Clis/blob/main/happyhorse/PUBLICATION.md) records the concrete mirror/package release steps and the temporary publisher-project allowance gate. No new account registration is required.

## Source installation

```bash
python -m pip install "git+https://github.com/AceDataCloud/Clis.git@06c580dbfddd59f9b9bb1c80e86776723fc6cfd3#subdirectory=happyhorse"
```

## API key and free local checks

Register/sign in at [Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_cli_readme_api_key), initialize General application if needed, and copy or create an API Key with HappyHorse generation and task-query access. Check expiration, limits, balance and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=happyhorse_cli_readme_pricing). Store only the raw token in `ACEDATACLOUD_API_TOKEN`, never a prompt or commit. A platform account-management token is different.

```bash
happyhorse --help
happyhorse models
```

These are local reference commands. Generation is charged under your current account terms. Save its task ID; use `happyhorse task <task-id>` or `happyhorse wait <task-id>` for that same task instead of generating again.

## Usage

```bash
# Set API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Generate video from text
happyhorse generate "A horse galloping through a field"

# Generate video from image
happyhorse image-to-video "Animate this scene" --image-url https://example.com/photo.jpg

# Generate video from reference images
happyhorse reference-to-video "Create scene" --image-urls https://example.com/ref.jpg

# Edit a video
happyhorse video-edit "Add dramatic music" --video-url https://example.com/video.mp4

# Check task status
happyhorse task abc123-def456

# Wait for task completion
happyhorse wait abc123 --interval 5

# List available models
happyhorse models

# Show configuration
happyhorse config
```

## Options

### generate

| Option | Default | Description |
|--------|---------|-------------|
| `--model` | `happyhorse-1.1-t2v` | Model to use |
| `--resolution` | `1080P` | Video resolution (720P, 1080P) |
| `--ratio` | `16:9` | Aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4) |
| `--duration` | `5` | Duration in seconds |
| `--watermark` | `False` | Add watermark |
| `--audio-setting` | `auto` | Audio setting (auto, origin) |
| `--seed` | None | Random seed |
| `--callback-url` | None | Webhook callback URL |
| `--async` | `False` | Submit asynchronously |
| `--json` | `False` | Output raw JSON |

## Models

| Model | Type |
|-------|------|
| `happyhorse-1.0-t2v` | Text-to-Video |
| `happyhorse-1.1-t2v` | Text-to-Video (default) |
| `happyhorse-1.0-i2v` | Image-to-Video |
| `happyhorse-1.1-i2v` | Image-to-Video |
| `happyhorse-1.0-r2v` | Reference-to-Video |
| `happyhorse-1.1-r2v` | Reference-to-Video |
| `happyhorse-1.0-video-edit` | Video Edit |

## License

MIT
