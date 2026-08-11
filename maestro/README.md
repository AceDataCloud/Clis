# Maestro CLI

CLI tool for [Maestro AI Video Studio](https://platform.acedata.cloud/documents/maestro) via AceDataCloud API.

## Installation

```bash
pip install maestro-cli
```

## Usage

```bash
maestro create "Explain what a vector database is in 20 seconds"
maestro create "Product demo" --aspect 16:9 --quality pro
maestro create "Continue the story" --action extend --ref-task-id <task-id>
maestro task <task-id>
maestro wait <task-id>
```

## Production SKUs

| SKU | Price | Duration | Output | Languages | Capabilities |
|---|---:|---:|---|---:|---|
| `lite` | 0.20 Credits/second | 5–30s | 720p/24fps | 1 | auto/narrated/captions; generate/edit |
| `standard` | 0.60 Credits/second | 5–120s | 1080p/30fps | 2 | adds avatar and remix |
| `pro` | 1.20 Credits/second | 5–300s | 1080p/30fps | 4 | adds drama and extend |

Successful tasks are billed by delivered integer-second duration, with no 30-second minimum. Avatar uses a 1.15× multiplier, drama uses 1.35×, and each additional delivered language adds 6 Credits. Failed tasks and polling are free.
