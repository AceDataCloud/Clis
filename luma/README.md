# Luma CLI

[![PyPI version](https://img.shields.io/pypi/v/luma-pro-cli.svg)](https://pypi.org/project/luma-pro-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/luma-pro-cli.svg)](https://pypi.org/project/luma-pro-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/LumaCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/LumaCli/actions/workflows/ci.yaml)

A command-line tool for AI video generation using [Luma](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI videos directly from your terminal — no MCP client required.

## Features

- **Video Generation** — Generate videos from text prompts with multiple models
- **Image-to-Video** — Create videos from reference images- **Video Extension** — Extend existing videos
- **Multiple Models** — luma
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Luma API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install luma-pro-cli

# Or with uv (recommended)
uv pip install luma-pro-cli

# Or from source
git clone https://github.com/AceDataCloud/LumaCli.git
cd LumaCli
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
luma generate "A test video"

# Generate from reference image
luma image-to-video "Animate this scene" -i https://example.com/photo.jpg

# Extend a video
luma extend <video-id>

# Check task status
luma task <task-id>

# Wait for completion
luma wait <task-id> --interval 5

# List available models
luma models
```

## Commands

| Command | Description |
|---------|-------------|
| `luma generate <prompt>` | Generate a video from a text prompt |
| `luma image-to-video <prompt> -i <url>` | Generate a video from reference image(s) |
| `luma extend <video_id>` | Extend an existing video |
| `luma task <task_id>` | Query a single task status |
| `luma tasks <id1> <id2>...` | Query multiple tasks at once |
| `luma wait <task_id>` | Wait for task completion with polling |
| `luma models` | List available Luma models |
| `luma config` | Show current configuration |
| `luma aspect-ratios` | List available aspect ratios |


## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--model TEXT    Luma model version (default: luma)
--timeout INT   Timeout in seconds for the API to return data
```

## Available Models

| Model | Version | Notes |
|-------|---------|-------|
| `luma` | Standard | Standard quality video generation (default) |


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `LUMA_DEFAULT_MODEL` | Default model | `luma` |
| `LUMA_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/LumaCli.git
cd LumaCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=luma_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy luma_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/luma-pro-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/luma-pro-cli generate "A test video"
```

## Project Structure

```
LumaCli/
├── luma_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m luma_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for Luma API
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

## Luma CLI vs Luma MCP

| Feature | Luma CLI | Luma MCP |
|---------|-----------|-----------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install luma-pro-cli` | `pip install mcp-luma` |

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
