# -*- coding: utf-8 -*-

"""Write an author list as text, e.g., for Microsoft Word or Google Docs."""

from operator import itemgetter
from typing import Iterable

from ..api import Authorship, Writer
from ..constants import SUPERSCRIPTS_TRANS

__all__ = [
    "TextWriter",
]


class TextWriter(Writer):
    """Write an authorship as text."""

    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate over text lines."""
        affiliation_counts: dict[str, int] = {}
        for author in authorship.authors:
            local_numbering = []
            for affiliation in author.institutions:
                local_numbering.append(affiliation)
                if affiliation.name not in affiliation_counts:
                    affiliation_counts[affiliation.name] = len(affiliation_counts)

            affiliation_text = "𝄒".join(
                str(affiliation_counts[affiliation.name] + 1).translate(SUPERSCRIPTS_TRANS)
                for affiliation in local_numbering
            )
            yield f"{author.name}{affiliation_text}"

        yield ""
        for affiliation_name, index in sorted(affiliation_counts.items(), key=itemgetter(1)):
            yield f"{index + 1}. {affiliation_name}"
