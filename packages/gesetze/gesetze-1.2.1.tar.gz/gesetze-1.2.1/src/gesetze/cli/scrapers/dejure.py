"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0801

from asyncio import Semaphore
import re
from typing import Dict, List

from bs4.element import Tag

from ..scraper import Scraper


class DejureOnline(Scraper):
    """
    Utilities for scraping 'dejure.org'
    """

    # Individual identifier
    identifier: str = "dejure"

    async def collect(self, limit: Semaphore) -> List[Dict[str, str]]:
        """
        Collects law URLs from 'dejure.org'

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
                "law": link.a.text,
                "title": link.text.replace(link.a.text, "").strip("( )"),
                "uri": link.a["href"][9:],
                "norms": {},
            }

        # Fetch overview page
        html = await self.get_html("https://dejure.org", limit)

        # Create data array
        links = []

        # Loop over relevant charset
        for char in "ABDEFGHIJKLMNOPRSTUVWZ":
            # Process links
            links.extend(
                [
                    extract(link)
                    for link in html.find("a", attrs={"name": char})
                    .find_next_sibling("ul")
                    .find_all("li")
                ]
            )

        return links

    async def harvest(self, law: Dict[str, str], limit: Semaphore) -> Dict[str, str]:
        """
        Harvests law data from 'dejure.org'

        :param law: dict Collected data
        :param limit: asyncio.Semaphore Bound limit
        :return: dict Processed data
        """

        # Fetch index page for each law
        html = await self.get_html(f'https://dejure.org/gesetze/{law["uri"]}', limit)

        # Iterate over `p` tags ..
        for tag in html.find_all("p", attrs={"class": "clearfix"}):
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

                # Store law data
                law["norms"][norm] = {
                    "norm": norm,
                    "title": title.replace("§  ", "§ "),
                    "uri": f'gesetze/{law["law"]}/{norm}.html',
                }

        return law
