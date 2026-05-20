# Gemini CLI

A command-line tool for Gemini chat completions via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install gemini-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

gemini chat "What is the capital of France?"
gemini chat "Explain AI" -m gemini-3.1-pro
gemini models
```

## Commands

| Command | Description |
|---------|-------------|
| `gemini chat <prompt>` | Chat with a Gemini model |
| `gemini models` | List available Gemini models |
| `gemini config` | Show current configuration |

## Global Options

```
--token TEXT    API token (or set ACEDATACLOUD_API_TOKEN env var)
--version       Show version
--help          Show help message
```

## Available Models

| Model | Notes |
|-------|-------|
| `gemini-3.1-pro` | Latest Gemini Pro model |
| `gemini-3.0-pro` | Gemini 3.0 Pro |
| `gemini-3.5-flash` | Gemini 3.5 Flash |
| `gemini-3-flash-preview` | Gemini 3 Flash Preview |
| `gemini-2.5-pro` | Gemini 2.5 Pro |
| `gemini-2.5-flash` | Gemini 2.5 Flash (default) |
| `gemini-2.0-flash` | Gemini 2.0 Flash |

## Configuration

Set environment variables or use a `.env` file:

```bash
ACEDATACLOUD_API_TOKEN=your_token
ACEDATACLOUD_API_BASE_URL=https://api.acedata.cloud
GEMINI_REQUEST_TIMEOUT=30
```

## License

MIT
