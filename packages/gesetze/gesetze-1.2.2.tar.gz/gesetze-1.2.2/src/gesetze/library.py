"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from pathlib import Path
import sqlite3
from typing import Any, Dict, Iterable, Optional, Union

from .models import Norm
from .utils import analyze


class Library:
    """
    Utilities for handling database queries
    """

    # Database connection
    conn: sqlite3.Connection

    def __init__(self, db_file: Union[Path, str]) -> None:
        """
        Creates 'Library' instance

        :param db_file: pathlib.Path | str Path to database file
        :return: None
        """

        # Connect to database file
        self.conn = sqlite3.connect(db_file)

        # Force dictionaries as query results
        self.conn.row_factory = sqlite3.Row

    def __del__(self) -> None:
        """
        Destroys 'Gesetz' instance

        :return: None
        """

        # Terminate connection
        self.conn.close()

    def init(self) -> None:
        """
        Sets up database tables

        :return: None
        """

        # Create database tables
        # (1) Available providers
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS providers(
                provider TEXT PRIMARY KEY,
                url TEXT
            );
            """
        )

        # (2) Overview
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS idx(
                provider TEXT,
                law TEXT,
                title TEXT,
                uri TEXT,
                PRIMARY KEY(provider, law)
            );
            """
        )

        # Add providers
        self.conn.executemany(
            f"""
            INSERT INTO providers
            VALUES(:name, :url);
            """,
            [
                {"name": "buzer", "url": "https://buzer.de"},
                {"name": "gesetze", "url": "https://www.gesetze-im-internet.de"},
                {"name": "dejure", "url": "https://dejure.org"},
                {"name": "lexparency", "url": "https://lexparency.de"},
            ],
        )

        # Save changes
        self.conn.commit()

    def store(self, provider: str, data: Dict[str, Dict[str, str]]) -> None:
        """
        Imports data into database

        :param provider: str Provider name
        :param data: dict Set of legal data
        :return: None
        """

        self.conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {provider}(
                law TEXT,
                norm TEXT,
                title TEXT,
                uri TEXT,
                PRIMARY KEY(law, norm)
            );
            """
        )

        # Loop over laws ..
        for law in data.values():
            # (1) .. adding law to index
            self.conn.execute(
                f"""
                INSERT INTO idx
                VALUES('{provider}', :law, :title, :uri);
                """,
                law,
            )

            # (2) .. importing its norms
            for norm in law["norms"].values():
                # Update provider table
                self.conn.execute(
                    f"""
                    INSERT INTO {provider}
                    VALUES('{law["law"]}', :norm, :title, :uri);
                    """,
                    norm,
                )

        # Save changes
        self.conn.commit()

    def fetch(self, provider: str, data: Dict[str, str]) -> Optional[Dict[str, str]]:
        """
        Provides database record matching provided legal data

        Example output:

        {
            'norm': '1',
            'title': '§ 1 Beginn der Rechtsfähigkeit',
            'law_short': 'BGB',
            'law_long': 'Bürgerliches Gesetzbuch',
            'url': 'https://www.gesetze-im-internet.de/bgb/__1.html',
        }

        :param provider: str Provider name
        :param data: dict Legal data
        :return: gesetze.models.Norm | None Data (if any)
        """

        try:
            return (
                self.conn.cursor()
                .execute(
                    f"""
                SELECT
                    norm,
                    {provider}.title,
                    idx.law as law_short,
                    idx.title AS law_long,
                    providers.url || '/' || {provider}.uri AS url
                FROM {provider}
                JOIN idx
                ON idx.provider IS '{provider}' AND idx.law IS {provider}.law
                JOIN providers
                ON providers.provider IS '{provider}'
                WHERE norm IS :norm AND LOWER(idx.law) IS LOWER(:gesetz)
                """,
                    data,
                )
                .fetchone()
            )

        except sqlite3.OperationalError:
            return None

    def has(self, providers: Union[Iterable[str], str], data: Dict[str, str]) -> bool:
        """
        Checks whether norm exists for provider

        :param providers: list | tuple | str Provider name(s)
        :param data: dict Legal data
        :return: bool
        """

        return self.get(providers, data) is not None

    def get(
        self, providers: Union[Iterable[str], str], data: Dict[str, str]
    ) -> Optional[Norm]:
        """
        Provides 'Norm' instance matching provided legal data

        :param providers: list | tuple | str Provider name(s)
        :param data: dict Legal data
        :return: gesetze.gesetz.models.Norm | None Data (if any)
        """

        # If single provider was passed ..
        if isinstance(providers, str):
            # .. make it a list
            providers = [providers]

        # Loop over providers
        for provider in providers:
            if norm_data := self.fetch(provider, data):
                return Norm(*norm_data)

        return None
