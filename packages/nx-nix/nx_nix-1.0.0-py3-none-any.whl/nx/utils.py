import re
import subprocess
import sys

import typer

from pathlib import Path

import randomname

from rich import print


def info(text: str):
    print(f"[bold blue]:snowflake:[/bold blue] {text}")


def abort(text: str):
    print(f"[bold yellow]:warning:[/bold yellow] [yellow]Aborting: {text}[/yellow]")
    exit(1)


def warn(text: str):
    print(f"[bold yellow]![/bold yellow] {text}")


def format_list(list_: list, idx: int):
    text = ""

    for (i, element) in enumerate(list_):
        if i == idx:
            text += f"\n  [bold cyan]•[/bold cyan] {element}"
        else:
            text += f"\n  [bold cyan]◦[/bold cyan] {element}"

    return text


def crash(command: str, log: str, code: int):
    print(
        "\n"
        + f"[bold red]X[/bold red] [red]Command [bold white]{command}[/bold white] returned a non-zero exit code.\n  "
        + f"A full output log can be found at:[/red]\n  [bold red]{log}[/bold red]"
    )
    exit(code)


def continue_(command: str, default: bool = False):
    info("NX will run the following command:")
    info(command)

    prompt = typer.confirm("  Continue?", default=default)

    if not prompt:
        abort("User cancelled operation")

    command = re.sub(r"\[[a-z]*\]|\[\/[a-z]*\]", "", command)

    app_path = Path(typer.get_app_dir("nx"))
    log_name = randomname.get_name()
    app_path.mkdir(parents=True, exist_ok=True)

    log_path = app_path / (log_name + ".log")
    log_file = open(log_path, "w")

    print(command)

    result = subprocess.Popen(
        command.split(" "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for line in result.stdout:
        sys.stdout.write(line.decode("utf-8"))
        log_file.write(line.decode("utf-8"))

    result.wait()
    log_file.close()

    if result.returncode != 0:
        crash(command, log_path, result.returncode)

    print(
        ":rocket: Operation successful! Thank you for using [link=https://github.com/mchal_/nx]NX[/link]!\n   "
        + f"The log for this operation is available at {log_path}"
    )
    exit(0)
