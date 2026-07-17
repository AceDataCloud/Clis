# Grok CLI

A command-line tool for Grok chat completions and video generation through the AceDataCloud platform.

## Installation

```bash
pip install grok-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Chat with Grok
grok chat "What is the capital of France?"

# Generate a video
grok video "A sunset over the ocean"

# Check a task status
grok task <task_id>

# Wait for a task to complete
grok wait <task_id>
```

## Commands

### `chat`

Chat with a Grok model.

```bash
grok chat "Your prompt here" [OPTIONS]
```

Options:
- `-m, --model`: Model to use (`grok-4.5`, `grok-4`, `grok-3`, default: `grok-4`)
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
- `--reasoning-effort`: Reasoning effort level (minimal/low/medium/high)
- `--service-tier`: Service tier (auto/default/flex/scale/priority)
- `--logprobs`: Return log probabilities of output tokens
- `--top-logprobs`: Number of most likely tokens with log probabilities to return
- `--parallel-tool-calls`: Enable parallel function calling during tool use
- `--store`: Store the output of this completion request
- `--json`: Output raw JSON

### `video`

Generate a video using Grok.

```bash
grok video [PROMPT] [OPTIONS]
```

Options:
- `-m, --model`: Video model (`grok-imagine-video-1.5-fast`, `grok-imagine-video-1.5`, default: `grok-imagine-video-1.5-fast`)
- `--image-url`: Reference image URL for image-to-video
- `--reference-image-url`: Additional reference image URLs (repeatable)
- `-a, --aspect-ratio`: Aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)
- `-r, --resolution`: Output resolution (480p, 720p, 1080p)
- `--duration`: Duration in seconds
- `--callback-url`: Webhook callback URL
- `--async`: Submit asynchronously
- `--json`: Output raw JSON

### `task`

Query a single task status.

```bash
grok task <task_id>
```

### `tasks`

Query multiple tasks at once.

```bash
grok tasks <task_id1> <task_id2> ...
```

### `wait`

Wait for a task to complete, polling periodically.

```bash
grok wait <task_id> [--interval SECONDS] [--timeout SECONDS]
```

### `models`

List available Grok models.

```bash
grok models [--type chat|video|all]
```

### `config`

Show current configuration.

```bash
grok config
```

## Authentication

Set your API token via environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or pass it directly:

```bash
grok --token your_token chat "Hello"
```

Get your API token at https://platform.acedata.cloud
