"""Prefix printer is function factory for prefixing text."""

from collections import Counter
from types import ModuleType
from typing import Any, Callable

from click import echo

from confprint import _exceptions, err_print
from confprint.format import bg, fg, font


global_count: Counter = Counter(n=-1, l=-1)


def prefix_printer(
    prefix: Any,
    whitespace: int = 0,
    stderr: bool = False,
    click: bool = False,
    upper: bool = True,
    frame_left: str = "[",
    frame_right: str = "]",
    prefix_end=":",
    counter_start: int = -1,
    global_counter: bool = False,
    text_color: str = "",
    text_style: str = "",
    text_bg_color: str = "",
    prefix_color: str = "",
    prefix_style: str = "",
    prefix_bg_color: str = "",
    format_frames: bool = True,
    *args,
    **kwargs,
) -> Callable[[str], None]:
    """
    Prefix printer is function factory for prefixing text.

    Args:
        prefix (Any): The prefix to use.
        whitespace (int, optional): The number of whitespaces to use.
        Defaults to 1.
        stderr (bool, optional):
            If True, the printer will print to sys.stderr instead of sys.stdout
            Defaults to False.
        click (bool, optional): If True, the printer will print to click.echo
            instead of sys.stdout. Defaults to False.
        upper (bool, optional): If True, the prefix will be printed in upper
        frame_left (str, optional): The left frame. Defaults to "[".
        frame_right (str, optional): The right frame. Defaults to "]".
        prefix_end (str, optional): The end of the prefix. Defaults to ":".
        counter_start (int, optional): The counter start value. Defaults to -1.
        global_counter (bool, optional): If True, the counter will be global.
            Defaults to False.
        text_color (str, optional): The text color. Defaults to "".
        text_style (str, optional): The text style. Defaults to "".
        text_bg_color (str, optional): The text background color.
        Defaults to "".
        prefix_color (str, optional): The prefix color. Defaults to "".
        prefix_style (str, optional): The prefix style. Defaults to "".
        prefix_bg_color (str, optional): The prefix background color.
        Defaults to "".
        format_frames (bool, optional): If True, the frames will be formatted.
            Defaults to True.
        format_frames (bool, optional): If True, the frames will be formatted.
            Defaults to True.

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

    def prefixed_printer(
        text: str = "", prefix: str = prefix, *args, **kwargs
    ) -> None:
        """
        Print text prefixed with the prefix.

        Args:
            text (str, optional): The text to print. Defaults to "".
            prefix (str, optional): The prefix to use. Defaults to prefix.

        Raises:
            _exceptions.PropertyError: Raised both stderr and click are True.
        """
        text_fmt_start = f""
        text_fmt_end = f""
        prefix_fmt_start = f""
        prefix_fmt_end = f""

        if text_color != "":
            text_fmt_start += f"{fg(text_color)}"
            text_fmt_end += f"{fg('reset')}"

        if text_style != "":
            text_fmt_start += f"{font(text_style)}"
            text_fmt_end += f"{font('reset')}"

        if text_bg_color != "":
            text_fmt_start += f"{bg(text_bg_color)}"
            text_fmt_end += f"{bg('reset')}"

        if prefix_color != "":
            prefix_fmt_start += f"{fg(prefix_color)}"
            prefix_fmt_end += f"{fg('reset')}"

        if prefix_style != "":
            prefix_fmt_start += f"{font(prefix_style)}"
            prefix_fmt_end += f"{font('reset')}"

        if prefix_bg_color != "":
            prefix_fmt_start += f"{bg(prefix_bg_color)}"
            prefix_fmt_end += f"{bg('reset')}"

        if upper and isinstance(prefix, str):
            prefix = prefix.upper()

        if not format_frames:
            prefix = f"{prefix_fmt_start}{prefix}{prefix_fmt_end}"

        if counter_start > -1 and not global_counter:
            prefix = (
                f"{frame_left}{prefix}{prefix_end}{count['n']}{frame_right}"
            )
            count["n"] += 1
        elif counter_start > -1 and global_counter:
            prefix = (
                f"{frame_left}{prefix}{prefix_end}{count['n']}{frame_right}"
            )
            count["n"] += 1
            global_count["l"] += 1
        elif counter_start == -1 and global_counter:
            prefix = (
                f"{frame_left}{prefix}{prefix_end}{count['n']}{frame_right}"
            )
            count["n"] += 1
        else:
            prefix = f"{frame_left}{prefix}{frame_right}"

        if format_frames:
            prefix = f"{prefix_fmt_start}{prefix}{prefix_fmt_end}"

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
            lines[
                0
            ] = f"{prefix}{prefix_end} {' ' * whitespace}{text_fmt_start}{lines[0]}{text_fmt_end}"
            indent_len = (
                len(lines[0])
                - first_line_len
                - len(text_fmt_start)
                - len(text_fmt_end)
            )
            print_func(lines[0], *args, **kwargs)  # type: ignore # mypy bug
            [print_func((" " * indent_len) + f"{text_fmt_start}{line}{text_fmt_end}") for line in lines[1:]]  # type: ignore # mypy bug # noqa: E501

        elif not text:
            print_func(f"{prefix}", *args, **kwargs)  # type: ignore # mypy bug
        else:
            print_func((f"{prefix}{prefix_end} {' ' * whitespace}{text_fmt_start}{text}{text_fmt_end}"), *args, **kwargs)  # type: ignore # mypy bug # noqa: E501

    return prefixed_printer
