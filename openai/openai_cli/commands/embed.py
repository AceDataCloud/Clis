"""Text embedding command."""

import click

from openai_cli.core.client import get_client
from openai_cli.core.exceptions import OpenAIError
from openai_cli.core.output import (
    DEFAULT_EMBEDDING_MODEL,
    EMBEDDING_MODELS,
    print_embedding_result,
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
    show_default=True,
    help="Embedding model to use.",
)
@click.option(
    "--encoding-format",
    type=click.Choice(["float", "base64"]),
    default="float",
    show_default=True,
    help="Format of the returned embeddings.",
)
@click.option(
    "--dimensions",
    default=None,
    type=int,
    help="Output embedding size (when supported by the model).",
)
@click.option("--json", "output_json", is_flag=True, help="Output raw JSON.")
@click.pass_context
def embed(
    ctx: click.Context,
    text: str,
    model: str,
    encoding_format: str,
    dimensions: int | None,
    output_json: bool,
) -> None:
    """Generate text embeddings.

    TEXT is the input string to embed.

    \b
    Examples:
      openai-cli embed "Hello, world!"
      openai-cli embed "Semantic search query" -m text-embedding-3-large
      openai-cli embed "Document text" --dimensions 256
    """
    client = get_client(ctx.obj.get("token"))
    payload: dict[str, object] = {
        "model": model,
        "input": text,
        "encoding_format": encoding_format,
        "dimensions": dimensions,
    }

    try:
        result = client.embeddings(**payload)  # type: ignore[arg-type]
        if output_json:
            print_json(result)
        else:
            print_embedding_result(result)
    except OpenAIError as e:
        print_error(e.message)
        raise SystemExit(1) from e
