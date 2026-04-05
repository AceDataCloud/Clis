# AceDataCloud CLIs

Monorepo for all AceDataCloud command-line interface tools.

## CLIs

| Directory | Standalone Repo | Description |
|---|---|---|
| `midjourney/` | [MidjourneyCli](https://github.com/AceDataCloud/MidjourneyCli) | Midjourney image & video generation CLI |
| `luma/` | [LumaCli](https://github.com/AceDataCloud/LumaCli) | Luma video generation CLI |
| `suno/` | [SunoCli](https://github.com/AceDataCloud/SunoCli) | Suno music generation CLI |
| `sora/` | [SoraCli](https://github.com/AceDataCloud/SoraCli) | Sora video generation CLI |
| `veo/` | [VeoCli](https://github.com/AceDataCloud/VeoCli) | Veo video generation CLI |
| `nanobanana/` | [NanoBananaCli](https://github.com/AceDataCloud/NanoBananaCli) | NanoBanana image generation CLI |
| `seedance/` | [SeedanceCli](https://github.com/AceDataCloud/SeedanceCli) | Seedance video generation CLI |
| `seedream/` | [SeedreamCli](https://github.com/AceDataCloud/SeedreamCli) | Seedream image generation CLI |
| `flux/` | [FluxCli](https://github.com/AceDataCloud/FluxCli) | Flux image generation & editing CLI |
| `serp/` | [SerpCli](https://github.com/AceDataCloud/SerpCli) | Google SERP (Search) CLI |
| `wan/` | [WanCli](https://github.com/AceDataCloud/WanCli) | Tongyi Wansiang video generation CLI |
| `adc/` | [AdcCli](https://github.com/AceDataCloud/AdcCli) | Unified AceDataCloud CLI (all services) |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.
