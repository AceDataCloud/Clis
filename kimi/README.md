# Kimi CLI

A command-line tool for Kimi chat completions through the AceDataCloud platform.

## Installation

```bash
pip install kimi-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Chat with Kimi
kimi chat "What is the capital of France?"

# Use a specific model
kimi chat "Explain quantum computing" -m kimi-k3.1-pro --reasoning-effort low

# List available models
kimi models

# Show configuration
kimi config
```

## Commands

### `chat`

Chat with a Kimi model.

```bash
kimi chat "Your prompt here" [OPTIONS]
```

Options:
- `-m, --model`: Model to use (default: `kimi-k3.1-pro`)
- `-s, --system`: System prompt
- `--temperature`: Sampling temperature (0-2)
- `--max-tokens`: Maximum tokens to generate
- `--max-completion-tokens`: Upper bound on tokens that can be generated for a completion
- `-n, --count`: Number of completion choices
- `--top-p`: Nucleus sampling probability
- `--frequency-penalty`: Frequency penalty (-2.0 to 2.0)
- `--presence-penalty`: Presence penalty (-2.0 to 2.0)
- `--seed`: Seed for deterministic sampling
- `--stop`: Stop sequences (repeatable)
- `--user`: End-user identifier
- `--reasoning-effort`: Reasoning effort level (`low`, `high`, or `max`)
- `--service-tier`: Service tier (auto/default/flex/scale/priority)
- `--logprobs`: Return log probabilities of output tokens
- `--top-logprobs`: Number of most likely tokens with log probabilities to return
- `--parallel-tool-calls`: Enable parallel function calling during tool use
- `--store`: Store the output of this completion request
- `--json`: Output raw JSON

K3.1 Pro always enables reasoning. Use `--reasoning-effort low`, `high`, or `max`
to select its reasoning effort; do not send thinking-disable settings. `kimi-k3`
remains available and should use `--reasoning-effort max`. For K2.6, use
`--thinking` with a JSON object instead of `--reasoning-effort`.

```bash
kimi chat "Review this code and suggest a fix" --reasoning-effort low
kimi chat "Explain this algorithm" -m kimi-k3 --reasoning-effort max
```

### `models`

List available Kimi models.

```bash
kimi models
```

### `config`

Show current configuration.

```bash
kimi config
```

## Available Models

| Model | Notes |
|-------|-------|
| `kimi-k3.1-pro` | Kimi K3.1 Pro (default, recommended) |
| `kimi-k3` | Kimi K3 |
| `kimi-k2.6` | Kimi K2.6 |
| `kimi-k2-thinking-turbo` | Kimi K2 Thinking Turbo |
| `kimi-k2.5` | Kimi K2.5 |
| `kimi-k2-thinking` | Kimi K2 Thinking |

## Authentication

Set your API token via environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or pass it directly:

```bash
kimi --token your_token chat "Hello"
```

Get your API token at https://platform.acedata.cloud
