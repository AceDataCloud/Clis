# Seedream CLI

[![PyPI version](https://img.shields.io/pypi/v/seedream-cli.svg)](https://pypi.org/project/seedream-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/seedream-cli.svg)](https://pypi.org/project/seedream-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/SeedreamCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/SeedreamCli/actions/workflows/ci.yaml)

A command-line tool for AI image generation using [Seedream](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI images directly from your terminal — no MCP client required.

## Features

- **Image Generation** — Generate images from text prompts with multiple models
- **Image Editing** — Edit, combine, and transform images with AI
- **Multiple Models** — doubao-seedream-5-0-260128, doubao-seedream-4-5-251128, doubao-seedream-4-0-250828, doubao-seedream-3-0-t2i-250415, doubao-seededit-3-0-i2i-250628
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Seedream API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install seedream-cli

# Or with uv (recommended)
uv pip install seedream-cli

# Or from source
git clone https://github.com/AceDataCloud/SeedreamCli.git
cd SeedreamCli
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
# Generate an image
seedream generate "A test image"

# Edit an image
seedream edit "Make it look like a painting" -i https://example.com/photo.jpg

# Check task status
seedream task <task-id>

# Wait for completion
seedream wait <task-id> --interval 5

# List available models
seedream models
```

## Commands

| Command | Description |
|---------|-------------|
| `seedream generate <prompt>` | Generate an image from a text prompt |
| `seedream edit <prompt> -i <url>...` | Edit or combine images using AI |
| `seedream task <task_id>` | Query a single task status |
| `seedream tasks <id1> <id2>...` | Query multiple tasks at once |
| `seedream wait <task_id>` | Wait for task completion with polling |
| `seedream models` | List available Seedream models |
| `seedream config` | Show current configuration |
| `seedream resolutions` | List available output resolutions |


## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--model TEXT    Seedream model version (default: doubao-seedream-5-0-260128)
```

## Available Models

| Model | Version | Notes |
|-------|---------|-------|
| `doubao-seedream-5-0-260128` | V5.0 | Latest model (default) |
| `doubao-seedream-4-5-251128` | V4.5 | Flagship model, best quality |
| `doubao-seedream-4-0-250828` | V4.0 | Standard quality |
| `doubao-seedream-3-0-t2i-250415` | V3.0 T2I | Text-to-image generation |
| `doubao-seededit-3-0-i2i-250628` | V3.0 I2I | Image-to-image editing |


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `SEEDREAM_DEFAULT_MODEL` | Default model | `doubao-seedream-5-0-260128` |
| `SEEDREAM_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/SeedreamCli.git
cd SeedreamCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=seedream_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy seedream_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/seedream-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/seedream-cli generate "A test image"
```

## Project Structure

```
SeedreamCli/
├── seedream_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m seedream_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for Seedream API
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── output.py          # Rich terminal formatting
│   └── commands/              # CLI command groups
│       ├── image.py           # Image generation commands
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

## Seedream CLI vs Seedream MCP

| Feature | Seedream CLI | Seedream MCP |
|---------|-----------|-----------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install seedream-cli` | `pip install mcp-seedream-pro` |

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
