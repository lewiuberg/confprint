"""Prefix printer is function factory for prefixing text."""

from collections import Counter
from types import ModuleType
from typing import Any, Callable

from click import echo

from confprint import _exceptions, err_print


global_count: Counter = Counter(n=-1, l=-1)


def prefix_printer(
    prefix: Any,
    stderr: bool = False,
    click: bool = False,
    upper: bool = True,
    frame_left: str = "[",
    frame_right: str = "]",
    counter_start: int = -1,
    global_counter: bool = False,
) -> Callable[[str], None]:
    """
    Prefix printer is function factory for prefixing text.

    Args:
        prefix (Any): The prefix to use.
        stderr (bool, optional):
            If True, the printer will print to sys.stderr instead of sys.stdout
            Defaults to False.
        click (bool, optional): If True, the printer will print to click.echo
            instead of sys.stdout. Defaults to False.
        upper (bool, optional): If True, the prefix will be printed in upper
        frame_left (str, optional): The left frame. Defaults to "[".
        frame_right (str, optional): The right frame. Defaults to "]".
        counter_start (int, optional): The counter start value. Defaults to -1.
        global_counter (bool, optional): If True, the counter will be global.

    Raises:
        _exceptions.PropertyError: Raised both stderr and click are True.

    Returns:
        Callable[[str], None]:
            A function that prints text prefixed with the prefix.
    """

    local_count: Counter = Counter(n=-1)

    if counter_start > -1 and not global_counter:
        local_count["n"] = counter_start
        count = local_count
    elif counter_start == -1 and global_counter:
        global_count["n"] = global_count["l"]
        count = global_count
    elif counter_start > -1 and global_counter:
        global_count["n"] = global_count["l"] = counter_start
        count = global_count

    def prefixed_printer(text: str = "", prefix: str = prefix) -> None:
        """
        Print text prefixed with the prefix.

        Args:
            text (str, optional): The text to print. Defaults to "".
            prefix (str, optional): The prefix to use. Defaults to prefix.

        Raises:
            _exceptions.PropertyError: Raised both stderr and click are True.
        """
        if upper and isinstance(prefix, str):
            prefix = prefix.upper()

        if counter_start > -1 and not global_counter:
            prefix = f"{frame_left}{prefix}:{count['n']}{frame_right}"
            count["n"] += 1
        elif counter_start > -1 and global_counter:
            prefix = f"{frame_left}{prefix}:{count['n']}{frame_right}"
            count["n"] += 1
            global_count["l"] += 1
        elif counter_start == -1 and global_counter:
            prefix = f"{frame_left}{prefix}:{count['n']}{frame_right}"
            count["n"] += 1
        else:
            prefix = f"{frame_left}{prefix}{frame_right}"

        if stderr and click:
            raise _exceptions.PropertyError(
                "stderr and click cannot be True at the same time"
            )
        elif stderr:
            # If stderr is True, print to stderr
            print_func: ModuleType = err_print
        elif click:
            print_func: ModuleType = echo  # type: ignore # mypy bug
        else:
            # If stderr and click are False, print to stdout
            print_func: Callable[[str], None] = print  # type: ignore # mypy bug # noqa: E501

        if "\n" in text:
            lines = text.split("\n")
            first_line_len = len(lines[0])
            lines[0] = f"{prefix}: {lines[0]}"
            indent_len = len(lines[0]) - first_line_len
            print_func(lines[0])  # type: ignore
            [print_func((" " * indent_len) + line) for line in lines[1:]]  # type: ignore # mypy bug # noqa: E501

        elif not text:
            print_func(f"{prefix}")  # type: ignore # mypy bug
        else:
            print_func(f"{prefix}: {text}")  # type: ignore # mypy bug

    return prefixed_printer
