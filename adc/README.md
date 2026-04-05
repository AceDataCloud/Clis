# AceDataCloud CLI

Unified command-line interface for all AceDataCloud AI services — images, videos, music, and search.

## Installation

```bash
pip install acedatacloud-cli
```

## Quick Start

```bash
# Save your API token
adc auth login

# Generate an image
adc image "A sunset over mountains, photorealistic"

# Generate a video
adc video "A cinematic ocean scene"

# Generate music
adc music "Upbeat electronic dance track"

# Search the web
adc search "artificial intelligence"

# Check task status
adc task abc123 -s flux

# Wait for completion
adc wait abc123 -s flux
```

## Configuration

Get your API token at [platform.acedata.cloud](https://platform.acedata.cloud).

```bash
# Option 1: Login command (saves to ~/.config/adc/config)
adc auth login

# Option 2: Environment variable
export ACEDATACLOUD_API_TOKEN=your_token

# Option 3: Per-command flag
adc --token your_token image "A sunset"
```

## Commands

### Image Generation

```bash
adc image "A sunset over mountains"                        # Flux (default)
adc image "Cyberpunk city" --service midjourney             # Midjourney
adc image "Logo design" --service seedream                  # Seedream
adc image "Add sunglasses" --image-url https://...         # Edit with Flux
adc image "A landscape" -m flux-pro-1.1-ultra -s 16:9     # Custom model & size
```

### Video Generation

```bash
adc video "A cinematic sunset"                              # Luma (default)
adc video "A rocket launching" --service sora               # Sora
adc video "Clouds moving" --service veo                     # Veo
adc video "Dance scene" --service seedance                  # Seedance
adc video "Cat playing" --loop -a 16:9                      # Loop + aspect ratio
```

### Music Generation

```bash
adc music "An upbeat electronic dance track"
adc music "Calm piano jazz" --instrumental
```

### Web Search

```bash
adc search "artificial intelligence"
adc search "tech news" -t news --time-range qdr:d
adc search "sunset photos" -t images -c us
```

### Task Management

```bash
adc task abc123 -s flux          # Check task status
adc task def456 -s luma --json   # JSON output
adc wait abc123 -s flux          # Wait for completion
adc wait def456 -s suno --interval 10 --timeout 300
```

### Info & Auth

```bash
adc services                     # List all available services
adc config                       # Show configuration
adc auth login                   # Save API token
adc auth status                  # Check auth status
```

## JSON Output

All commands support `--json` for machine-readable output:

```bash
adc image "A sunset" --json | jq '.task_id'
adc search "test query" --json | jq '.organic[].title'
```

## Supported Services

| Service      | Type   | Command                    |
| ------------ | ------ | -------------------------- |
| Flux         | Image  | `adc image --service flux` |
| Midjourney   | Image  | `adc image --service midjourney` |
| Seedream     | Image  | `adc image --service seedream` |
| NanoBanana   | Image  | `adc image --service nanobanana` |
| Suno         | Music  | `adc music`                |
| Luma         | Video  | `adc video --service luma` |
| Sora         | Video  | `adc video --service sora` |
| Veo          | Video  | `adc video --service veo`  |
| Seedance     | Video  | `adc video --service seedance` |
| SERP         | Search | `adc search`               |

## Development

```bash
# Install with dev dependencies
pip install -e ".[all]"

# Run tests
pytest

# Lint
ruff check .
ruff format --check .
```

## License

MIT
