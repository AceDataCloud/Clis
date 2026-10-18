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

# One-shot voice clone (does not create a saved model)
fish tts "New speech" \
  --reference-audio-url https://cdn.acedata.cloud/reference.mp3 \
  --reference-text "The exact reference transcript"

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

## Saved voice model queries

```bash
# List voices created and saved through AceDataCloud by your account
fish models --self --page-size 5 --page-number 1 --json

# Filter the public voice library by title language
fish models --title-language en --sort-by created_at --json
```

`--self` lists voices created through this platform by the calling account,
including voices created with other API tokens belonging to that account. It
paginates in descending creation order; `--author-id` can further filter those
voices by author ID. With `--self`, `--sort-by` supports `created_at` and
`task_count`. `--title-language` is only supported for public-library queries,
not with `--self`.

Voices created through the platform's model-creation API are saved publicly
long-term and may be searched for and used by other users. Requesting `private`
or `unlist` visibility does not change that public scope. `--self` only filters
the list; it does not make voices private.

Raw `--json` list output includes `total`, `items`, and `has_more`. For `--self`,
`has_more` is a boolean; public-library queries may return `null`. Use
`--page-size` and `--page-number` to paginate, using `total` when `has_more` is
`null`.

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


## Voice cloning modes

- Use `--reference-id` for a saved or public voice that will be reused.
- Use `--reference-audio-url` with `--reference-text` for a one-shot clone. The HTTPS MP3/WAV reference should be 10–270 seconds.
- Do not combine the two modes. Billing remains based on the target text's UTF-8 byte count.
