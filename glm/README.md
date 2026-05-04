# GLM CLI

A command-line tool for GLM chat completions via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install glm-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

glm chat "What is the capital of France?"
glm chat "Explain AI" -m glm-5.1
glm models
```

## Commands

| Command | Description |
|---------|-------------|
| `glm chat <prompt>` | Chat with a GLM model |
| `glm models` | List available GLM models |
| `glm config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

## Available Models

| Model | Notes |
|-------|-------|
| `glm-5.1` | Latest GLM model |
| `glm-4.7` | GLM-4 series (default) |
| `glm-4.6` | GLM-4 series |
| `glm-4.5-air` | GLM-4 Air variant |
| `glm-3-turbo` | GLM-3 Turbo |

## Configuration

Set environment variables or use a `.env` file:

```bash
ACEDATACLOUD_API_TOKEN=your_token
ACEDATACLOUD_API_BASE_URL=https://api.acedata.cloud
GLM_REQUEST_TIMEOUT=30
```

## License

MIT
