"""Rich terminal output formatting for Discord Bot CLI."""

import json
from typing import Any

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


def print_error(message: str) -> None:
    """Print an error message."""
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message."""
    console.print(f"[bold green]\u2713[/bold green] {message}")


def print_health(data: dict[str, Any]) -> None:
    """Print health check result."""
    status = data.get("status", "unknown")
    gateway_ready = data.get("gateway_ready", False)
    color = "green" if status == "ok" and gateway_ready else "yellow"
    console.print(
        Panel(
            f"[bold]Status:[/bold] {status}\n"
            f"[bold]Gateway Ready:[/bold] {'[green]yes[/green]' if gateway_ready else '[red]no[/red]'}",
            title=f"[bold {color}]Health[/bold {color}]",
            border_style=color,
        )
    )


def print_whoami(data: dict[str, Any]) -> None:
    """Print account info."""
    account = data.get("data", data)
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")
    for key in ["id", "username", "discriminator", "global_name", "email"]:
        if account.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(account[key]))
    console.print(Panel(table, title="[bold green]Account Info[/bold green]", border_style="green"))


def print_guilds(data: dict[str, Any]) -> None:
    """Print guild list."""
    guilds = data.get("data", data)
    if not isinstance(guilds, list):
        guilds = [guilds]
    table = Table(title="Guilds", show_header=True, header_style="bold cyan")
    table.add_column("ID")
    table.add_column("Name")
    for guild in guilds:
        table.add_row(str(guild.get("id", "")), str(guild.get("name", "")))
    console.print(table)


def print_channels(data: dict[str, Any]) -> None:
    """Print channel list."""
    channels = data.get("data", data)
    if not isinstance(channels, list):
        channels = [channels]
    table = Table(title="Channels", show_header=True, header_style="bold cyan")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Type")
    for ch in channels:
        table.add_row(
            str(ch.get("id", "")),
            str(ch.get("name", "")),
            str(ch.get("type", "")),
        )
    console.print(table)


def print_members(data: dict[str, Any]) -> None:
    """Print member list."""
    members = data.get("data", data)
    if not isinstance(members, list):
        members = [members]
    table = Table(title="Members", show_header=True, header_style="bold cyan")
    table.add_column("ID")
    table.add_column("Username")
    table.add_column("Nick")
    for m in members:
        user = m.get("user", m)
        table.add_row(
            str(user.get("id", "")),
            str(user.get("username", "")),
            str(m.get("nick") or ""),
        )
    console.print(table)


def print_messages(data: dict[str, Any]) -> None:
    """Print message list."""
    messages = data.get("data", data)
    if not isinstance(messages, list):
        messages = [messages]
    table = Table(title="Messages", show_header=True, header_style="bold cyan")
    table.add_column("ID", width=20)
    table.add_column("Author", width=20)
    table.add_column("Content")
    for msg in messages:
        author = msg.get("author", {})
        username = author.get("username", "") if isinstance(author, dict) else str(author)
        table.add_row(
            str(msg.get("id", "")),
            username,
            str(msg.get("content", "")),
        )
    console.print(table)


def print_message(data: dict[str, Any]) -> None:
    """Print a single message result."""
    msg = data.get("data", data)
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")
    for key in ["id", "channel_id", "content", "timestamp"]:
        if msg.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(msg[key]))
    console.print(Panel(table, title="[bold green]Message[/bold green]", border_style="green"))


def print_dm_channel(data: dict[str, Any]) -> None:
    """Print DM channel info."""
    ch = data.get("data", data)
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", width=15)
    table.add_column("Value")
    for key in ["id", "type"]:
        if ch.get(key) is not None:
            table.add_row(key.replace("_", " ").title(), str(ch[key]))
    console.print(
        Panel(table, title="[bold green]DM Channel[/bold green]", border_style="green")
    )
