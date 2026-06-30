"""Allow running fish_cli as a module: python -m fish_cli."""

from fish_cli.main import cli

if __name__ == "__main__":
    cli()
