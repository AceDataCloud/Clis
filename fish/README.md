# Fish CLI

A command-line tool for Fish Audio Text-to-Speech generation via the AceDataCloud platform.

## Installation

```bash
pip install fish-cli
```

## Usage

```bash
# Generate TTS audio
fish tts "Hello, world!"

# Use a specific voice model
fish tts "Hello" --reference-id d7900c21663f485ab63ebdb7e5905036

# Generate in WAV format
fish tts "Hello" --format wav

# Async generation with callback
fish tts "Hello" --callback-url https://webhook.site/your-id

# List voice models
fish models

# Get a specific voice model
fish model d7900c21663f485ab63ebdb7e5905036

# Query a task
fish task 2725a2d3-f87e-4905-9c53-9988d5a7b2f5

# Wait for task completion
fish wait 2725a2d3-f87e-4905-9c53-9988d5a7b2f5
```

## Configuration

Set your API token as an environment variable:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or use the `--token` option:

```bash
fish --token your_token tts "Hello"
```

Get your API token at [https://platform.acedata.cloud](https://platform.acedata.cloud).

## License

MIT
