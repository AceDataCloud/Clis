# HappyHorse by Ace Data Cloud — CLI

A command-line tool for AI video generation using HappyHorse through the AceDataCloud platform.

## Install the published Ace integration

This CLI is maintained by **Ace Data Cloud** for HappyHorse. It is not an official client published by the model owner. The first public release, [happyhorse-cli 2026.10.19.4](https://pypi.org/project/happyhorse-cli/2026.10.19.4/), was published and verified on **2026-10-20 Asia/Shanghai**. The version uses the release workflow's UTC date.

```bash
python -m pip install happyhorse-cli
happyhorse --help
happyhorse models
```

The local help/model-reference commands do not send a generation request or need a key. Check the package's source is [AceDataCloud/HappyHorseCli](https://github.com/AceDataCloud/HappyHorseCli). Canonical source remains [Clis/happyhorse](https://github.com/AceDataCloud/Clis/tree/main/happyhorse); do not edit the mirror directly. The independently published [HappyHorse MCP](https://pypi.org/project/mcp-happyhorse/) is also available for MCP hosts.

[中文安装与密钥指南](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES_zh-CN.md) · [Exact first-release receipt and maintenance sequence](https://github.com/AceDataCloud/Clis/blob/main/happyhorse/PUBLICATION.md)

## API key and free local checks

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Click the copy button beside **API KEY**, marked **1** in the screenshot. Confirm access to the HappyHorse generation and task-query APIs. Check expiration, limits, balance and [current pricing](https://platform.acedata.cloud/models?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen). Store only the raw token in `ACEDATACLOUD_API_TOKEN`, never a prompt or commit. A platform account-management token is different.

```bash
happyhorse --help
happyhorse models
```

These are local reference commands. Generation is charged under your current account terms. Save its task ID; use `happyhorse task <task-id>` or `happyhorse wait <task-id>` for that same task instead of generating again.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

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

### Inherited dimensions for image/video inputs

`image-to-video` inherits the source image's aspect ratio; `--ratio` has no effect.
`video-edit` inherits both source video duration and aspect ratio; `--duration`
and `--ratio` do not override them. Editing is billed for the combined input and
output video durations. Use `--audio-setting origin` to retain the source audio.

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
