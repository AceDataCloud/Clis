# GLM CLI

A command-line tool for GLM AI chat via AceDataCloud API.

## Installation

```bash
pip install glm-cli
```

## Setup

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or copy `.env.example` to `.env` and fill in your token.

## Usage

```bash
glm chat "What is the capital of France?"
glm chat "Explain AI" -m glm-5.1
glm models
glm config
```

## Commands

| Command | Description |
|---------|-------------|
| `glm chat <prompt>` | Chat with a GLM model |
| `glm models` | List available GLM models |
| `glm config` | Show current configuration |

## Models

| Model | Notes |
|-------|-------|
| `glm-5.1` | Latest GLM model |
| `glm-4.7` | GLM 4.7 (default) |
| `glm-4.6` | GLM 4.6 |
| `glm-4.5-air` | GLM 4.5 Air |
| `glm-3-turbo` | GLM 3 Turbo |

## Options

```
glm chat --help
```

| Option | Description |
|--------|-------------|
| `-m, --model` | Model to use (default: glm-4.7) |
| `-s, --system` | System prompt |
| `--temperature` | Sampling temperature (0-2) |
| `--max-tokens` | Maximum tokens to generate |
| `--top-p` | Nucleus sampling probability |
| `--json` | Output raw JSON |

## License

MIT
