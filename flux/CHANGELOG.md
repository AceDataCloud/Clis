# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-01-21

### Added

- Initial release of Flux CLI
- `generate` command for text-to-image generation
- `edit` command for image editing with text prompts
- `task` command for querying task status
- `tasks` command for batch task queries
- `wait` command for polling task completion
- `models` command to list available Flux models
- `aspect-ratios` command to list available aspect ratios
- `config` command to show current configuration
- Support for all Flux models: flux-dev, flux-pro, flux-pro-1.1, flux-pro-1.1-ultra, flux-kontext-pro, flux-kontext-max
- `--json` flag for machine-readable output on all commands
- `--token` option and `ACEDATACLOUD_API_TOKEN` env var for authentication
- Rich terminal formatting for human-readable output
- Docker support via Dockerfile and docker-compose.yaml
