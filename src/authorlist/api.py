# -*- coding: utf-8 -*-

"""Generate author list text from a Google Sheet."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel

from .constants import ROLES

__all__ = [
    "Institution",
    "Author",
    "Authorship",
    "Reader",
    "Writer",
]


class Institution(BaseModel):
    name: str
    address: str
    ror: Optional[str]
    wikidata: Optional[str]


class Author(BaseModel):
    first: str
    middle: str
    last: str
    email: str
    orcid: str
    wikidata: str
    role: Optional[ROLES]
    homepage: Optional[str]
    conflict: Optional[str]
    twitter: Optional[str]
    institutions: list[Institution]


class Authorship(BaseModel):
    authors: list[Author]
    institutions: list[Institution]


class Reader(ABC):
    """A getter for authorship."""

    @abstractmethod
    def get_author_list(self) -> Authorship:
        """Get an author list."""


class Writer(ABC):
    """A writer for authorship."""

    @abstractmethod
    def to_lines(self, authorship: Authorship) -> list[str]:
        """Make lines for the authorship."""

    def to_str(self, authorship: Authorship) -> str:
        """Make a string from the authorship."""
        return "\n".join(self.to_lines(authorship))

    def write(self, authorship: Authorship, path: Union[str, Path]) -> None:
        """Write the authorship to a path."""
        Path(path).resolve().write_text(self.to_str(authorship))
