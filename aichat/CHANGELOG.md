# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-04-25

### Added

- Initial release of AiChat CLI
- `chat` command for AI dialogue via `/aichat/conversations`
- Support for all models: GPT-5.x, GPT-4.x, GPT-4o, o1/o3/o4, DeepSeek, Grok, GLM series
- Stateful conversation support with `--id` and `--stateful` flags
- Reference/context injection via `--reference` option
- Preset support via `--preset` option
- `models` command to list available models
- `config` command to show current configuration
- `--json` flag for machine-readable output
- Rich terminal formatting for human-readable output
- Docker support via Dockerfile and docker-compose.yaml
