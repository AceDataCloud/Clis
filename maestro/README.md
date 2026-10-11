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
maestro create "Explain what a vector database is in 20 seconds" --lang en
maestro create "Continue the story" --action extend --ref-task-id <task-id>
maestro task <task-id>
maestro wait <task-id>
```

## Video options

Videos render at 1080p/30fps. Set a duration from 5 to 300 seconds and provide up to 20 reference media URLs. Each task delivers one video in one language: use `--lang en` to select English, or omit `--lang` for the default `zh-cn`. Repeating `--lang` is rejected; create separate tasks for different languages.

Successful tasks cost **0.7 credits per actual delivered second**, capped at the requested duration. All scenarios, actions, and languages use the same rate, with no scenario multipliers or language surcharges. Failed tasks and task polling are free.
