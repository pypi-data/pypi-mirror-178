import typer

import nx.profile
import nx.nixos

app = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)
app.add_typer(nx.profile.app, name="profile")
app.add_typer(nx.nixos.app, name="os")


@app.callback()
def callback():
    """
    [bold]NX[/bold] is a fast and beautiful [bold blue]NixOS[/bold blue] and [bold blue]Nix[/bold blue] management
    utility [bold cyan]:snowflake:[/bold cyan]

    [bold]NX[/bold] supports operations that alter both [bold blue]NixOS[/bold blue] systems and [bold blue]Nix[/bold blue] profiles, for more info see the --help flag for the subcommands listed below

    [bold white]Alternatively, for documentation, see the [link=https://gitlab.com/mchal_/nx]GitLab repository[/link][/bold white]
    """
