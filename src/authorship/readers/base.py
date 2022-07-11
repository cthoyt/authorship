"""Base readers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

from class_resolver import HintOrType, OptionalKwargs

from ..models import Authorship

if TYPE_CHECKING:
    from ..writers import Writer

__all__ = [
    "Reader",
    "PreparedReader",
]


class Reader(ABC):
    """A getter for authorship."""

    @abstractmethod
    def get_authorship(self) -> "Authorship":
        """Get an author list."""

    def print(  # noqa:T202
        self,
        writer: HintOrType["Writer"] = "text",
        writer_kwargs: OptionalKwargs = None,
        file=None,
        **kwargs,
    ) -> None:
        """Print the authorship from this reader with a writer, given by name (e.g., text, biorxiv)."""
        from ..writers import writer_resolver

        _writer = writer_resolver.make(writer, writer_kwargs)
        if file is None:
            _writer.print(self.get_authorship(), **kwargs)
        elif isinstance(file, (str, Path)):
            with Path(file).expanduser().resolve().open("w") as _file:
                _writer.print(self.get_authorship(), file=_file, **kwargs)
        else:
            _writer.print(self.get_authorship(), file=file, **kwargs)


class PreparedReader(Reader):
    """A reader for prepared :class:`Authorship` instances."""

    def __init__(self, authorship: "Authorship"):
        """Instantiate the prepared reader."""
        self.authorship = authorship

    def get_authorship(self) -> "Authorship":
        """Get the prepared authorship."""
        return self.authorship
