# Veo CLI

[![PyPI version](https://img.shields.io/pypi/v/veo-cli.svg)](https://pypi.org/project/veo-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/veo-cli.svg)](https://pypi.org/project/veo-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/VeoCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/VeoCli/actions/workflows/ci.yaml)

A command-line tool for AI video generation using [Veo](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI videos directly from your terminal — no MCP client required.

## Features

- **Video Generation** — Generate videos from text prompts with multiple models
- **Image-to-Video** — Create videos from reference images- **Video Upscale** — Get 1080p versions of generated videos
- **Multiple Models** — veo3, veo3-fast, veo31, veo31-fast, veo31-fast-ingredients, veo2, veo2-fast
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Veo API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install veo-cli

# Or with uv (recommended)
uv pip install veo-cli

# Or from source
git clone https://github.com/AceDataCloud/VeoCli.git
cd VeoCli
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
veo generate "A test video"

# Generate from reference image
veo image-to-video "Animate this scene" -i https://example.com/photo.jpg

# Generate from ingredient images (uses veo31-fast-ingredients model)
veo ingredients-to-video "Product showcase" -i https://example.com/product.jpg

# Upscale to 1080p
veo upscale <video-id>

# Check task status
veo task <task-id>

# Wait for completion
veo wait <task-id> --interval 5

# List available models
veo models
```

## Commands

| Command | Description |
|---------|-------------|
| `veo generate <prompt>` | Generate a video from a text prompt |
| `veo image-to-video <prompt> -i <url>` | Generate a video from reference image(s) |
| `veo ingredients-to-video <prompt> -i <url>` | Generate a video from 1-3 ingredient images |
| `veo upscale <video_id>` | Get 1080p version of a generated video |
| `veo task <task_id>` | Query a single task status |
| `veo tasks <id1> <id2>...` | Query multiple tasks at once |
| `veo wait <task_id>` | Wait for task completion with polling |
| `veo models` | List available Veo models |
| `veo config` | Show current configuration |
| `veo aspect-ratios` | List available aspect ratios |


## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json                        Output raw JSON (for piping/scripting)
--model TEXT                  Veo model version (default: veo3)
--resolution TEXT             Output resolution: 4k, 1080p, gif (generate and image-to-video)
--translation/--no-translation  Enable automatic prompt translation (generate and image-to-video)
```

## Available Models

| Model | Version | Notes |
|-------|---------|-------|
| `veo3` | V3 | Latest model, best quality (default) |
| `veo3-fast` | V3 Fast | Fast generation |
| `veo31` | V3.1 | Next generation model |
| `veo31-fast` | V3.1 Fast | Fast next-gen model |
| `veo31-fast-ingredients` | V3.1 Fast Ingredient | Ingredient-based fast next-gen model |
| `veo2` | V2 | Previous generation, stable |
| `veo2-fast` | V2 Fast | Fast previous-gen model |


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `VEO_DEFAULT_MODEL` | Default model | `veo3` |
| `VEO_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/VeoCli.git
cd VeoCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=veo_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy veo_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/veo-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/veo-cli generate "A test video"
```

## Project Structure

```
VeoCli/
├── veo_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m veo_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for Veo API
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

## Veo CLI vs MCP Veo

| Feature | Veo CLI | MCP Veo |
|---------|-----------|-----------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install veo-cli` | `pip install mcp-veo` |

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
