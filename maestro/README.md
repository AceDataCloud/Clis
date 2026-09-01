# Maestro CLI

CLI tool for [Maestro AI Video Studio](https://platform.acedata.cloud/documents/maestro) via AceDataCloud API.

## Installation

```bash
pip install maestro-cli
```

## Usage

```bash
maestro create "Explain what a vector database is in 20 seconds"
maestro create "Product demo" --aspect 16:9
maestro create "Continue the story" --action extend --ref-task-id <task-id>
maestro task <task-id>
maestro wait <task-id>
```

## Video options

Videos render at 1080p/30fps. Set a duration from 5 to 300 seconds and provide up to four output languages or 20 reference media URLs.
