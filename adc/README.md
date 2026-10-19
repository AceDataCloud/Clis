# AceDataCloud CLI

Unified command-line interface for all AceDataCloud AI services — images, videos, music, and search.

## Get your Ace Data Cloud API key

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=adc_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=adc_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

## Installation

```bash
pip install acedatacloud-cli
```

## Find a service by name

```bash
adc packages suno
adc packages "gpt image" --json
adc packages "nano banana"
```

This local directory shows Ace-maintained service packages and their observed publication state. It never installs a package or submits a request. HappyHorse's standalone CLI is published; its directory entry carries the exact first-release version/hash/install receipt. The independent MCP entry remains available. See the [service-name directory](https://github.com/AceDataCloud/Clis/blob/main/docs/SERVICE_PACKAGES.md) for publisher checks and first-use steps.

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

Get your API token at [platform.acedata.cloud](https://platform.acedata.cloud?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=adc_cli_readme_platform).

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
