# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import


class ValidationError(Exception):
    """
    Raised data is not properly formatted.
    """


class InvalidDataError(ValueError):
    """
    Raised when data is invalid to load.
    """


class EmptyDataError(InvalidDataError):
    """
    Raised when data is not included valid table data.
    """


class OpenError(IOError):
    """
    Raised when failed to open a file.
    """
