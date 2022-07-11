"""Write an author list for the CITATION.cff file on GitHub."""

from textwrap import dedent
from typing import Iterable

from .base import Writer
from ..models import Authorship

__all__ = [
    "CitationCFFWriter",
]


class CitationCFFWriter(Writer):
    """Write an author list for the CITATION.cff file on GitHub."""

    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate lines."""
        yield "authors:"
        for author in authorship.authors:
            given = f"{author.first} {author.middle}" if author.middle else author.first
            yield dedent(
                f"""\
            - family-names: "{author.last}"
              given-names: "{given}"
              orcid: "https://orcid.org/{author.orcid}"
            """
            ).rstrip()
