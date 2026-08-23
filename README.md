# AceDataCloud CLIs

Monorepo for all AceDataCloud command-line interface tools.

## CLIs

| Directory | Standalone Repo | Description |
|---|---|---|
| `luma/` | [LumaCli](https://github.com/AceDataCloud/LumaCli) | Luma video generation CLI |
| `suno/` | [SunoCli](https://github.com/AceDataCloud/SunoCli) | Suno music generation CLI |
| `sora/` | [SoraCli](https://github.com/AceDataCloud/SoraCli) | Sora video generation CLI |
| `veo/` | [VeoCli](https://github.com/AceDataCloud/VeoCli) | Veo video generation CLI |
| `nanobanana/` | [NanoBananaCli](https://github.com/AceDataCloud/NanoBananaCli) | NanoBanana image generation CLI |
| `seedance/` | [SeedanceCli](https://github.com/AceDataCloud/SeedanceCli) | Seedance video generation CLI |
| `qwen-image/` | [QwenImageCli](https://github.com/AceDataCloud/QwenImageCli) | [qwen-image-cli](https://pypi.org/project/qwen-image-cli/) | Image |
| `seedream/` | [SeedreamCli](https://github.com/AceDataCloud/SeedreamCli) | Seedream image generation CLI |
| `flux/` | [FluxCli](https://github.com/AceDataCloud/FluxCli) | Flux image generation & editing CLI |
| `serp/` | [SerpCli](https://github.com/AceDataCloud/SerpCli) | Google SERP (Search) CLI |
| `wan/` | [WanCli](https://github.com/AceDataCloud/WanCli) | Tongyi Wansiang video generation CLI |
| `adc/` | [AceDataCloudCli](https://github.com/AceDataCloud/AceDataCloudCli) | Unified AceDataCloud CLI (all services) |
| `aichat/` | [AiChatCli](https://github.com/AceDataCloud/AiChatCli) | AI Dialogue CLI |
| `glm/` | [GLMCli](https://github.com/AceDataCloud/GLMCli) | GLM chat completions CLI |
| `hailuo/` | [HailuoCli](https://github.com/AceDataCloud/HailuoCli) | Hailuo video generation CLI |
| `kling/` | [KlingCli](https://github.com/AceDataCloud/KlingCli) | Kling video generation CLI |
| `openai/` | [OpenAICli](https://github.com/AceDataCloud/OpenAICli) | OpenAI-compatible API CLI |
| `producer/` | [ProducerCli](https://github.com/AceDataCloud/ProducerCli) | Producer music generation CLI |
| `webextrator/` | [WebExtratorCli](https://github.com/AceDataCloud/WebExtratorCli) | Web extraction and rendering CLI |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.
