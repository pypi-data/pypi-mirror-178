"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0903

from pathlib import Path
from typing import Union

from .scraper import Scraper
from .scrapers import Buzer, DejureOnline, GesetzeImInternet, Lexparency


class Factory:
    """
    Utilities for creating 'Scraper' instances
    """

    @staticmethod
    def create(provider: str, data_dir: Union[Path, str]) -> Scraper:
        """
        Creates a new 'Scraper' instance for the given type

        :param provider: str Scraper type
        :param data_dir: pathlib.Path | str Download directory
        :return: Scraper Scraper instance
        :raises: Exception Invalid provider
        """

        # List available scrapers
        scrapers = {
            # (1) 'gesetze-im-internet.de'
            "gesetze": GesetzeImInternet,
            # (2) 'dejure.org'
            "dejure": DejureOnline,
            # (3) 'buzer.de'
            "buzer": Buzer,
            # (4) 'lexparency.de'
            "lexparency": Lexparency,
        }

        # Fail early for invalid scrapers
        if provider not in scrapers:
            raise Exception(f'Invalid scraper type: "{provider}"')

        # Instantiate object
        return scrapers[provider](data_dir)
