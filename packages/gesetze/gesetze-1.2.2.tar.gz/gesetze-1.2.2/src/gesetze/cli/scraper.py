"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from abc import ABC, abstractmethod
import asyncio
import hashlib
from pathlib import Path
import random
from typing import Dict, List, Optional, Union

import aiofiles
import aiohttp
import bs4


class Scraper(ABC):
    """
    Utilities for scraping providers
    """

    # Download directory
    data_dir: Optional[Path] = None

    # UA strings
    ua: List[str] = [
        # Firefox
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        + "/51.0.2704.103 Safari/537.36",
        # Opera
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
        + "/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",
        # Safari
        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15"
        + " (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1",
        # Internet Explorer
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobil"
        + "e/9.0)",
        # Google
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    ]

    # Individual identifier
    identifier: Optional[str] = None

    def __init__(self, data_dir: Union[Path, str, None] = None) -> None:
        """
        Creates 'Scraper' instance

        :param data_dir: pathlib.Path | str | None Download directory
        :return: None
        """

        if data_dir is None:
            data_dir = Path.cwd() / f".{self.identifier}"

        # Define download directory
        self.data_dir = Path(data_dir)

        # Create it (if needed)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def get_file_path(self, url: str) -> Path:
        """
        Determines path to stored HTML file

        :param url: str Target URL
        :return: pathlib.Path Path to HTML file
        """

    async def get_html(self, url: str, limit: asyncio.Semaphore) -> str:
        """
        Fetches HTML for given URL

        :param url: str Target URL
        :param limit: asyncio.Semaphore Bound limit
        :return: str Source HTML
        """

        # Use hash string as filename
        filename = hashlib.blake2b(url.encode("utf-8")).hexdigest()

        # Build its path
        file = self.data_dir / f"{filename}.html"

        # If file exists, but is empty ..
        if file.exists() and file.stat().st_size == 0:
            # .. remove it
            file.unlink()

        # Impose bound limit
        async with limit:
            # Check whether file exists
            if not file.exists():
                # Define request options, like ..
                # (1) .. timeout
                timeout = aiohttp.ClientTimeout(total=120)

                # (2) .. headers
                headers = {"User-Agent": random.choice(self.ua)}

                # Open HTTP session
                async with aiohttp.ClientSession(headers=headers) as session:
                    # Fetch URL contents
                    async with session.get(url, timeout=timeout) as response:
                        # Make sure it worked
                        assert response.status == 200

                        # Get HTML text
                        html = await response.text("utf-8", "ignore")

                # Wait for it ..
                await asyncio.sleep(random.randint(4, 8))

                async with aiofiles.open(str(file), "w", encoding="utf-8") as html_file:
                    await html_file.write(html)

            else:
                async with aiofiles.open(str(file), "r", encoding="utf-8") as html_file:
                    html = await html_file.read()

        return bs4.BeautifulSoup(html, "lxml")

    def scrape(self, maximum: int = 16) -> List[Dict[str, str]]:
        """
        Scrapes legal norms across all laws

        :param maximum: int Maximum for simultaneous requests
        :return: list Scraped data
        """

        async def worker() -> List[Dict[str, str]]:
            """
            Asyn helper

            :return: list Scraped data
            """

            # Limit requests using semaphore
            limit = asyncio.Semaphore(maximum)

            # Collect URLs
            laws = await self.collect(limit)

            # Harvest laws
            data = await asyncio.gather(*[self.harvest(law, limit) for law in laws])

            return data

        return asyncio.run(worker())

    @abstractmethod
    async def collect(self, limit: asyncio.Semaphore) -> list:
        """
        Collects law URLs

        :param limit: asyncio.Semaphore Bound limit
        :return: list Collected URLs
        """

    @abstractmethod
    async def harvest(self, law: Dict[str, str], limit: asyncio.Semaphore) -> dict:
        """
        Harvests law data

        :param law: dict Collected data
        :param limit: asyncio.Semaphore Bound limit
        :return: list Harvested data
        """
