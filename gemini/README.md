# Gemini CLI

A command-line interface for Google Gemini AI via AceDataCloud.

## Installation

```bash
pip install gemini-cli
```

## Usage

```bash
# Chat using OpenAI-compatible endpoint
gemini-cli chat "What is the capital of France?"

# Generate content using native Gemini API
gemini-cli generate "Explain quantum computing"

# Specify a model
gemini-cli chat "Hello" --model gemini-2.5-pro

# List available models
gemini-cli models

# Show configuration
gemini-cli config
```

## Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or use the `--token` flag:

```bash
gemini-cli --token your_token chat "Hello"
```

Get your API token at https://platform.acedata.cloud
