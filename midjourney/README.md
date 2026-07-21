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
midjourney edits --image-url https://example.com/photo.jpg --prompt "Add mountains"
midjourney videos --prompt "A flowing river" --action generate
midjourney describe --image-url https://example.com/photo.jpg
midjourney shorten "A very long and detailed prompt that needs to be shortened"
midjourney translate "Una hermosa puesta de sol"
midjourney seed --image-id abc123
midjourney task abc123
```

## Configuration

Set your API token:

```bash
export ACEDATACLOUD_API_TOKEN=your_token
```

Or use the `--token` flag:

```bash
midjourney --token your_token imagine "A beautiful sunset"
```
