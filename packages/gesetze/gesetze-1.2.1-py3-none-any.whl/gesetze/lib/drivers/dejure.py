"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from ..driver import Driver


class DejureOnline(Driver):
    """
    Utilities for dealing with 'dejure.org'
    """

    # Individual identifier
    identifier: str = "dejure"

    # Base URL
    url: str = "https://dejure.org"
