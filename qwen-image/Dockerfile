FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY qwen_image_cli/ qwen_image_cli/

RUN pip install --no-cache-dir .

ENTRYPOINT ["qwen-image-cli"]
