"""Base writers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Union

from ..models import Authorship

if TYPE_CHECKING:
    from ..readers import Reader

__all__ = [
    "Writer",
]


class Writer(ABC):
    """A writer for authorship."""

    @abstractmethod
    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate over lines for the authorship."""

    def to_lines(self, authorship: Union["Reader", Authorship]) -> list[str]:
        """Make lines for the authorship."""
        from ..readers import Reader

        if isinstance(authorship, Reader):
            authorship = authorship.get_authorship()
        return list(self.iter_lines(authorship))

    def to_str(self, authorship: Union["Reader", Authorship]) -> str:
        """Make a string from the authorship."""
        return "\n".join(self.to_lines(authorship))

    def print(self, authorship: Union["Reader", Authorship], **kwargs) -> None:  # noqa:T202
        """Print the authorship."""
        print(self.to_str(authorship), **kwargs)  # noqa:T201

    def write(self, authorship: Union["Reader", Authorship], *, path: Union[str, Path]) -> None:
        """Write the authorship to a path."""
        Path(path).resolve().write_text(self.to_str(authorship))
