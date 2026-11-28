# DrawAI CLI

A command-line tool for the [AceDataCloud](https://platform.acedata.cloud) AI ID Photo (DrawAI) API.

## Installation

```bash
pip install drawai-cli
```

## Quick Start

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

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
