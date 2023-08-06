import glob
import os
import shutil
import subprocess

import typer

from os import path
from os import getlogin
from os import readlink
from os import listdir

from nx.utils import info, abort, continue_, warn, format_list

app = typer.Typer(rich_markup_mode="rich")


@app.callback()
def callback():
    """
    Commands that alter [bold blue]Nix[/bold blue] profiles
    """


@app.command()
def install(
    flake: str = typer.Option(
        "nixpkgs", "-f", "--flake", help="The Flake to install from"
    ),
    output: str = typer.Argument(..., help="The Flake output to install"),
    profile: str = typer.Option(
        "", "-p", "--profile", help="The profile to update", envvar="NX_PROFILE"
    ),
):
    """
    [bold]Simple[/bold] helper command for installing [cyan]Flake [bold]:snowflake:[/bold][/cyan] outputs to your [bold blue]Nix[/bold blue] profile

    - Custom Flakes (other than Nixpkgs) can be selected using the --flake option
    - Allows specifying a different Nix profile

    [bold white]For documentation, see the [link=https://gitlab.com/mchal_/nx]GitLab repository[/link][/bold white]
    """

    if not profile == "":
        command = (
            f"nix profile install [blue]{flake}[/blue][grey]#[/grey][green]{output}[/green] --profile "
            + f"[magenta]{profile}[/magenta]"
        )
    else:
        command = f"nix profile install [blue]{flake}[/blue][grey]#[/grey][green]{output}[/green]"

    continue_(command, default=True)


@app.command()
def remove(
    package: str = typer.Argument(
        ..., help="The name of the package to remove from the current Nix profile"
    ),
    profile: str = typer.Option(
        "", "-p", "--profile", help="The profile to update", envvar="NX_PROFILE"
    ),
):
    """
    [bold]Simple[/bold] helper command for removing [cyan]Flake [bold]:snowflake:[/bold][/cyan] outputs from your [bold blue]Nix[/bold blue] profile

    - Uses a REGEX search to remove only packages with PACKAGE as the final element (e.g, if PACKAGE is "hello", it will delete legacyPackages.x86_64-linux.hello but NOT other-output.hello.something else)
    - Allows specifying a different Nix profile

    [bold white]For documentation, see the [link=https://gitlab.com/mchal_/nx]GitLab repository[/link][/bold white]
    """

    if not profile == "":
        command = f"nix profile remove [green].*\\.{package}[/green] --profile [magenta]{profile}[/magenta]"
    else:
        command = f"nix profile remove [green].*\\.{package}[/green]"

    continue_(command, default=False)


@app.command()
def switch(
    profile: str = typer.Argument(..., help="The name of the profile to operate on"),
    create: bool = typer.Option(
        False,
        "-c",
        "--create",
        help="If profile is not found, create it before switching to it",
    ),
    delete: bool = typer.Option(
        False,
        "--delete",
        help="Delete profile instead of switching to it (Use with caution, this cannot be undone!)",
    ),
):
    """
    [bold]Simple[/bold] helper command for switching to/creating [bold blue]Nix[/bold blue] profiles

    - Allows for creation of a new profile if supplied profile is not found
    - Allows for deleting a profile if no longer necessary
      - Safety checks to make sure you don't delete the current or default profile

    [bold yellow]:warning: This feature might cause issues if you manage your environment using [link=https://github.com/nix-community/home-manager]home-manager[/link][/bold yellow]
      [bold yellow]If you end up somehow losing anything from your current [bold blue]home-manager[/bold blue] config, follow the instructions [link=https://gitlab.com/mchal_/nx/-/wikis/Restoring-the-home-manager-Environment]here[/link]
    """

    user = getlogin()
    profile_path = f"/nix/var/nix/profiles/per-user/{user}/{profile}"
    exists = path.exists(profile_path)

    if delete:
        if readlink(f"/home/{user}/.nix-profile") == profile_path:
            abort("Cannot delete current profile")

        if profile == "profile":
            abort("Cannot delete default profile")

        info(f'Deleting profile "{profile}" for user "{user}"...')
        warn(
            "Deleting a profile does not delete its relevant /nix/store entries. "
            + "It's recommended you run [bold]nx os gc[/bold] after the operation to remove these"
        )

        command = f'rm -rf {profile_path} [magenta]{" ".join(glob.glob(f"/nix/var/nix/profiles/per-user/{user}/{profile}-*-link"))}[/magenta]'

        continue_(command, default=False)

    if not exists and not create:
        abort(
            f'Profile "{profile}" not found for user "{user}" and [cyan]--create[/cyan] not passed'
        )

    if not exists and create:
        info(f'Profile "{profile}" not found for user "{user}", creating...')

    command = f"nix-env --switch-profile {profile_path}"

    continue_(command, default=False)


@app.command(name="info")
def info_(
    list_profiles: bool = typer.Option(
        False, "-l", "--list-profiles", help="Lists installed profiles"
    )
):
    """
    Returns information about the currently active [bold blue]Nix[/bold blue] profile
    """

    user = getlogin()
    profile = readlink(f"/home/{user}/.nix-profile")
    profile_name = path.basename(profile)
    join_ = "\n  [bold cyan]◦[/bold cyan] "

    profile_list = [
        x
        for x in map(path.basename, listdir(f"/nix/var/nix/profiles/per-user/{user}"))
        if not x.endswith("link")
    ]

    if list_profiles:
        profile_text = (
            f"Profiles:{format_list(profile_list, profile_list.index(profile_name))}"
        )
    else:
        profile_text = f"Profiles Count: {len(profile_list)}"

    info(
        f"Current Profile: [bold]{profile_name}[/bold]\n  "
        + f"Profile Path: {str(profile)}\n  "
        + f'Installed Packages: {len(subprocess.check_output(["nix", "profile", "list"]).splitlines())}\n  '
        + profile_text
    )
