from configparser import SectionProxy
from datetime import date
from itertools import zip_longest
from typing import Callable, Any, Optional

from rich.console import Console
from rich.table import Table

from mum.constants import MAP_INT_TO_WEEKDAY
from mum.enums import CommandEnum, Section
from mum.todo_file import TodoFile


MAP_COMMAND_TO_FUNC: dict[str, Callable[[Any], Any]] = {}


def map_command(command: Optional[str | Callable] = None) -> Callable:
    def _add_command_function(command_func: Callable) -> Callable:
        if callable(command) or command is None:
            command_name_ = command_func.__name__.strip("_")
        else:
            command_name_ = command

        MAP_COMMAND_TO_FUNC[command_name_] = command_func
        return command_func

    if callable(command):
        return _add_command_function(command)

    return _add_command_function


class Command:
    def __init__(self, todo_file: TodoFile, command: str, console: Console) -> None:
        self._todo_file = todo_file
        self._command: list[str] = command.split(" ")
        self._console = console

    def _ls_all(self, table: Table) -> None:
        for name in [member.lower().capitalize() for member in Section]:
            table.add_column(name)

        result = []
        for section in [self._todo_file.get_section(member) for member in Section]:
            row = []
            for value in section.values():
                row.append(value)
            result.append(row)

        for row in zip_longest(*result):
            table.add_row(*row)

    def _ls_logic(self, tail: list[str], table: Table) -> bool:
        if not tail:
            self._ls_all(table)
            return True

        commands = [section.lower().capitalize() for section in Section]
        fst_command = tail[0].lower().capitalize()
        if fst_command not in commands:
            return False

        table.add_column(fst_command)
        section = self._todo_file.get_section(Section[fst_command.lower()])
        for key, value in section.items():
            if fst_command == Section.todo.value.lower().capitalize():
                table.add_row(f"{key}: {value}")
                continue
            table.add_row(value)

        return True

    @map_command
    def _ls(self, tail: list[str]) -> bool:
        table = Table()
        if self._ls_logic(tail, table):
            self._console.print(table)
            return True

        return False

    @map_command
    def _rst(self) -> bool:
        self._todo_file.bootstrap_todo_file()
        return True

    @staticmethod
    def _max_section_number(section: SectionProxy) -> int:
        return int(max(sorted(section.keys()))) if section else 0

    @map_command
    def _dn(self, tail: list[str]) -> bool:
        command_text = " ".join(tail)
        if not command_text:
            return False

        day = MAP_INT_TO_WEEKDAY[date.today().weekday()]
        day_section = self._todo_file.get_section(Section[day])
        day_section[str(self._max_section_number(day_section) + 1)] = command_text
        self._todo_file.write_config_to_file()
        return True

    @map_command
    def _td(self, tail: list[str]) -> bool:
        if not tail:
            return False

        if tail[0] == "dn":
            if len(tail) != 2 or not tail[1].isnumeric():
                return False

            removed = (
                self._todo_file.get_section(Section.todo).pop(tail[1], None).split(" ")
            )
            return self._dn(removed)

        section = self._todo_file.get_section(Section.todo)
        section[str(self._max_section_number(section) + 1)] = " ".join(tail)
        self._todo_file.write_config_to_file()
        return True

    def run_command(self) -> bool:
        fst_command = self._command[0].lower()
        command_func = MAP_COMMAND_TO_FUNC.get(fst_command)
        if command_func is None:
            return False

        tail = self._command[1 : len(self._command)]
        if tail or fst_command == CommandEnum.ls:
            return command_func(self, tail)  # type: ignore

        return command_func(self)
