# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-04-25

### Added

- Initial release of AiChat CLI
- `chat` command to send questions to large language models
- `models` command to list all available models
- `config` command to show current configuration
- Support for conversation continuation via `--id`
- Support for stateful conversations via `--stateful`
- Support for references/context documents via `--ref`
- Support for preset models via `--preset`
- `--json` flag for machine-readable output on all commands
- Rich terminal formatting for human-readable output
- Docker support via Dockerfile and docker-compose.yaml
