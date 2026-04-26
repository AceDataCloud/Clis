# Claude CLI

A command-line interface for Anthropic Claude AI via AceDataCloud.

## Installation

```bash
pip install claude-cli
```

## Usage

```bash
# Chat using OpenAI-compatible endpoint
claude-cli chat "What is the capital of France?"

# Send messages using native Claude Messages API
claude-cli messages "Explain quantum computing"

# Count tokens in a message
claude-cli count-tokens "Hello, how are you?"

# Specify a model
claude-cli chat "Hello" --model claude-opus-4-20250514

# List available models
claude-cli models

# Show configuration
claude-cli config
```

## Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or use the `--token` flag:

```bash
claude-cli --token your_token chat "Hello"
```

Get your API token at https://platform.acedata.cloud
