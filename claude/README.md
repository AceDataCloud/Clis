# Claude CLI

A command-line tool for Claude AI models via AceDataCloud.

## Installation

```bash
pip install claude-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Chat with a Claude model (OpenAI-compatible endpoint)
claude chat "What is the capital of France?"

# Use the native Claude Messages API
claude messages "Tell me a joke" --max-tokens 1024

# Count tokens for a prompt
claude count-tokens "Hello, how are you?" --model claude-3-5-haiku-20241022

# List available models
claude models

# Show configuration
claude config
```

## Commands

- `chat` — Chat completions via the OpenAI-compatible endpoint
- `messages` — Claude native Messages API
- `count-tokens` — Count tokens for a given prompt
- `models` — List available Claude models
- `config` — Show current configuration

## Get API Token

Visit [https://platform.acedata.cloud](https://platform.acedata.cloud) to get your API token.
