# Seedance CLI

[![PyPI version](https://img.shields.io/pypi/v/seedance-cli.svg)](https://pypi.org/project/seedance-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/seedance-cli.svg)](https://pypi.org/project/seedance-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/AceDataCloud/SeedanceCli/actions/workflows/ci.yaml/badge.svg)](https://github.com/AceDataCloud/SeedanceCli/actions/workflows/ci.yaml)

A command-line tool for AI video generation using [Seedance](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Generate AI videos directly from your terminal — no MCP client required.

## Features

- **Video Generation** — Generate videos from text prompts with multiple models
- **Image-to-Video** — Create videos from reference images
- **Multiple Models** — doubao-seedance-1-5-pro-251215, doubao-seedance-1-0-pro-250528, doubao-seedance-1-0-pro-fast-251015, doubao-seedance-1-0-lite-t2v-250428, doubao-seedance-1-0-lite-i2v-250428
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Seedance API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install seedance-cli

# Or with uv (recommended)
uv pip install seedance-cli

# Or from source
git clone https://github.com/AceDataCloud/SeedanceCli.git
cd SeedanceCli
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
seedance generate "A test video"

# Generate from reference image
seedance image-to-video "Animate this scene" -i https://example.com/photo.jpg

# Check task status
seedance task <task-id>

# Wait for completion
seedance wait <task-id> --interval 5

# List available models
seedance models
```

## Commands

| Command | Description |
|---------|-------------|
| `seedance generate <prompt>` | Generate a video from a text prompt |
| `seedance image-to-video <prompt> -i <url>` | Generate a video from reference image(s) |
| `seedance task <task_id>` | Query a single task status |
| `seedance tasks <id1> <id2>...` | Query multiple tasks at once |
| `seedance wait <task_id>` | Wait for task completion with polling |
| `seedance models` | List available Seedance models |
| `seedance config` | Show current configuration |
| `seedance aspect-ratios` | List available aspect ratios |
| `seedance resolutions` | List available output resolutions |


## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

Most commands support:

```
--json                       Output raw JSON (for piping/scripting)
--model TEXT                 Seedance model version (default: doubao-seedance-1-0-pro-250528)
--aspect-ratio TEXT          Aspect ratio (16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive)
--resolution TEXT            Output resolution (480p, 720p, 1080p)
--duration FLOAT             Duration in seconds (2–12). Mutually exclusive with --frames.
--frames INT                 Frame count (29–289, must satisfy 25+4n). Mutually exclusive with --duration.
--seed INT                   Random seed for reproducible generation (-1 for random).
--camerafixed BOOL           Fix the camera position (true/false).
--watermark BOOL             Add a watermark to the output (true/false).
--generate-audio BOOL        Generate audio (true/false). Only doubao-seedance-1-5-pro-251215.
--return-last-frame BOOL     Return the last frame of the video (true/false).
--service-tier TEXT          Service level (default/flex).
--execution-expires-after INT  Task timeout in seconds (3600–259200).
--callback-url TEXT          Webhook callback URL.
```

## Available Models

| Model | Version | Notes |
|-------|---------|-------|
| `doubao-seedance-1-5-pro-251215` | V1.5 Pro | Newest, supports audio generation |
| `doubao-seedance-1-0-pro-250528` | V1.0 Pro | Standard quality (default) |
| `doubao-seedance-1-0-pro-fast-251015` | V1.0 Fast | Faster generation |
| `doubao-seedance-1-0-lite-t2v-250428` | V1.0 Lite T2V | Lightweight text-to-video |
| `doubao-seedance-1-0-lite-i2v-250428` | V1.0 Lite I2V | Lightweight image-to-video |


## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `SEEDANCE_DEFAULT_MODEL` | Default model | `doubao-seedance-1-0-pro-250528` |
| `SEEDANCE_REQUEST_TIMEOUT` | Timeout in seconds | `1800` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/SeedanceCli.git
cd SeedanceCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=seedance_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy seedance_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/seedance-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/seedance-cli generate "A test video"
```

## Project Structure

```
SeedanceCli/
├── seedance_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py            # python -m seedance_cli entry point
│   ├── main.py                # CLI entry point
│   ├── core/                  # Core modules
│   │   ├── client.py          # HTTP client for Seedance API
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

## Seedance CLI vs MCP Seedance

| Feature | Seedance CLI | MCP Seedance |
|---------|-----------|-----------|
| Interface | Terminal commands | MCP protocol |
| Usage | Direct shell, scripts, CI/CD | Claude, VS Code, MCP clients |
| Output | Rich tables / JSON | Structured MCP responses |
| Automation | Shell scripts, piping | AI agent workflows |
| Install | `pip install seedance-cli` | `pip install mcp-seedance` |

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
