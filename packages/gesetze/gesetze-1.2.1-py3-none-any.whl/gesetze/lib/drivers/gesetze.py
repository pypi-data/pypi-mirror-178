"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from ..driver import Driver


class GesetzeImInternet(Driver):
    """
    Utilities for dealing with 'gesetze-im-internet.de'
    """

    # Individual identifier
    identifier: str = "gesetze"

    # Base URL
    url: str = "https://www.gesetze-im-internet.de"
