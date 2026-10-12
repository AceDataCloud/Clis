# Wan CLI

[![PyPI version](https://img.shields.io/pypi/v/wan-cli.svg)](https://pypi.org/project/wan-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/wan-cli.svg)](https://pypi.org/project/wan-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool for AI video generation using [Tongyi Wansiang](https://platform.acedata.cloud/?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_cli_readme_platform) through the [AceDataCloud API](https://platform.acedata.cloud/?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_cli_readme_platform).

Generate AI videos directly from your terminal — no MCP client required.

## Features

- **Video Generation** — Generate videos from text prompts with multiple models
- **Image-to-Video** — Create videos from reference images
- **Multiple Models** — wan2.6-t2v, wan2.6-i2v, wan2.6-i2v-flash, wan2.6-r2v, wan3.0-video
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_cli_readme_api_key). Sign in, or register an account first.
2. Find **General application**. If it has not been created, choose **Initialize General Application**. A general key can use the services available to your account; a dedicated application's key is limited to its service. Check the required service/model access and [current pricing](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=wan_cli_readme_pricing).
3. Copy the **API Key** from the application card, or open **Keys / Manage Keys → Create** to create a separate key for this integration. Give it a recognizable name so you can revoke or rotate it independently.
4. When creating a key, review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Enable only the restrictions you need, allow the operations you will call, then click **Create** and copy the token from the key list. Task lookup does not grant permission to submit a generation. Confirm the application's balance can cover your first request; any trial allowance is whatever your account currently displays.
5. Copy only the token value, without quotation marks, spaces, or `Bearer `. An API Key / API Token field expects this raw value; only a manually configured HTTP `Authorization` header needs the `Bearer ` prefix. A `platform-...` account-management token cannot replace a generation API key.

![Copy an application API key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![Create a separately named key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

Save the key in the client's credential store or the environment variable shown below. Never put it in a prompt, shared workflow, screenshot, or Git commit. If authentication fails, check the full copied value, application/service access, expiration, usage limit, and balance before creating another key.

### 2. Install

```bash
# Install with pip
pip install wan-cli

# Or with uv (recommended)
uv pip install wan-cli

# Or from source
git clone https://github.com/AceDataCloud/WanCli.git
cd WanCli
pip install -e .
```

### 3. Configure

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token_here

# Or use .env file
cp .env.example .env
# Edit .env with your token
```

### 4. Use

```bash
# Generate a video from text
wan generate "Astronauts shuttle from space to volcano"

# Generate from reference image
wan image-to-video "Animate this scene" -i https://example.com/photo.jpg

# Check task status
wan task <task-id>

# Wait for completion
wan wait <task-id> --interval 5

# List available models
wan models
```

## Commands

| Command | Description |
|---------|-------------|
| `wan generate <prompt>` | Generate a video from a text prompt |
| `wan image-to-video <prompt> -i <url>` | Generate a video from a reference image |
| `wan task <task_id>` | Query a single task status |
| `wan tasks <id1> <id2>...` | Query multiple tasks at once |
| `wan wait <task_id>` | Wait for task completion with polling |
| `wan models` | List available Wan models |
| `wan resolutions` | List available resolutions |
| `wan config` | Show current configuration |


## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json                        Output raw JSON (for piping/scripting)
--model TEXT                  Wan model version (default: wan2.6-t2v)
--resolution TEXT             Output resolution: 480P, 720P, 1080P
--duration TEXT               Duration in seconds: 2-30, or -1 for auto
--shot-type TEXT              Shot type: single, multi
--audio/--no-audio            Whether the video has sound
--prompt-extend/--no-prompt-extend  Enable prompt intelligent rewriting
--media TYPE=URL              Media item (repeatable)
--ratio TEXT                  Aspect ratio: adaptive, 16:9, 4:3, 1:1, 3:4, 9:16
--seed INTEGER                Random seed (0-2147483647)
--watermark/--no-watermark    Whether to add a watermark
```

## Available Models

| Model | Type | Notes |
|-------|------|-------|
| `wan2.6-t2v` | Text-to-Video | Text-to-video generation (default) |
| `wan2.6-i2v` | Image-to-Video | Image-to-video generation |
| `wan2.6-i2v-flash` | Image-to-Video Flash | Fast image-to-video generation |
| `wan2.6-r2v` | Reference-to-Video | Reference video-to-video generation |
| `wan3.0-video` | Video Generation | Wan 3.0 video generation |


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `WAN_DEFAULT_MODEL` | Default model | `wan2.6-t2v` |
| `WAN_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/WanCli.git
cd WanCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=wan_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy wan_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/wan-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/wan-cli generate "Astronauts shuttle from space to volcano"
```

## Project Structure

```
WanCli/
├── wan_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m wan_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for Wan API
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── output.py          # Rich terminal formatting
│   └── commands/              # CLI command groups
│       ├── video.py           # Video generation commands
│       ├── task.py            # Task management commands
│       └── info.py            # Info & utility commands
├── tests/                     # Test suite
├── Dockerfile                 # Container image
├── deploy/                    # Kubernetes deployment configs
├── .env.example               # Environment template
├── pyproject.toml             # Project configuration
└── README.md
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
