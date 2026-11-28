# QRArt CLI

A command-line tool for the [AceDataCloud](https://platform.acedata.cloud) Art QR Code Generation API.

## Installation

```bash
pip install qrart-cli
```

## Quick Start

Sign in to [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) and open **General Application**. On your first visit, select **Initialize General Application** if prompted. Copy the key with the button beside **API KEY**, marked **1** in the screenshot. Store it privately in `ACEDATACLOUD_API_TOKEN` on the machine that runs the CLI.

![Copy button beside API KEY in General Application, marked 1](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

```bash
export ACEDATACLOUD_API_TOKEN=your_token

# Generate an art QR code
qrart generate "A beautiful sunset over the ocean" --content https://example.com

# Use a predefined style preset
qrart generate "Futuristic city" --content https://example.com --preset neon-mech

# Use custom pattern and pixel style
qrart generate "Cherry blossoms" --content https://example.com \
              --pattern s1 --pixel-style rounded

# Check task status
qrart task abc123-def456

# Wait for completion
qrart wait abc123
```

## Commands

- `generate` – Generate an artistic QR code from a text prompt
- `task` – Query a single task status
- `tasks` – Query multiple tasks
- `wait` – Poll until a task completes
- `presets` – List available style presets
- `config` – Show current configuration
