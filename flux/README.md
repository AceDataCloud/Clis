# Flux CLI

A command-line tool for AI image generation and editing using [Flux](https://blackforestlabs.ai/) through the [AceDataCloud](https://platform.acedata.cloud) platform.

## Features

- **Text-to-Image Generation** — Generate images from text prompts with multiple Flux models
- **Image Editing** — Edit existing images using text descriptions (kontext models)
- **Task Management** — Query status, batch check, and poll for completion
- **Multiple Models** — flux-dev, flux-pro, flux-kontext-pro, flux-kontext-max, flux-2-flex, flux-2-pro, flux-2-max
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

- [AceDataCloud Platform](https://platform.acedata.cloud)
- [API Documentation](https://docs.acedata.cloud)
- [Flux by Black Forest Labs](https://blackforestlabs.ai/)
