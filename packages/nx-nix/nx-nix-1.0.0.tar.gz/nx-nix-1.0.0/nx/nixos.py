import typer

from platform import node

from nx.utils import continue_


app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def callback():
    """
    Commands that alter [bold blue]NixOS[/bold blue] systems
    """


@app.command()
def deploy(
    flake: str = typer.Argument(
        f".#{node()}", help="The Flake URI to deploy", envvar="NX_FLAKE"
    ),
    remote: str = typer.Option(
        "",
        "-r",
        "--remote",
        help="If a value is passed, attempt to SSH to the passed value and run the relevant command remotely",
    ),
    boot: bool = typer.Option(
        False,
        "-b",
        "--boot",
        help="If passed, runs [bold white]nixos-rebuild boot[/bold white] "
        + "instead of [bold white]nixos-rebuild switch[/bold white]. "
        + "Has no effect if --install is present",
    ),
    install: bool = typer.Option(
        False,
        "-i",
        "--install",
        help="If passed, runs [bold white]nixos-install[/bold white] instead of [bold white]nixos-rebuild[/bold white]",
    ),
    rollback: bool = typer.Option(
        False,
        "--rollback",
        help="Instead of rebuilding a new generation, rolls the system back to the previous one",
    ),
):
    """
    [bold]Quickly[/bold] and [bold]efficiently[/bold] deploy a [bold blue]NixOS[/bold blue] system from a [cyan]Flake [bold]:snowflake:[/bold][/cyan]

    - Defaults to current system, but can run remotely over SSH if --deploy is provided
    - Can install a NixOS ISO remotely using the NixOS default ISO's [bold white]sshd[/bold white]
    - Allows for rolling back to a previous generation instead of rebuilding

    [bold white]For documentation, see the [link=https://gitlab.com/mchal_/nx]GitLab repository[/link][/bold white]
    """
    if boot:
        mode = "boot"
    else:
        mode = "switch"

    if remote != "":
        if install:
            command = f"ssh [green]{remote}[/green] -- sudo nixos-install --flake [blue]{flake}[/blue]"
        else:
            if rollback:
                command = f"ssh [green]{remote}[/green] -- sudo nixos-rebuild [magenta]{mode}[/magenta] --rollback"
            else:
                command = (
                    f"ssh [green]{remote}[/green] -- sudo nixos-rebuild [magenta]{mode}[/magenta] --flake "
                    + f"[blue]{flake}[/blue]"
                )
    else:
        if rollback:
            command = f"sudo nixos-rebuild [magenta]{mode}[/magenta] --rollback"
        else:
            command = f"sudo nixos-rebuild [magenta]{mode}[/magenta] --flake [blue]{flake}[/blue]"

    continue_(command, default=False)


@app.command()
def gc(
    delete_old: bool = typer.Option(
        False,
        "-d",
        "--delete-old",
        help="Deletes old, currently unused Nix derivations from the store. Prevents future rollback",
    )
):
    """
    [bold]Shortcut[/bold] for quickly clearing the [bold]nix-store[/bold] cache
    """

    if delete_old:
        command = f"sudo nix-collect-garbage [red]--delete-old[/red]"
    else:
        command = f"sudo nix-collect-garbage"

    continue_(command, default=True)
