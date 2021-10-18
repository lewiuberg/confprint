"""Exceptions for the confprint package.

Custom exceptions used by confprint for more helpful error messages.
"""


class confprintException(Exception):
    """Base class for all confprint exceptions."""


class PropertyError(confprintException):
    """Selection of properties failed."""
