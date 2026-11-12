# Midjourney CLI

A command-line tool for Midjourney image and video generation via AceDataCloud API.

## Installation

```bash
pip install midjourney-pro-cli
```

## Usage

```bash
export ACEDATACLOUD_API_TOKEN=your_token

midjourney imagine "A beautiful sunset over the ocean"
midjourney imagine "A beautiful sunset over the ocean" --version 8.2
midjourney edits --image-url https://example.com/photo.jpg --prompt "Add mountains"
midjourney videos --prompt "A flowing river" --action generate
midjourney describe --image-url https://example.com/photo.jpg
midjourney shorten "A very long and detailed prompt that needs to be shortened"
midjourney translate "Una hermosa puesta de sol"
midjourney seed --image-id abc123
midjourney task abc123
```

For Imagine, select a version with `--version` (the API's `version` field), not
`--model`. Omit `--version` to keep the API default. The Python client rejects any
`model` key, including `""` or `None`, before sending an Imagine request. Requests
sent directly to the API with `model` (including `""` or `null`) return HTTP 400
`bad_request` before generation or asynchronous acceptance, without charging.
Remove `model` rather than setting it to an empty value.

## Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or use the `--token` flag:

```bash
midjourney --token your_token imagine "A beautiful sunset"
```
