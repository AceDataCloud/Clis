# Sora CLI

[![PyPI version](https://img.shields.io/pypi/v/sora-pro-cli.svg)](https://pypi.org/project/sora-pro-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/sora-pro-cli.svg)](https://pypi.org/project/sora-pro-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/SoraCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/SoraCli/actions/workflows/ci.yaml)

A command-line tool for AI video generation using [Sora](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI videos directly from your terminal — no MCP client required.

## Features

- **Video Generation** — Generate videos from text prompts with multiple models
- **Image-to-Video** — Create videos from reference images
- **Multiple Models** — sora-2, sora-2-pro
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Sora API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install sora-pro-cli

# Or with uv (recommended)
uv pip install sora-pro-cli

# Or from source
git clone https://github.com/AceDataCloud/SoraCli.git
cd SoraCli
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
# Generate a video
sora generate "A test video"

# Generate from reference image
sora image-to-video "Animate this scene" -i https://example.com/photo.jpg

# Check task status
sora task <task-id>

# Wait for completion
sora wait <task-id> --interval 5

# List available models
sora models
```

## Commands

| Command | Description |
|---------|-------------|
| `sora generate <prompt>` | Generate a video from a text prompt |
| `sora image-to-video <prompt> -i <url>` | Generate a video from reference image(s) |
| `sora task <task_id>` | Query a single task status |
| `sora tasks <id1> <id2>...` | Query multiple tasks at once |
| `sora wait <task_id>` | Wait for task completion with polling |
| `sora models` | List available Sora models |
| `sora config` | Show current configuration |
| `sora orientations` | List available orientations |
| `sora sizes` | List available video sizes |


## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--model TEXT    Sora model version (default: sora-2)
--duration CHOICE  Duration in seconds: 4, 8, 10, 12, 15, 25 (default: 15)
--size TEXT     Video size (default: small). Use pixel resolutions for --version 2.0
--version TEXT  API version: 1.0 or 2.0 (default: 1.0)
```

## Available Models

| Model | Version | Notes |
|-------|---------|-------|
| `sora-2` | Standard | Fast generation, good quality (default) |
| `sora-2-pro` | Pro | Highest quality, more detailed, longer duration support |

## Available Sizes

| Size | API Version | Description |
|------|-------------|-------------|
| `small` | 1.0 | Standard definition (default) |
| `large` | 1.0 | HD — sora-2-pro only |
| `720x1280` | 2.0 | Portrait HD resolution |
| `1280x720` | 2.0 | Landscape HD resolution |
| `1024x1792` | 2.0 | Portrait Full HD resolution |
| `1792x1024` | 2.0 | Landscape Full HD resolution |

## Available Durations

Valid duration values (seconds): `4`, `8`, `10`, `12`, `15`, `25`

- **Version 1.0**: 10 or 15s (sora-2); 10, 15, or 25s (sora-2-pro). Default: 15
- **Version 2.0**: 4, 8, or 12s. Default: 4


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `SORA_DEFAULT_MODEL` | Default model | `sora-2` |
| `SORA_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/SoraCli.git
cd SoraCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=sora_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy sora_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/sora-pro-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/sora-pro-cli generate "A test video"
```

## Project Structure

```
SoraCli/
├── sora_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m sora_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for Sora API
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── output.py          # Rich terminal formatting
│   └── commands/              # CLI command groups
│       ├── video.py           # Video generation commands
│       ├── task.py            # Task management commands
│       └── info.py            # Info & utility commands
├── tests/                     # Test suite
├── .github/workflows/         # CI/CD (lint, test, publish to PyPI)
├── Dockerfile                 # Container image
├── deploy/                    # Kubernetes deployment configs
├── .env.example               # Environment template
├── pyproject.toml             # Project configuration
└── README.md
```

## Sora CLI vs Sora MCP

| Feature | Sora CLI | Sora MCP |
|---------|-----------|-----------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install sora-pro-cli` | `pip install mcp-sora` |

Both tools use the same AceDataCloud API and share the same API token.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

### Development Requirements

- Python 3.10+
- Dependencies: `pip install -e ".[all]"`
- Lint: `ruff check . && ruff format --check .`
- Test: `pytest`

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
