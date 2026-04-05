# Wan CLI

[![PyPI version](https://img.shields.io/pypi/v/wan-cli.svg)](https://pypi.org/project/wan-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/wan-cli.svg)](https://pypi.org/project/wan-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool for AI video generation using [Tongyi Wansiang](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI videos directly from your terminal — no MCP client required.

## Features

- **Video Generation** — Generate videos from text prompts with multiple models
- **Image-to-Video** — Create videos from reference images
- **Multiple Models** — wan2.6-t2v, wan2.6-i2v, wan2.6-i2v-flash, wan2.6-r2v
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Wan API page
3. Click "Acquire" to get your token

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
--duration TEXT               Duration in seconds: 5, 10, 15
--shot-type TEXT              Shot type: single, multi
--audio/--no-audio            Whether the video has sound
--prompt-extend/--no-prompt-extend  Enable prompt intelligent rewriting
```

## Available Models

| Model | Type | Notes |
|-------|------|-------|
| `wan2.6-t2v` | Text-to-Video | Text-to-video generation (default) |
| `wan2.6-i2v` | Image-to-Video | Image-to-video generation |
| `wan2.6-i2v-flash` | Image-to-Video Flash | Fast image-to-video generation |
| `wan2.6-r2v` | Reference-to-Video | Reference video-to-video generation |


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
