# Copilot Sync Instructions for AceDataCloud Clis

## Repository Structure

This is a monorepo with one CLI tool per subdirectory (e.g., `suno/`, `luma/`, `flux/`).
Each subdirectory contains a standalone Python CLI package.

## Source of Truth

The **AceDataCloud/Docs** repo is the source of truth:

- `openapi/<service>.json` — OpenAPI specs for each service
- `guides/<service>.md` — Usage guides (optional reference)

## What to Sync

When the Docs repo changes, compare the OpenAPI specs against the CLI code and update:

1. **Commands and subcommands** — ensure all API operations have corresponding CLI commands
2. **Command parameters/options** — match request body schemas from OpenAPI specs
3. **Endpoint paths** — verify API paths match the OpenAPI `paths` section
4. **Help text** — update descriptions to match OpenAPI operation summaries

## Rules

- Do NOT change the CLI framework or architecture patterns
- Do NOT modify CI/CD workflows or sync.yaml
- Keep backward compatibility: add new commands/options, don't remove existing ones unless the API removed them
- Each subdirectory is independent — only update directories for changed services
