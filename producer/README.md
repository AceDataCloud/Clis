# Producer CLI

A command-line tool for AI music generation using the Producer service via AceDataCloud API.

## Installation

```bash
pip install producer-cli
```

## Usage

```bash
# Set your API token
export ACEDATACLOUD_API_TOKEN=your_token

# Generate a music track
producer generate "A happy upbeat pop song about summer"

# Generate with a specific model
producer generate "Dark metal with heavy guitar riffs" -m "FUZZ-2.0 Pro"

# Generate an instrumental track
producer generate "Epic orchestral battle theme" --instrumental

# Generate lyrics
producer lyrics "A love song about the ocean at sunset"

# Create a cover of an existing track
producer cover abc123-def456

# Extend an existing track
producer extend abc123-def456 --continue-at 30.5

# Generate a variation
producer variation abc123-def456

# Swap vocals
producer swap-vocals abc123-def456

# Swap instrumentals
producer swap-instrumentals abc123-def456

# Replace a section
producer replace-section abc123 --replace-section-start 10 --replace-section-end 30

# Extract stems
producer stems abc123-def456

# Upload audio from URL
producer upload https://example.com/my-audio.mp3

# Generate video from audio
producer video abc123-def456

# Get WAV format
producer wav abc123-def456

# Check task status
producer task abc123-def456

# Wait for task completion
producer wait abc123-def456

# List available models
producer models

# Show configuration
producer config
```

## Authentication

Set your API token via the `ACEDATACLOUD_API_TOKEN` environment variable or use the `--token` option:

```bash
producer --token your_token generate "A happy song"
```

## License

MIT
