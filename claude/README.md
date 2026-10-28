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

## Chat and Messages billing

Accepted compatible-model requests are billed for the selected model's input, output and cache usage, not a fixed fee per request. Switching interface formats does not change this to per-request billing. Check current model prices in the console and the returned `usage.cost` for the charge; billing support alone does not establish model availability or account access.

- Chat Completions `usage.prompt_tokens` includes cached tokens. Reported cache usage is settled at the corresponding cache price; do not add it to the prompt total again.
- Messages `usage.input_tokens` excludes separately reported cache-read and cache-creation tokens. Those dimensions are settled separately, so input tokens alone do not describe all billed input usage.

Use `--json` to inspect the full returned usage, including cache details and `usage.cost` when present; the default terminal summary is not a billing breakdown. These commands submit billable requests:

```bash
claude chat "Hello" --model claude-3-5-haiku-20241022 --json | jq '.usage'
claude messages "Hello" --model claude-3-5-haiku-20241022 --max-tokens 1024 --json | jq '.usage'
```

### Opus 5.5

`claude-opus-5-5` supports ordinary and streaming Chat Completions, as well as Messages. Chat compatibility does not return native thinking blocks; use Messages for complete thinking blocks, signatures and native tool semantics.

For this model's Chat requests, use only `--count 1`, omit `--temperature` or set it to at least 1, and omit `--top-p` or use its default value of 1. When calling tools, use `--tool-choice auto`, not a forced tool. Leave sufficient output budget for thinking and the final text.

```bash
claude chat "Review these tradeoffs" --model claude-opus-5-5 --max-tokens 32768
claude chat "Review these tradeoffs" --model claude-opus-5-5 --max-tokens 32768 --stream
```

`chat --stream` prints raw SSE lines, including any terminal marker and usage events returned by the server; it does not assemble a single JSON response. Use each command's `--help` to check supported model choices; model defaults are unchanged.

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
