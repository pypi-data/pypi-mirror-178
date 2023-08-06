"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from copy import deepcopy
import re
from typing import Callable, Dict, Iterable, List, Union

from .lib.driver import Driver
from .lib.factory import Factory
from .lib.helpers import REGEX


class Gesetz:
    """
    Utilities for linking to german legal norms
    """

    # Available providers
    drivers: List[Driver]

    # Defines HTML attribute defaults
    attributes: Dict[str, str] = {"target": "_blank"}

    # Controls `title` attribute
    #
    # Possible values:
    #
    # 'light'  => abbreviated law (eg 'GG')
    # 'normal' => complete law (eg 'Grundgesetz')
    # 'full'   => official heading (eg 'Art 45d Parlamentarisches Kontrollgremium')
    title: Union[bool, str] = False

    def __init__(self, order: Union[Iterable[str], str, None] = None) -> None:
        """
        Creates 'Gesetz' instance

        :param order: Iterable[str] | str | None Driver(s) to be used
        :return: None
        """

        # Set default order
        if order is None:
            order = [
                # (1) 'gesetze-im-internet.de'
                "gesetze",
                # (2) 'dejure.org'
                "dejure",
                # (3) 'buzer.de'
                "buzer",
                # (4) 'lexparency.de'
                "lexparency",
            ]

        # If string was passed as order ..
        if isinstance(order, str):
            # .. make it a list
            order = [order]

        # Initialize drivers
        self.drivers = [Factory.create(driver) for driver in order]

    def validate(self, string: str) -> bool:
        """
        Validates a single legal norm (across all providers)

        :param string: str Legal norm
        :return: bool Whether legal norm is valid (= linkable)
        """

        # Fail early when string is empty
        if not string:
            return False

        # Iterate over drivers
        for driver in self.drivers:
            # If legal norm checks out ..
            if driver.validate(string):
                # .. break the loop
                return True

        return False

    def linkify(self, match: re.Match) -> str:
        """
        Converts matched legal reference into `a` tag

        :param match: re.Match Matched legal norm
        :return: str Converted `a` tag
        """

        # Set `a` tag attribute defaults
        attributes = deepcopy(self.attributes)

        # Fetch extracted data
        string = match.group(0)
        data = match.groupdict()

        # Iterate over drivers for each match ..
        for driver in self.drivers:
            # .. using only valid laws & legal norms
            if driver.validate(string):
                # Build `a` tag attributes
                # (1) Determine `href` attribute
                attributes["href"] = driver.get_url(data)

                # (2) Determine `title` attribute
                attributes["title"] = driver.get_title(data, self.title)

                # Abort the loop
                break

        # If `href` attribute is undefined ..
        if "href" not in attributes:
            # .. return original string
            return string

        # Build `a` tag
        # (1) Format key-value pairs
        attributes = [f'{key}="{value}"' for key, value in attributes.items() if value]

        # (2) Combine everything
        return f"<a {' '.join(attributes)}>{string}</a>"

    def markdownify(self, match: re.Match) -> str:
        """
        Converts matched legal reference into markdown link

        :param match: re.Match Matched legal norm
        :return: str Converted markdown link
        """

        # Fetch extracted data
        string = match.group(0)
        data = match.groupdict()

        # Set fallback
        link = None

        # Iterate over drivers for each match ..
        for driver in self.drivers:
            # .. using only valid laws & legal norms
            if driver.validate(string):
                # Determine link
                link = driver.get_url(data)

                # Abort loop
                break

        # If link is undefined ..
        if not link:
            # .. return original string
            return string

        # Build markdown link
        return f"[{string}]({link})"

    def gesetzify(self, string: str, callback: Union[Callable, None] = None) -> str:
        """
        Converts legal references throughout text into `a` tags

        :param string: str Text
        :param callback: typing.Callable Callback function
        :return: str Processed text
        """

        if callback is None:
            callback = self.linkify

        return REGEX.sub(callback, string)
