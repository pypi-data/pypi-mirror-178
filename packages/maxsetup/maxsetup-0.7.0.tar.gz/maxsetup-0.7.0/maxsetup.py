from __future__ import annotations

from inspect import currentframe, getframeinfo
from pathlib import Path
from shutil import copytree, ignore_patterns, rmtree
from typing import Optional

from loguru import logger as log
import loguru
from loguru import _logger
from maxcolor import gradient, gradient_panel
from maxconsole import get_console, get_theme
from maxprogress import get_progress
from rich.console import Console
from rich.traceback import install as install_rich_traceback

__version__ = '0.6.0'

console = get_console(get_theme())
progress = get_progress(console)

CWD = Path.cwd()
LOG_DIR = CWD / "logs"
RUN = CWD / "logs" / "run.txt"
VERBOSE_LOG = CWD / "logs" / "verbose.log"
LOG = CWD / "logs" / "log.log"
TEMPLATE = Path("/Users/maxludden/dev/template")

# ───────────── Set Up File Structure ─────────────────────────

def _create_files() -> None:
    """Copy files from the template folder to the current working directory."""
    if (CWD / "logs" / "run.txt").exists():

        # Read pyproject.toml into active memory
        TOML = CWD / 'pyproject.toml'
        with open (TOML, 'r') as infile:
            PYPROJECT = infile.read()
            console.log(
                gradient(f'Read [bold bright_white]pyproject.toml[/] into active memory.'),
                log_locals=True
            )
        
        # Read poetry.lock into active memory
        LOCK = CWD / 'poetry.lock'
        with open (LOCK, 'r') as infile:
            POETRY = infile.read()
            console.log(
                gradient(f'Read [bold bright_white]poetry.lock[/] into active memory.'),
                log_locals=True
            )

        # Clear current working directory    
        rmtree(CWD)
        console.log(
            "[bold red]Removed the [/][bold bright_cyan]CWD[/] [bold red]file structure.[/]"
        )

        # Write pyproject.toml back into CWD
        with open (TOML, 'w') as outfile:
            outfile.write(PYPROJECT)

        # Write poetry.lock back into CWD
        with open (LOCK, 'w') as outfile:
            outfile.write(POETRY)

        console.log(
            "Saved [bold bright_white]pyproject.toml[/] and [bold bright_white]poetry.lock[\] back to the [bold purple1]CWD[/]"
        )

        # Copy file structure from template directory into current directory
        copytree(
            TEMPLATE, CWD, ignore=ignore_patterns("*.pyc", "venv", "__pycache__", ".py")
        )
        console.print("")
        console.print(
            gradient_panel(
                "Created file structure from template directory.", 
                title="Created File Structure",
                justify_text='center'
            ),
            justify="center",
        )


# ─────────────────── Run ─────────────────────────────────

def _get_last_run() -> int:
    """Get the last run number from the run.txt file. If the run.text file doesn't exist, re-create the entire file structure."""
    if not RUN.exists():
        _create_files()
    with open("logs/run.txt", "r") as infile:
        last_run = int(infile.read())
        # console.log(f"Last Run: {last_run}")
        return last_run



def _increment_run(last_run: int) -> int:
    """Update the run.txt file with the next run number."""
    return last_run + 1



def _record_run(current_run: int) -> None:
    """Write the current run number to disk.add()

    Args:
        current_run (`int``): The current run number.
    """
    with open (RUN, 'w') as run_file:
        run_file.write(f"{current_run}")



# ──────────────────── Log Sinks  ───────────────────────────────
def setup_loguru_sinks (current_run: int, console: Console=console) -> _logger:
    """Set up the Loguru logger and generate the logger sinks.

    Args:
        current_run (`int`): The current run number with with to bind the sinks to.
        console (`Console`): The console with which to log to.

    Returns:
        log (`logger`): A Loguru logger with custom sinks.
    """
    sinks = log.configure(
        handlers=[
            dict(  # . debug.log
                sink=f"{VERBOSE_LOG}",
                level="DEBUG",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
                rotation="10 MB",

            ),
            dict(  # . info.log
                sink=f"{LOG}",
                level="INFO",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: <8}ﰲ  {message}",
                rotation="10 MB",
            ),
            dict(  # . Rich Console Log > INFO
                sink=(lambda msg: console.log(f"[#aaaaaa]{msg}[/]", markup=True, highlight=True, log_locals=False)),
                level="DEBUG",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
            dict(  # . Rich Console Log > INFO
                sink=(lambda msg: console.log(f"[#47c8ff]{msg}[/]", markup=True, highlight=True, log_locals=False)),
                level="INFO",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
            dict(  # . Rich Console Log > ERROR
                sink=(lambda msg: console.log(f"[bold reverse red]msg[/]", markup=True, highlight=True, log_locals=True)),
                level="ERROR",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
        ],
        extra={
            "run": current_run, # > Current Run
        },  
        patcher=lambda record: record["extra"]
    )
    log = log.bind(

    )
    return log


def new_run(console: Console=console) -> loguru._logger:
    """Start a new run. Generate the file structure, log files, and `run.txt` to keep track of runs if they do not exist. Read the last run, increment it, save the new integer to disk, and then clear the console and print the current run to the console as a horizontal rule.

    Args:
        console (`Console`): The console with which to work with.

    Returns:
        log (`loguru._logger`): The Loguru Logger.
    """
    console.clear() # Clear the console of the activated environment sourcing.

    # Retrieve, increment, and record the run number.
    run = _increment_run(_get_last_run())
    _record_run(run)

    # Sinks
    log = setup_loguru_sinks(run, console)

    # Print the current run number to the console as a horizontal rule with gradient text.
    console.rule(
        title = gradient(f"Run {run}"),
        style = "bold bright_white"
    )
    return log

    