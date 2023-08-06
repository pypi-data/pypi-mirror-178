"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

# pylint: disable=R0801

from asyncio import Lock, Semaphore
import re
from typing import Dict, List

from ..scraper import Scraper


class Buzer(Scraper):
    """
    Utilities for scraping 'buzer.de'
    """

    # Individual identifier
    identifier: str = "buzer"

    async def crawl(
        self, url: str, urls: List[str], lock: Lock, limit: Semaphore
    ) -> None:
        """
        Crawls overview pages recursively while collecting law URLs

        :param url: str Target URL
        :param urls: list Collected law URLs
        :param lock: asyncio.Lock Global lock
        :param limit: asyncio.Semaphore Bound limit
        :return: None
        """

        # Fetch overview page
        fna_html = await self.get_html(url, limit)

        # If relevant law URLs are present ..
        if law_links := fna_html.find_all("a", {"class": "ltg"}):
            # .. loop over them
            for link in law_links:
                # Skip deprecated laws
                if (
                    sibling := link.next_sibling
                ) and "aufgehoben durch" in sibling.text:
                    continue

                # Aquire lock
                async with lock:
                    # Store law URL
                    urls.append(link["href"])

        # Loop over collected overview links
        for link in fna_html.find("table").find_all("a"):
            # Check whether link leads to an overview page,
            # as opposed to the overview page that was crawled before
            if re.match(
                r"""
                # Random string(s)
                .*\s
                # Open bracket
                (?:\(
                    # Available subcategories
                    \d*(?:\sUntergebiete\s)?
                    \/
                    # Number of laws therein
                    \d*(?:\sgeltende\sVorschriften\s)?
                    \/
                    # Deprecated laws therein
                    \d*(?:\saufgehobene\sVorschriften)?
                # Close bracket
                \))
                """,
                link.parent.text,
                re.VERBOSE,
            ):
                await self.crawl(
                    f'https://www.buzer.de{link["href"]}', urls, lock, limit
                )

    async def collect(self, limit: Semaphore) -> List[Dict[str, str]]:
        """
        Collects law URLs from 'buzer.de'

        :param limit: asyncio.Semaphore Bound limit
        :return: list Collected URLs
        """

        def extract(uri: str) -> Dict[str, str]:
            """
            Extracts law data from law URI

            :param uri: str Law URI
            :return: dict Extracted data
            """

            return {
                "law": "",
                "title": "",
                "uri": uri,
                "norms": {},
            }

        # Create data array
        urls = []

        # Crawl index & all subsequent indices
        await self.crawl("https://www.buzer.de/fna/index.htm", urls, Lock(), limit)

        # Process law URLs
        return [extract(url) for url in urls]

    async def harvest(self, law: Dict[str, str], limit: Semaphore) -> Dict[str, str]:
        """
        Harvests law data from 'buzer.de'

        :param law: dict Collected data
        :param limit: asyncio.Semaphore Bound limit
        :return: dict Processed data
        """

        # Fetch index page for each law
        html = await self.get_html(law["uri"], limit)

        # Get title
        heading = html.find("h1").text

        # If stripped shorthand of title present ..
        if heading_match := re.match(
            r"""
            # Start
            ^
            # Long title
            (.*)\s
            # Open bracket
            \(
                # Short title (optional)
                (?:(.*)\s\-\s)?
                # Abbreviation (lazy)
                (.*?)
                # Hint saying 'no official abbreviation'
                (?:\sk\.a\.Abk\.)?
            # Close bracket
            \)
            # End
            $
            """,
            heading,
            re.VERBOSE,
        ):
            # .. store it as title for current law
            law["law"] = heading_match.group(3)
            law["title"] = heading_match.group(1)

            if short_title := heading_match.group(2):
                law["title"] = short_title

        # Iterate over relevant `div` tags ..
        for div in html.find_all("div", attrs={"class": "inhalt"}):
            # .. selecting their first child `a` tag
            tag = div.find("a")

            # Get norm heading
            title = tag.text.strip().replace("§  ", "§ ")

            # If identifier available ..
            if match := re.match(
                r"(?:§+|Art|Artikel)\.?\s*(\d+(?:\w\b)?)",
                title,
                re.IGNORECASE,
            ):
                # .. extract norm
                norm = match.group(1)

                # Store law data
                law["norms"][norm] = {
                    "norm": norm,
                    "title": title.replace("\n", " "),
                    "uri": tag["href"].lstrip("/"),
                }

        return law
