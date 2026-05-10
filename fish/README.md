# Fish CLI

A command-line tool for AI audio generation and voice cloning via [AceDataCloud](https://platform.acedata.cloud).

## Installation

```bash
pip install fish-pro-cli
```

Or install from source:

```bash
cd fish
pip install -e .
```

## Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token_here
```

Or copy `.env.example` to `.env` and fill in your token.

## Usage

### Generate Audio (TTS)

Generate audio from text using a cloned voice:

```bash
fish generate "Hello, world!" --voice-id d7900c21663f485ab63ebdb7e5905036
```

With options:

```bash
fish generate "Welcome to Fish TTS" \
  --voice-id d7900c21663f485ab63ebdb7e5905036 \
  --model fish-tts \
  --callback-url https://example.com/callback
```

### Clone a Voice

Register a new voice from an audio URL:

```bash
fish clone-voice --voice-url https://example.com/sample.mp3 --title "My Voice"
```

With additional metadata:

```bash
fish clone-voice \
  --voice-url https://example.com/sample.mp3 \
  --title "My Voice" \
  --description "A custom voice clone" \
  --image-url https://example.com/cover.jpg
```

### Task Management

Query a single task:

```bash
fish task abc123-def456
```

Query multiple tasks:

```bash
fish tasks abc123 def456 ghi789
```

Wait for a task to complete:

```bash
fish wait abc123
fish wait abc123 --interval 10 --timeout 300
```

### List Models

```bash
fish models
```

### Show Configuration

```bash
fish config
```

## Options

All commands support `--json` for machine-readable output:

```bash
fish generate "Hello" --voice-id abc123 --json
```

Pass a token directly:

```bash
fish --token YOUR_TOKEN generate "Hello" --voice-id abc123
```

## Available Models

| Model    | Description                              |
| -------- | ---------------------------------------- |
| fish-tts | Default text-to-speech with voice cloning |

## License

MIT License. See [LICENSE](LICENSE) for details.
