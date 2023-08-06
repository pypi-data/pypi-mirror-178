"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from ..driver import Driver


class Buzer(Driver):
    """
    Utilities for dealing with 'buzer.de'
    """

    # Individual identifier
    identifier: str = "buzer"

    # Base URL
    url: str = "https://buzer.de"
