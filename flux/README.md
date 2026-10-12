# Flux CLI

A command-line tool for AI image generation and editing using [Flux](https://blackforestlabs.ai/) through the [AceDataCloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_cli_readme_platform) platform.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Features

- **Text-to-Image Generation** — Generate images from text prompts with multiple Flux models
- **Image Editing** — Edit existing images using text descriptions (kontext models)
- **Task Management** — Query status, batch check, and poll for completion
- **Multiple Models** — flux-dev, flux-pro, flux-kontext-pro, flux-kontext-max, flux-2-flex, flux-2-pro, flux-2-max, flux-2-klein
- **Rich Output** — Beautiful terminal formatting with `--json` for scripting

## Installation

```bash
pip install flux-pro-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Generate an image
flux generate "A majestic mountain landscape at golden hour, photorealistic"

# Generate with a specific model
flux generate "Cyberpunk city with neon lights" -m flux-2-pro

# Generate with aspect ratio (ultra/kontext models)
flux generate "Minimalist logo of a phoenix" -m flux-2-max -s 16:9

# Generate multiple images
flux generate "A red car" --count 2

# Edit an existing image
flux edit "Add sunglasses to the person" --image-url https://example.com/photo.jpg

# Edit with max context model
flux edit "Change background to sunset beach" --image-url https://example.com/img.png -m flux-kontext-max

# Check task status
flux task abc123-def456

# Wait for task completion
flux wait abc123 --interval 5 --timeout 300

# Batch check multiple tasks
flux tasks task-1 task-2 task-3
```

## Commands

| Command | Description |
|---------|-------------|
| `generate` | Generate an image from a text prompt |
| `edit` | Edit an existing image with a text prompt |
| `task` | Query a single task status |
| `tasks` | Query multiple tasks at once |
| `wait` | Wait for a task to complete |
| `models` | List available Flux models |
| `aspect-ratios` | List available aspect ratios |
| `config` | Show current configuration |

## Models

| Model | Type | Size Input | Notes |
|-------|------|-----------|-------|
| `flux-dev` | Dev | Pixels | Fast, good balance (default) |
| `flux-pro` | Pro | Pixels | Higher quality |
| `flux-kontext-pro` | Kontext | Aspect ratio | Best for editing/style transfer |
| `flux-kontext-max` | Kontext | Aspect ratio | Max context for complex edits |
| `flux-2-flex` | Flux 2 | Pixels | Fast Flux 2 generation |
| `flux-2-pro` | Flux 2 | Pixels | Higher quality Flux 2 generation |
| `flux-2-max` | Flux 2 | Pixels | Maximum quality Flux 2 generation |
| `flux-2-klein` | Flux 2 | Pixels | Compact Flux 2 generation |

## JSON Output

All commands support `--json` for machine-readable output:

```bash
flux generate "A red car" --json | jq '.task_id'
flux task abc123 --json | jq '.data[0].image_url'
```

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API authentication token | (required) |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `FLUX_REQUEST_TIMEOUT` | Request timeout in seconds | `1800` |

You can also use a `.env` file or pass `--token` directly.

## Docker

```bash
docker compose run flux-cli generate "A beautiful sunset"
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[all]"

# Run tests
pytest

# Run linter
ruff check .
ruff format --check .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Links

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_cli_readme_platform)
- [API Documentation](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=flux_cli_readme_documents)
- [Flux by Black Forest Labs](https://blackforestlabs.ai/)

## FLUX 3 video

Save a JSON request such as `{"action":"generate","mode":"t2v","prompt":"Waves at sunset","duration":5,"generate_audio":false}` in `request.json`, then run `flux video --request-file request.json`. The request is validated before submission. Use `i2v` with `keyframes`, `v2v` with `start_video`, or `draft_enhance` with an owned platform `draft_task_id`. Draft availability is temporary.

Video generation uses `POST /flux/videos` with `action=generate` (default) and `mode=t2v/i2v/v2v/draft_enhance`. The `flux video --request-file request.json` command validates the generation mode and outputs JSON. Requests are asynchronous by default; use `flux task`/`flux wait` for final delivery. Set `async=false` to wait synchronously.
