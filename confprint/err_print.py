"""err_print uses sys.stderr.write() as the printer function."""

import sys


def err_print(*args, **kwargs) -> None:
    """Use sys.stderr.write() as print()."""
    print(*args, file=sys.stderr, **kwargs)
