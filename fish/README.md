# Fish CLI

[![PyPI version](https://img.shields.io/pypi/v/fish-cli.svg)](https://pypi.org/project/fish-cli/)
[![PyPI downloads](https://img.shields.io/pypi/dm/fish-cli.svg)](https://pypi.org/project/fish-cli/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A command-line tool for AI text-to-speech using [Fish AI](https://platform.acedata.cloud/) through the [AceDataCloud API](https://platform.acedata.cloud/).

Convert text to speech directly from your terminal — no MCP client required.

## Features

- **Text-to-Speech** — Synthesize text to audio with multiple TTS models (s1, s2-pro)
- **Voice Models** — Browse and filter available Fish AI voice models
- **Multiple Formats** — Output in mp3, wav, pcm, or opus
- **Async Support** — Submit long synthesis jobs with a callback URL, then poll for completion
- **Task Management** — Query tasks, batch query, wait with polling
- **Rich Output** — Beautiful terminal tables and panels via Rich
- **JSON Mode** — Machine-readable output with `--json` for piping

## Quick Start

### 1. Get API Token

Get your API token from [AceDataCloud Platform](https://platform.acedata.cloud/):

1. Sign up or log in
2. Navigate to the Fish API page
3. Click "Acquire" to get your token

### 2. Install

```bash
# Install with pip
pip install fish-cli

# Or with uv (recommended)
uv pip install fish-cli

# Or from source
git clone https://github.com/AceDataCloud/FishCli.git
cd FishCli
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
# Synthesize text to speech
fish tts "Hello, world!"

# Use a specific voice model
fish tts "Hello" --reference-id <voice-id>

# Output as WAV
fish tts "Hello" --format wav --json

# Browse voice models
fish voices

# Filter by language
fish voices --language en

# Get details of a specific voice model
fish voice <voice-id>

# Check task status
fish task <task-id>

# Wait for completion
fish wait <task-id> --interval 5
```

## Commands

| Command | Description |
|---------|-------------|
| `fish tts <text>` | Convert text to speech |
| `fish voices` | List available voice models |
| `fish voice <voice_id>` | Get details of a specific voice model |
| `fish task <task_id>` | Query a single task status |
| `fish tasks <id1> <id2>...` | Query multiple tasks at once |
| `fish wait <task_id>` | Wait for task completion with polling |
| `fish models` | List available TTS models |
| `fish formats` | List available audio output formats |
| `fish config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

## TTS Options

```
--model TEXT              TTS model (s1, s2-pro). Default: s2-pro
--reference-id TEXT       Voice model ID for single-speaker synthesis
--format TEXT             Audio format (mp3, wav, pcm, opus). Default: mp3
--sample-rate INT         Sampling rate (e.g. 16000, 22050, 44100)
--mp3-bitrate TEXT        MP3 bit rate (64, 128, 192). Only for --format=mp3
--opus-bitrate INT        Opus bit rate. Only for --format=opus
--latency TEXT            Latency mode (normal, balanced). Default: normal
--chunk-length INT        Chunk length for the upstream synthesiser
--min-chunk-length INT    Minimum chunk length
--temperature FLOAT       Sampling temperature (0.0–1.0)
--top-p FLOAT             Top-p nucleus sampling parameter
--repetition-penalty FLOAT  Repetition penalty
--max-new-tokens INT      Maximum number of new tokens to generate
--normalize/--no-normalize  Apply text normalization
--callback-url TEXT       Webhook URL for async synthesis (returns task_id)
--json                    Output raw JSON
```

## Available TTS Models

| Model | Notes |
|-------|-------|
| `s2-pro` | High-quality TTS model (default) |
| `s1` | Standard TTS model |

## Voice Model Filters

```
--page-size INT         Items per page (default: 10)
--page-number INT       Page number (default: 1)
--title TEXT            Filter by partial title match
--tag TEXT              Filter by tag
--self                  Only show your own voice models
--author-id TEXT        Filter by author ID
--language TEXT         Filter by language code (e.g. en, zh)
--title-language TEXT   Filter by title language
--sort-by TEXT          Sort field (e.g. created_at, task_count)
--json                  Output raw JSON
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token from AceDataCloud | *Required* |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `FISH_DEFAULT_MODEL` | Default TTS model | `s2-pro` |
| `FISH_REQUEST_TIMEOUT` | Timeout in seconds | `300` |

## Development

### Setup Development Environment

```bash
git clone https://github.com/AceDataCloud/FishCli.git
cd FishCli
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
```

### Run Tests

```bash
pytest
pytest --cov=fish_cli
pytest tests/test_integration.py -m integration
```

### Code Quality

```bash
ruff format .
ruff check .
mypy fish_cli
```

## Docker

```bash
docker pull ghcr.io/acedatacloud/fish-cli:latest
docker run --rm -e ACEDATACLOUD_API_TOKEN=your_token \
  ghcr.io/acedatacloud/fish-cli tts "Hello, world!"
```

## Project Structure

```
FishCli/
├── fish_cli/                # Main package
│   ├── __init__.py
│   ├── __main__.py          # python -m fish_cli entry point
│   ├── main.py              # CLI entry point
│   ├── core/                # Core modules
│   │   ├── client.py        # HTTP client for Fish API
│   │   ├── config.py        # Configuration management
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── output.py        # Rich terminal formatting
│   └── commands/            # CLI command groups
│       ├── tts.py           # Text-to-speech command
│       ├── voice.py         # Voice model commands
│       ├── task.py          # Task management commands
│       └── info.py          # Info & utility commands
├── tests/                   # Test suite
├── Dockerfile               # Container image
├── .env.example             # Environment template
├── pyproject.toml           # Project configuration
└── README.md
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
