from __future__ import annotations
import argparse
import datetime
import os
import signal
import sys
import time
from typing import Any

try:
    import readline
except ImportError:
    import pyreadline3 as readline

from inteltk.colors import *


class IntelTk:
    def __init__(self, commands: dict[str, dict[str, function | str]], cookie_path: str) -> None:
        self.META_COMMANDS = {
            "cookies": {
                "func": self._delete_cookies,
                "desc": "\t\t\t(meta) Delete cookies",
            },
            "exit": {
                "func": self._exit_program,
                "desc": "\t\t\t(meta) Exits the program"
            },
            "list": {
                "func": self._list_commands,
                "desc": "\t\t\t(meta) Shows all commands"
            },
        }
        self.COMMANDS = {**self.META_COMMANDS, **commands}
        self.path = cookie_path

    def _completer(self, text: str, state: int) -> list[str] | None:
        if options := [x for x in self.COMMANDS if x.startswith(text)]:
            return options[state]
        return None

    def _delete_cookies(self) -> None:
        os.remove(self.path)

    def _exit_program(*_: Any) -> None:
        printcolor("\nGoodbye!", RED)
        sys.exit(0)

    def _list_commands(self) -> None:
        printcolor("Commands:", BLUE)
        for cmd, data in self.COMMANDS.items():
            printcolor(f"{cmd}{data['desc']}", WHITE)


def calculate_remaining_time(start_time: int, idx: int, total: int) -> str:
    return str(datetime.timedelta(seconds=round(((time.time() - start_time) / (idx + 1)) * (total - (idx + 1)))))


def create_parser(logo) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=50),
        description=logo
    )


def set_exit_program(func):
    signal.signal(signal.SIGINT, func)


def set_readline(func):
    readline.parse_and_bind("tab: complete")
    readline.set_completer(func)
    readline.set_completer_delims("")


def startup(logo: str, version: str, description: str, json: bool, txt: bool) -> None:
    printcolor(logo, BLUE)
    printcolor(f"Version {version} - {description}", BLUE)
    printcolor(f"Type {WHITE}json=y{RESET} to save results to json")
    printcolor(f"Type {WHITE}json=n{RESET} to disable saving to json")
    printcolor(f"Type {WHITE}txt=y{RESET} to save results to txt")
    printcolor(f"Type {WHITE}txt=n{RESET} to disable saving to txt")
    printcolor(f"Type {WHITE}list{RESET} to show all commands")
    printcolor((f"JSON output: {GREEN if json else RED}{json}{RESET}, "
                f"Txt output: {GREEN if txt else RED}{txt}"), BLUE)
