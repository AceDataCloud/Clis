# Dreamina CLI

A command-line tool for generating AI talking-head videos using Dreamina through the AceDataCloud platform.

## Installation

```bash
pip install dreamina-cli
```

## Quick Start

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Generate a talking-head video
dreamina generate --image-url https://example.com/portrait.jpg \
                  --audio-url https://example.com/speech.mp3

# Check a task status
dreamina task <task_id>

# Wait for a task to complete
dreamina wait <task_id>
```

## Commands

### `generate`

Generate a talking-head video from a portrait image and audio file.

```bash
dreamina generate --image-url <URL> --audio-url <URL> [OPTIONS]
```

Options:
- `--image-url` (required): URL of the portrait image
- `--audio-url` (required): URL of the audio file
- `-m, --model`: Model to use (default: `omnihuman-1.5`)
- `--prompt`: Optional text prompt to guide generation
- `--mask-url`: URL(s) of mask image(s) (repeatable)
- `--callback-url`: Webhook callback URL
- `--async`: Submit asynchronously and return task_id
- `--json`: Output raw JSON

### `task`

Query a single task status.

```bash
dreamina task <task_id>
```

### `tasks`

Query multiple tasks at once.

```bash
dreamina tasks <task_id1> <task_id2> ...
```

### `wait`

Wait for a task to complete, polling periodically.

```bash
dreamina wait <task_id> [--interval SECONDS] [--timeout SECONDS]
```

### `models`

List available Dreamina models.

```bash
dreamina models
```

### `config`

Show current configuration.

```bash
dreamina config
```

## Authentication

Set your API token via environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or pass it directly:

```bash
dreamina --token your_token generate --image-url ...
```

Get your API token at https://platform.acedata.cloud
