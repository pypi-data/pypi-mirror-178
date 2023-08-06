# maxlog.py
from pathlib import Path

from rich.console import Console
from loguru import logger as log
from loguru import _logger
from maxconsole import get_console, get_theme
from maxprogress import get_progress
from maxcolor import gradient, gradient_panel

console = get_console(get_theme())
progress = get_progress(console)

CWD = Path.cwd()
LOG_DIR = CWD / "logs"
RUN = CWD / "logs" / "run.txt"
VERBOSE_LOG = CWD / "logs" / "verbose.log"
LOG = CWD / "logs" / "log.log"

def file_exists(file: str, exists: bool, is_directory: bool = False) -> None:
    """Logs whether or not a directory or file exists to console.
    
    Args:
        file (`str`): The file or folder about which to log.
        is_directory (`bool`): Whether `file` is a directory or a file.
        exists (`bool`): Whether `file` exists.
    """
    if is_directory:
        file_type = 'directory'
    else:
        file_type = 'file'

    if exists:
        console.log(f"[#ffffff]The {file_type},[/#ffffff] [bold bright_white]{file}[/bold bright_white], already exists")
    else:
        if file_type == 'directory':
            console.log(f"[#00ff00]Created[/#00ff00] [bold bright_white]{file}[/bold bright_white] [#999999]directory.[/#999999]")
        else:
            console.log(f"[#00ff00]Created[/#00ff00] [bold bright_white]{file}.[/bold bright_white]")


def make_files() -> None:
    """Create the logs directory along with generating the log files and  `run.txt` to keep track of run count.
    """
    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_exists("logs", False, True)
    else:
        file_exists("logs", True, True)

    if not RUN.exists():
        with open(RUN, 'w') as outfile:
            outfile.write("0")
        file_exists("run.txt",False)
    else:
        file_exists("run.txt", True)

    if not VERBOSE_LOG.exists():
        with open(VERBOSE_LOG, 'w') as outfile:
            outfile.write("")
        file_exists("verbose.log", False)
    else:
        file_exists("verbose.log", True)

    if not LOG.exists():
        with open(LOG, 'w') as outfile:
            outfile.write("")
        file_exists("log.log", False)
    else:
        file_exists("log.log", True)


def get_run() -> int:
    """Create the Logs directory if it does not exist and read the last run number.

    Returns:
        last_run (`int`): The last run number.
    """
    if not RUN.exists():
        make_files()
    with open (RUN, 'r') as run_file:
        last_run = int(run_file.read())
        return last_run


def increment_run(last_run: int) -> int:
    """Increment the last run to get the current run number.

    Args:
        last_run (`int``): The last run number.

    Returns:
        current_run (`int`): The current run number.
    """
    return last_run + 1


def record_run (current_run: int) -> None:
    """Record the current run number to disk.add()

    Args:
        current_run (`int`): The current run number.
    """
    with open (RUN, 'w') as run_file:
        run_file.write(f"{current_run}")


def get_log(current_run: int) -> _logger:
    """Set up the Loguru logger and generate the logger sinks.
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
                sink=(
                    lambda msg: console.log(
                        msg, markup=True, highlight=True, log_locals=False
                    )
                ),
                level="INFO",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
            dict(  # . Rich Console Log > ERROR
                sink=(
                    lambda msg: console.log(
                        msg, markup=True, highlight=True, log_locals=True
                    )
                ),
                level="ERROR",
                format="Run {extra[run]} | {time:hh:mm:ss:SSS A} | {file.name: ^13} |  Line {line: ^5} | {level: ^8} ﰲ  {message}",
                diagnose=True,
                catch=True,
                backtrace=True,
            ),
        ],
        extra={"run": current_run},  # > Current Run
    )
    return log


def new_run(console: Console=console) -> _logger:
    """Start a new run. Generate the file structure, log files, and `run.txt` to keep track of runs if they do not exist. Read the last run, increment it, save the new integer to disk, and then clear the console and print the current run to the console as a horizontal rule.

    Args:
        current_run (`int`): The current run number.

    Returns:
        int: the current run number
    """
    console.clear() # Clear the console of the activated environment sourcing.

    # Retrieve, increment, and record the run number.
    run = increment_run(get_run())
    record_run(run)

    # Print the current run number to the console as a horizontal rule with gradient text.
    console.rule(
        title = gradient(f"Run {run}"),
        style = "bold bright_white"
    )
    return get_log(run)

log = new_run()