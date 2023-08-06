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


class Lexparency(Scraper):
    """
    Utilities for scraping 'lexparency.de'
    """

    # Individual identifier
    identifier: str = "lexparency"

    async def collect(self, limit: Semaphore) -> List[Dict[str, str]]:
        """
        Collects law URLs from 'lexparency.org'

        :param limit: asyncio.Semaphore Bound limit
        :return: list Collected URLs
        """

        def extract(link: Tag) -> Dict[str, str]:
            """
            Extracts law data from tag

            :param link: bs4.element.Tag Link tag
            :return: dict Extracted data
            """

            law = link.text.strip()

            # If abbreviation available ..
            if law_match := re.match(r".*\((.*)\)$", law):
                # .. store it as shorthand for current law
                law = law_match.group(1)

            # .. collecting its information
            return {
                "law": law,
                "title": "",
                "uri": link["href"][4:],
                "norms": {},
            }

        # Fetch overview page
        html = await self.get_html("https://lexparency.de", limit)

        # Process links
        return [
            extract(link) for link in html.select_one("#featured-acts").find_all("a")
        ]

    async def harvest(self, law: Dict[str, str], limit: Semaphore) -> Dict[str, str]:
        """
        Harvests law data from 'lexparency.org'

        :param law: dict Collected data
        :param limit: asyncio.Semaphore Bound limit
        :return: dict Processed data
        """

        # Fetch index page for each law
        html = await self.get_html(f'https://lexparency.de/eu/{law["uri"]}/', limit)

        # Determine title
        # (1) Create data array
        title = []

        # (2) Convert first character of second entry (= 'title essence') to lowercase
        for i, string in enumerate(list(html.select_one("h1").stripped_strings)):
            if i == 1:
                string = string[:1].lower() + string[1:]

            title.append(string)

        # (3) Create title from strings
        law["title"] = " ".join(title).strip()

        # Iterate over `li` tags ..
        for tag in html.select_one("#toccordion").find_all(
            "li", attrs={"class": "toc-leaf"}
        ):
            # .. skipping norms without ..
            # (1) .. `a` tag child
            if not tag.a:
                continue

            # (2) .. `href` attribute in `a` tag child
            if not tag.a.get("href"):
                continue

            # Get norm heading
            title = tag.text.replace("—", "-")

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
                    "uri": f'eu/{law["uri"]}/ART_{norm}',
                }

        return law
