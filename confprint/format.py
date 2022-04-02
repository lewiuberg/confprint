"""Format the output of the configuration."""

from colorama import Back, Fore, Style, init


init()


def fg(color: str = "") -> str:
    """
    Pick a color from colorama.

    Args:
        fg (str, optional): The color to pick. Defaults to "".

    Returns:
        str: The picked color.
    """
    if color == "red":
        return Fore.RED
    elif color == "green":
        return Fore.GREEN
    elif color == "yellow":
        return Fore.YELLOW
    elif color == "blue":
        return Fore.BLUE
    elif color == "magenta":
        return Fore.MAGENTA
    elif color == "cyan":
        return Fore.CYAN
    elif color == "white":
        return Fore.WHITE
    elif color == "black":
        return Fore.BLACK
    elif color == "lightred":
        return Fore.LIGHTRED_EX
    elif color == "lightgreen":
        return Fore.LIGHTGREEN_EX
    elif color == "lightyellow":
        return Fore.LIGHTYELLOW_EX
    elif color == "lightblue":
        return Fore.LIGHTBLUE_EX
    elif color == "lightmagenta":
        return Fore.LIGHTMAGENTA_EX
    elif color == "lightcyan":
        return Fore.LIGHTCYAN_EX
    elif color == "lightwhite":
        return Fore.LIGHTWHITE_EX
    elif color == "lightblack":
        return Fore.LIGHTBLACK_EX
    elif color == "reset":
        return Fore.RESET


def font(style: str = "") -> str:
    """
    Pick a font style from colorama.

    Args:
        style (str, optional): The font style to pick. Defaults to "".

    Returns:
        str: The picked font style.
    """
    if style == "bold":
        return Style.BRIGHT
    elif style == "dim":
        return Style.DIM
    elif style == "normal":
        return Style.NORMAL
    elif style == "reset":
        return Style.RESET_ALL


def bg(color: str = "") -> str:
    """
    Pick a background color from colorama.

    Args:
        bg (str, optional): The background to pick. Defaults to "".

    Returns:
        str: The picked background color.
    """
    if color == "red":
        return Back.RED
    elif color == "green":
        return Back.GREEN
    elif color == "yellow":
        return Back.YELLOW
    elif color == "blue":
        return Back.BLUE
    elif color == "magenta":
        return Back.MAGENTA
    elif color == "cyan":
        return Back.CYAN
    elif color == "white":
        return Back.WHITE
    elif color == "black":
        return Back.BLACK
    elif color == "lightred":
        return Back.LIGHTRED_EX
    elif color == "lightgreen":
        return Back.LIGHTGREEN_EX
    elif color == "lightyellow":
        return Back.LIGHTYELLOW_EX
    elif color == "lightblue":
        return Back.LIGHTBLUE_EX
    elif color == "lightmagenta":
        return Back.LIGHTMAGENTA_EX
    elif color == "lightcyan":
        return Back.LIGHTCYAN_EX
    elif color == "lightwhite":
        return Back.LIGHTWHITE_EX
    elif color == "lightblack":
        return Back.LIGHTBLACK_EX
    elif color == "reset":
        return Back.RESET
