"""Write an author list for bioRxiv bulk upload."""

from typing import Iterable

from ..api import Author, Authorship, Writer

HEADER = [
    "Email",
    "Institution",
    "First Name",
    "Middle Name(s)/Initial(s)",
    "Last Name",
    "Suffix",
    "Corresponding Author",
    "Home Page URL",
    "Collaborative Group/Consortium",
    "ORCiD",
]


class BiorxivWriter(Writer):
    """Write output for bioRxiv bulk author import."""

    def author_to_row(self, author: Author) -> tuple[str, ...]:
        """Make a row from an author."""
        return (
            author.email,
            author.institutions[0].name,
            author.first,
            author.middle or "",
            author.last,
            "",  # suffix
            "x" if author.role == "Senior" else "",  # corresponding
            f"https://bioregistry.io/wikidata:{author.wikidata}",  # homepage TODO look up from wikidata
            "",  # Collaborative Group/Consortium
            author.orcid,
        )

    def iter_rows(self, authorship: Authorship) -> Iterable[tuple[str, ...]]:
        """Iterate over all author rows."""
        for author in authorship.authors:
            yield self.author_to_row(author)

    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate over lines for a bioRxiv author template."""
        yield "\t".join(HEADER)
        for row in self.iter_rows(authorship):
            yield "\t".join(row)
