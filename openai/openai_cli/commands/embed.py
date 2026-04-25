"""Embeddings commands."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_EMBEDDING_MODEL,
    EMBEDDING_MODELS,
    print_embed_result,
    print_error,
    print_json,
)


@click.command()
@click.argument("text")
@click.option(
    "-m",
    "--model",
    type=click.Choice(EMBEDDING_MODELS),
    default=DEFAULT_EMBEDDING_MODEL,
    help="Embedding model to use.",
)
@click.option(
    "--dimensions",
    type=int,
    default=None,
    help="Output embedding dimensions (when supported by the model).",
)
@click.option(
    "--encoding-format",
    type=click.Choice(["float", "base64"]),
    default=None,
    help="Format of the returned embeddings (default: float).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def embed(
    ctx: click.Context,
    text: str,
    model: str,
    dimensions: int | None,
    encoding_format: str | None,
    output_json: bool,
) -> None:
    """Create an embedding vector for the given text.

    TEXT is the input string to embed.

    \b
    Examples:
      openai embed "The quick brown fox"
      openai embed "Hello world" -m text-embedding-3-large
      openai embed "Sample text" --dimensions 256
    """
    client = get_client(ctx.obj.get("token"))
    try:
        payload: dict[str, object] = {
            "model": model,
            "input": text,
            "dimensions": dimensions,
            "encoding_format": encoding_format,
        }

        result = client.embed(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_embed_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e
