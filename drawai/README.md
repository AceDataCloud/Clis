# DrawAI CLI

A command-line tool for the [AceDataCloud](https://platform.acedata.cloud) AI ID Photo (DrawAI) API.

## Installation

```bash
pip install drawai-cli
```

## Quick Start

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Generate an AI headshot with default business template
drawai generate --image-url https://example.com/face.jpg

# Generate with a specific template
drawai generate --image-url https://example.com/face.jpg --template wedding

# Use relax mode for higher quality
drawai generate --image-url https://example.com/face.jpg --mode relax --async

# Check task status
drawai task abc123-def456

# Wait for completion
drawai wait abc123
```

## Commands

- `generate` – Generate an AI headshot or ID photo
- `task` – Query a single task status
- `tasks` – Query multiple tasks
- `wait` – Poll until a task completes
- `templates` – List available photo templates
- `config` – Show current configuration
