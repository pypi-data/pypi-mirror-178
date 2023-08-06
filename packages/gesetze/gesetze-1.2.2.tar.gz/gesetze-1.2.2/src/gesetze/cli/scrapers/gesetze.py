"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0801

from asyncio import Semaphore, gather
import re
from typing import Any, Dict, List

from bs4.element import Tag

from ..scraper import Scraper


class GesetzeImInternet(Scraper):
    """
    Utilities for scraping 'gesetze-im-internet.de'
    """

    # Individual identifier
    identifier: str = "gesetze"

    async def collect(self, limit: Semaphore) -> List[Dict[str, str]]:
        """
        Collects law URLs from 'gesetze-im-internet.de'

        :param limit: asyncio.Semaphore Bound limit
        :return: list Collected URLs
        """

        def extract(link: Tag) -> Dict[str, str]:
            """
            Extracts law data from tag

            :param link: bs4.element.Tag Link tag
            :return: dict Extracted data
            """

            return {
                "law": link.a.text[1:-1],
                "title": link.a.abbr["title"],
                "uri": link.a["href"][2:-11],
                "norms": {},
            }

        async def fetch(char: str) -> List[Dict[str, str]]:
            # Fetch overview page
            html = await self.get_html(
                f"https://www.gesetze-im-internet.de/Teilliste_{char}.html", limit
            )

            return [
                extract(link) for link in html.select_one("#paddingLR12").find_all("p")
            ]

        # Create data array
        return flatten_lists(
            await gather(
                *[fetch(char) for char in "ABCDEFGHIJKLMNOPQRSTUVWYZ123456789"]
            )
        )

    async def harvest(self, law: Dict[str, str], limit: Semaphore) -> Dict[str, str]:
        """
        Harvests law data from 'gesetze-im-internet.de'

        :param law: dict Collected data
        :param limit: asyncio.Semaphore Bound limit
        :return: dict Processed data
        """

        # Fetch index page for each law
        html = await self.get_html(
            f'https://www.gesetze-im-internet.de/{law["uri"]}/index.html', limit
        )

        # Iterate over `a` tags ..
        for tag in html.select_one("#paddingLR12").find_all("td"):
            # .. skipping norms without ..
            # (1) .. `a` tag child
            if not tag.a:
                continue

            # (2) .. `href` attribute in `a` tag child
            if not tag.a.get("href"):
                continue

            # Get norm heading
            title = tag.text.strip()

            # If identifier available ..
            if match := re.match(
                r"(?:§+|Art|Artikel)\.?\s*(\d+(?:\w\b)?)", title, re.IGNORECASE
            ):
                # .. extract norm
                norm = match.group(1)

                # Determine URI
                # (1) Set default URI
                uri = f"__{norm}"

                # (2) Except for the 'Grundgesetz' ..
                if law["law"] == "GG":
                    # .. which is different
                    uri = f"art_{norm}"

                # Store law data
                law["norms"][norm] = {
                    "norm": norm,
                    "title": title,
                    "uri": f'{law["uri"]}/{uri}.html',
                }

        return law


def flatten_lists(lists: List[List[Any]]) -> List[Any]:
    """
    Flattens list of lists

    :param lists: list
    :return: list
    """

    return [item for sublist in lists for item in sublist]
