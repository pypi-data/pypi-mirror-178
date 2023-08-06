"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from copy import deepcopy
from pathlib import Path
import re
from typing import Callable, Dict, Iterable, List, Optional, Union

from .library import Library
from .utils import REGEX, analyze


class Gesetz:
    """
    Utilities for linking to german legal norms
    """

    # Database wrapper
    library: Library

    # Available providers
    providers: List[str]

    # Controls HTML attribute defaults
    attributes: Dict[str, str] = {"target": "_blank"}

    # Controls `title` attribute
    #
    # 'light'  => abbreviated law (eg 'BGB')
    # 'normal' => complete law (eg 'Bürgerliches Gesetzbuch')
    # 'full'   => (un)official heading (eg '§ 1 Beginn der Rechtsfähigkeit')
    title: Union[bool, str] = False

    def __init__(self, providers: Optional[Union[Iterable[str], str]] = None) -> None:
        """
        Creates 'Gesetz' instance

        :param providers: list | tuple | str | None Provider(s) to be used
        :return: None
        """

        # Initialize library
        self.library = Library(Path(__file__).parent / "nomoi.sqlite")

        # Determine (order of) providers
        # (1) If single provider was passed ..
        if isinstance(providers, str):
            # .. make it a list
            providers = [providers]

        # (1) Apply providers in specified order ..
        self.providers = providers or [
            # .. otherwise provide fallback
            # (a) 'gesetze-im-internet.de'
            "gesetze",
            # (b) 'dejure.org'
            "dejure",
            # (c) 'buzer.de'
            "buzer",
            # (d) 'lexparency.de'
            "lexparency",
        ]

    def validate(self, string: str) -> bool:
        """
        Validates a single legal norm (across all providers)

        :param string: str Legal norm
        :return: bool Whether legal norm is valid (= linkable)
        """

        # Fail early when string is empty
        if not string:
            return False

        # Analyze string
        if data := analyze(string):
            # If legal norm checks out ..
            if self.library.has(self.providers, data):
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

        # Fetch record from library
        if norm := self.library.get(self.providers, match.groupdict()):
            # Build `a` tag attributes
            # (1) Determine `href` attribute
            attributes["href"] = norm.url

            # (2) Determine `title` attribute, which boils down to ..
            if title := {
                # (a) .. abbreviated law (eg 'BGB')
                "light": norm.law_short,
                # (b) .. complete law (eg 'Bürgerliches Gesetzbuch')
                "normal": norm.law_long,
                # (c) .. (un)official heading (eg '§ 1 Beginn der Rechtsfähigkeit')
                "full": norm.title,
            }.get(self.title):
                attributes["title"] = title

            # Build `a` tag
            # (1) Format key-value pairs
            attributes = [
                f'{key}="{value}"' for key, value in attributes.items() if value
            ]

            # (2) Combine everything
            return f"<a {' '.join(attributes)}>{match.group(0)}</a>"

        # Return original string
        return match.group(0)

    def markdownify(self, match: re.Match) -> str:
        """
        Converts matched legal reference into markdown link

        :param match: re.Match Matched legal norm
        :return: str Converted markdown link
        """

        # Set fallback
        link = None

        # Fetch data record from library
        if norm := self.library.get(self.providers, match.groupdict()):
            # Build markdown link
            return f"[{match.group(0)}]({norm.url})"

        # Return original string
        return match.group(0)

    def gesetzify(self, string: str, callback: Optional[Callable] = None) -> str:
        """
        Converts legal references throughout text into `a` tags

        :param string: str Unprocessed text
        :param callback: callable | None Callback function
        :return: str Processed text
        """

        return REGEX.sub(callback or self.linkify, string)
