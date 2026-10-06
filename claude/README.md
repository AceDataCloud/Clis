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
- `models` — List models available to Chat Completions and Messages
- `config` — Show current configuration

## Sol Fast

The public alias `gpt-5.6-sol-fast` is available through both `chat` and `messages`. It is not supported by `count-tokens`; Claude model defaults are unchanged.

```bash
claude chat "Explain the tradeoffs" --model gpt-5.6-sol-fast
claude messages "Explain the tradeoffs" --model gpt-5.6-sol-fast --max-tokens 1024
```

## Thinking options

`messages` and `count-tokens` pass thinking settings through to the selected model without fixed mode/display enums, a minimum budget, or model-specific combination rules. The model determines which values and combinations it supports; parameter errors are returned rather than silently rewriting the request.

Use `--thinking` for a JSON object, including extension fields. The convenience flags `--thinking-type`, `--thinking-budget-tokens`, and `--thinking-display` override only their corresponding fields if supplied alongside `--thinking`. `messages --output-config` likewise preserves JSON fields and effort values.

```bash
claude messages "Explain the tradeoffs" --max-tokens 16000 \
  --thinking '{"type":"adaptive","display":"summarized"}' \
  --output-config '{"effort":"high"}'

claude messages "Explain the tradeoffs" --max-tokens 16000 \
  --thinking-type adaptive --thinking-display updates \
  --anthropic-beta thinking-display-updates-2026-08-18

claude count-tokens "Explain the tradeoffs" \
  --thinking '{"type":"adaptive","display":"updates"}' \
  --anthropic-beta thinking-display-updates-2026-08-18
```

`display=updates` is a beta mode that requires the `anthropic-beta: thinking-display-updates-2026-08-18` header. Supply it with `--anthropic-beta` (comma-separated values can be used for multiple betas); the CLI does not add it automatically. Actual support and output depend on the selected model. Thinking and final text share the `max_tokens` output budget, so allow enough tokens for both.

## Get API Token

Visit [https://platform.acedata.cloud](https://platform.acedata.cloud) to get your API token.
