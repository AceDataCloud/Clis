# Gemini CLI

A command-line tool for Gemini AI via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install gemini-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

gemini chat "What is the capital of France?"
gemini chat "Explain AI" -m gemini-2.5-pro
gemini generate "A cinematic sunset over the ocean"
gemini models
```

## Commands

| Command | Description |
|---------|-------------|
| `gemini chat <prompt>` | Chat with a Gemini model |
| `gemini generate <prompt>` | Generate a video from a text prompt |
| `gemini image-to-video <prompt>` | Generate a video from reference image(s) |
| `gemini task <task_id>` | Query a task status |
| `gemini tasks <task_ids...>` | Query multiple tasks |
| `gemini wait <task_id>` | Wait for a task to complete |
| `gemini models` | List available Gemini models |
| `gemini config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

## Available Chat Models

| Model | Notes |
|-------|-------|
| `gemini-3.1-pro` | Latest Gemini Pro model |
| `gemini-3.0-pro` | Gemini 3.0 Pro |
| `gemini-3.5-flash` | Gemini 3.5 Flash |
| `gemini-3-flash-preview` | Gemini 3 Flash Preview |
| `gemini-3.1-flash-lite-preview` | Gemini 3.1 Flash Lite Preview |
| `gemini-3.1-flash-image-preview` | Gemini 3.1 Flash Image Preview |
| `gemini-3-pro-image-preview` | Gemini 3 Pro Image Preview |
| `gemini-2.5-pro` | Gemini 2.5 Pro |
| `gemini-2.5-flash` | Gemini 2.5 Flash (default) |
| `gemini-2.5-flash-lite` | Gemini 2.5 Flash Lite |
| `gemini-2.5-flash-image` | Gemini 2.5 Flash Image |
| `gemini-2.0-flash` | Gemini 2.0 Flash |

## Available Video Models

| Model | Notes |
|-------|-------|
| `omni-flash` | Gemini video generation model (default) |

## Configuration

Set environment variables or use a `.env` file:

```bash
ACEDATACLOUD_API_TOKEN=your_token
ACEDATACLOUD_API_BASE_URL=https://api.acedata.cloud
GEMINI_REQUEST_TIMEOUT=30
```

## License

MIT
