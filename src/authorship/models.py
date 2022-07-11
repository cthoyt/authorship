"""Models."""

from typing import Optional

from pydantic import BaseModel

__all__ = [
    "Institution",
    "Author",
    "Authorship",
]


class Institution(BaseModel):
    """An institution."""

    name: str
    address: Optional[str]
    ror: Optional[str]
    wikidata: Optional[str]


class Author(BaseModel):
    """An author."""

    first: str
    middle: Optional[str]
    last: str
    email: str
    orcid: str
    wikidata: Optional[str]
    role: Optional[str]
    homepage: Optional[str]
    conflict: Optional[str]
    twitter: Optional[str]
    institutions: list[Institution]

    @property
    def name(self) -> str:
        """Get the name of the author."""
        if self.middle:
            return f"{self.first} {self.middle} {self.last}"
        return f"{self.first} {self.last}"


class Authorship(BaseModel):
    """A combination of authors and institutions."""

    authors: list[Author]
    institutions: list[Institution]
