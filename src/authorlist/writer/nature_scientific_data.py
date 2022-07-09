"""Write an author list for the LaTeX template provided by Nature Scientific Data."""

from operator import itemgetter
from typing import Iterable, Optional

from ..api import Author, Authorship, Writer

__all__ = [
    "ScientificDataWriter",
]


class ScientificDataWriter(Writer):
    """Write an author list for the latex template for Nature Scientific Data."""

    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate lines."""
        corresponding: Optional[Author] = None
        affiliation_counts: dict[str, int] = {}
        for author in authorship.authors:
            local_numbering = []
            for affiliation in author.institutions:
                local_numbering.append(affiliation)
                if affiliation.name not in affiliation_counts:
                    affiliation_counts[affiliation.name] = len(affiliation_counts)

            affiliation_text = ",".join(
                str(affiliation_counts[affiliation.name] + 1) for affiliation in local_numbering
            )
            if author.role == "Senior":
                affiliation_text = f"{affiliation_text},*"
                corresponding = author
            yield rf"\author[{affiliation_text}]{{{author.name}}}"

        for _affiliation, index in sorted(affiliation_counts.items(), key=itemgetter(1)):
            yield rf"\affil[{index + 1}]{{{_affiliation}}}"

        if corresponding is not None:
            yield rf"\affil[*]{{corresponding author(s): {corresponding.name} ({corresponding.email})}}"
