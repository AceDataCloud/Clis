# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2026-04-30

### Added
- `chat` command: new options `--max-completion-tokens`, `--top-p`, `--frequency-penalty`, `--presence-penalty`, `--seed`, `--stop`, `--reasoning-effort`, `--user`, `--service-tier`
- `edit` command: new options `--mask-url`, `--partial-images`
- `response` command: new options `--count` (`-n`), `--response-format`

## [0.1.0] - 2025-04-25

### Added
- Initial release
- `chat` command for OpenAI-compatible chat completions
- `embed` command for text embeddings
- `image` command for image generation
- `edit` command for image editing
- `response` command for Responses API
- `models` info command listing available models
- `config` command to inspect current settings
