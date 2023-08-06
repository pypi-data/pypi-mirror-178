"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from ..driver import Driver


class Lexparency(Driver):
    """
    Utilities for dealing with 'lexparency.de'
    """

    # Individual identifier
    identifier: str = "lexparency"

    # Base URL
    url: str = "https://lexparency.de"
