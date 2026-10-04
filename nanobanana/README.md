# NanoBanana CLI

[![PyPI version](https://img.shields.io/pypi/v/nano-banana-pro-cli.svg)](https://pypi.org/project/nano-banana-pro-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/nano-banana-pro-cli.svg)](https://pypi.org/project/nano-banana-pro-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/NanoBananaCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/NanoBananaCli/actions/workflows/ci.yaml)

A command-line tool for AI image generation and editing using [NanoBanana](https://platform.acedata.cloud/) (Gemini-powered) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate and edit AI images directly from your terminal — no MCP client required.

## Features

- **Image Generation** — Generate images from text prompts with multiple models
- **Image Editing** — Edit, combine, and transform images with AI
- **Multiple Models** — nano-banana (fast), nano-banana-2 (improved), nano-banana-pro (best, 4K)
- **Flexible Output** — Aspect ratios (1:1, 16:9, 9:16, etc.) and resolutions (1K/2K/4K)
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the NanoBanana API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install nano-banana-pro-cli

# Or with uv (recommended)
uv pip install nano-banana-pro-cli

# Or from source
git clone https://github.com/AceDataCloud/NanoBananaCli.git
cd NanoBananaCli
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
# Generate an image from a prompt
nano-banana-pro generate "A cat sitting on a windowsill at sunset, warm lighting"

# Generate with specific model and aspect ratio
nano-banana-pro generate "Product photo of a watch" -m nano-banana-pro -a 16:9 -r 4K

# Edit an image
nano-banana-pro edit "Make it look like an oil painting" -i https://example.com/photo.jpg

# Virtual try-on (combine person + clothing)
nano-banana-pro edit "Let this person wear this T-shirt" -i person.jpg -i shirt.jpg

# Check task status
nano-banana-pro task <task-id>

# Wait for completion with polling
nano-banana-pro wait <task-id> --interval 5

# List available models
nano-banana-pro models
```

## Commands

### Image Generation & Editing

| Command | Description |
|---------|-------------|
| `nano-banana-pro generate <prompt>` | Generate an image from a text prompt |
| `nano-banana-pro edit <prompt> -i <url>...` | Edit or combine images using AI |

### Task Management

| Command | Description |
|---------|-------------|
| `nano-banana-pro task <task_id>` | Query a single task status |
| `nano-banana-pro tasks <id1> <id2>...` | Query multiple tasks at once |
| `nano-banana-pro wait <task_id>` | Wait for task completion with polling |

### Utilities

| Command | Description |
|---------|-------------|
| `nano-banana-pro models` | List available NanoBanana models |
| `nano-banana-pro aspect-ratios` | List available aspect ratios |
| `nano-banana-pro resolutions` | List available output resolutions |
| `nano-banana-pro config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json          Output raw JSON (for piping/scripting)
--model TEXT    NanoBanana model version (default: nano-banana)
```

## Scripting & Piping

The `--json` flag outputs machine-readable JSON suitable for piping:

```bash
# Generate and extract task ID
TASK_ID=$(nano-banana-pro generate "a red circle" --json | jq -r '.task_id')

# Wait for completion and get image URL
nano-banana-pro wait $TASK_ID --json | jq -r '.data[0].image_url'

# Batch generate from a file of prompts
while IFS= read -r prompt; do
  nano-banana-pro generate "$prompt" --json >> results.jsonl
done < prompts.txt
```

## Available Models

| Model | Engine | Notes |
|-------|--------|-------|
| `nano-banana` | Gemini 2.5 Flash | Fast, good quality (default) |
| `nano-banana-2` | Improved | Better quality, balanced speed |
| `nano-banana-pro` | Gemini 3 Pro | Best quality, supports resolution control (1K/2K/4K) |

## Aspect Ratios

| Ratio | Orientation |
|-------|-------------|
| `1:1` | Square (default) |
| `3:2` / `2:3` | Classic photo |
| `16:9` / `9:16` | Widescreen / Portrait |
| `4:3` / `3:4` | Standard |

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `NANOBANANA_DEFAULT_MODEL` | Default model | `nano-banana` |
| `NANOBANANA_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AceDataCloud/NanoBananaCli.git
cd NanoBananaCli

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
pip install -e ".[dev,test]"
```

### Run Tests

```bash
# Run unit tests
pytest

# Run with coverage
pytest --cov=nanobanana_cli

# Run integration tests (requires API token)
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy nanobanana_cli
```

### Build & Publish

```bash
# Install build dependencies
pip install -e ".[release]"

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Docker

```bash
# Pull the image
docker pull ghcr.io/acedatacloud/nano-banana-pro-cli:latest

# Run a command
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/nano-banana-pro-cli generate "A beautiful sunset"

# Or use docker-compose
docker compose run --rm nano-banana-pro-cli generate "A beautiful sunset"
```

## Project Structure

```
NanoBananaCli/
├── nanobanana_cli/            # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m nanobanana_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for NanoBanana API
│   │   ├── config.py          # Configuration management
│   │   ├── exceptions.py      # Custom exceptions
│   │   └── output.py          # Rich terminal formatting
│   └── commands/              # CLI command groups
│       ├── image.py           # Image generation & editing commands
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

## NanoBanana CLI vs MCP NanoBanana

| Feature | NanoBanana CLI | MCP NanoBanana |
|---------|----------------|----------------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install nano-banana-pro-cli` | `pip install mcp-nanobanana-pro` |

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
