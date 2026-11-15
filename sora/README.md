# Sora CLI — retired

The Ace Data Cloud Sora integration is retired and is no longer available in the public API catalog. This directory and the SoraCli mirror retain historical source only. Previously published `sora-pro-cli` packages are not an active video-generation integration.

Do not install this CLI for a new workflow. The old commands, model list and configuration remain in source and Git history for reference; they do not indicate current service availability.

## Migrate an existing workflow

Review the current video services and their pricing in the [Ace Data Cloud catalog](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=sora_cli_retirement). Available alternatives have separate CLI packages and API contracts:

- [Seedance CLI](https://github.com/AceDataCloud/SeedanceCli)
- [Kling CLI](https://github.com/AceDataCloud/KlingCli)
- [Veo CLI](https://github.com/AceDataCloud/VeoCli)

Choose and configure the replacement explicitly. These packages are not drop-in replacements and may have different request parameters, limits and prices.

For an unresolved historical task, keep its task ID and trace ID and contact Ace Data Cloud support.

## Source maintenance

This directory is maintained in the [AceDataCloud/Clis monorepo](https://github.com/AceDataCloud/Clis/tree/main/sora) and mirrored to SoraCli. The source is retained to inspect past behavior, not to advertise a supported service.
