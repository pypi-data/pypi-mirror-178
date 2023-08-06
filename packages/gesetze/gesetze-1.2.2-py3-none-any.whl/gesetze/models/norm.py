"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from dataclasses import dataclass


@dataclass
class Norm:
    """
    Holds legal data on a norm
    """

    norm: str
    title: str
    law_short: str
    law_long: str
    url: str
