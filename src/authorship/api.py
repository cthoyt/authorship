# -*- coding: utf-8 -*-

"""Generate author list text from a Google Sheet."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Optional, Union

from class_resolver import HintOrType, OptionalKwargs
from pydantic import BaseModel

__all__ = [
    "Institution",
    "Author",
    "Authorship",
    "Reader",
    "Writer",
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


class Reader(ABC):
    """A getter for authorship."""

    @abstractmethod
    def get_authorship(self) -> Authorship:
        """Get an author list."""

    def print(  # noqa:T202
        self,
        writer: HintOrType["Writer"],
        writer_kwargs: OptionalKwargs = None,
        file=None,
        **kwargs,
    ) -> None:
        """Print the authorship from this reader with a writer, given by name (e.g., text, biorxiv)."""
        from .writer import writer_resolver

        _writer = writer_resolver.make(writer, writer_kwargs)
        if file is None:
            _writer.print(self.get_authorship(), **kwargs)
        elif isinstance(file, (str, Path)):
            with Path(file).expanduser().resolve().open("w") as _file:
                _writer.print(self.get_authorship(), file=_file, **kwargs)
        else:
            _writer.print(self.get_authorship(), file=file, **kwargs)


class Writer(ABC):
    """A writer for authorship."""

    @abstractmethod
    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate over lines for the authorship."""

    def to_lines(self, authorship: Union[Reader, Authorship]) -> list[str]:
        """Make lines for the authorship."""
        if isinstance(authorship, Reader):
            authorship = authorship.get_authorship()
        return list(self.iter_lines(authorship))

    def to_str(self, authorship: Union[Reader, Authorship]) -> str:
        """Make a string from the authorship."""
        return "\n".join(self.to_lines(authorship))

    def print(self, authorship: Union[Reader, Authorship], **kwargs) -> None:  # noqa:T202
        """Print the authorship."""
        print(self.to_str(authorship), **kwargs)  # noqa:T201

    def write(self, authorship: Union[Reader, Authorship], *, path: Union[str, Path]) -> None:
        """Write the authorship to a path."""
        Path(path).resolve().write_text(self.to_str(authorship))
