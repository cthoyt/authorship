"""Write an author list for the LaTeX template provided by Oxford Bioinformatics."""

from operator import itemgetter
from typing import Iterable, Optional

from authorship.models import Author, Authorship
from authorship.writers.base import Writer

__all__ = [
    "OxfordBioinformaticsDataWriter",
]


class OxfordBioinformaticsDataWriter(Writer):
    """Write an author list for the latex template for Oxford Bioinformatics."""

    def iter_lines(self, authorship: Authorship) -> Iterable[str]:
        """Iterate lines."""
        corresponding: Optional[Author] = None
        affiliation_counts: dict[str, int] = {}

        authors_ = []

        for author in authorship.authors:
            local_numbering = []
            for affiliation in author.institutions:
                local_numbering.append(affiliation)
                if affiliation.name not in affiliation_counts:
                    affiliation_counts[affiliation.name] = len(affiliation_counts)

            xx = []
            for affiliation in local_numbering:
                xx.append(rf"\text{{\sfb {affiliation_counts[affiliation.name] + 1}}}")
            if author.role == "Senior":
                xx.append("*")
                corresponding = author

            author_text = author.name
            affiliation_text = ",".join(xx)
            authors_.append((author_text, affiliation_text))

        yield rf"\author[{authorship.authors[0].last} \textit{{et~al}}.]{{%"
        for author_name, affiliation_text in authors_:
            yield f"    {author_name}\\,$^{{{affiliation_text}}}$,"  # TODO add and for penultimate instead of comma
        yield "}"

        yield r"\address{%"
        for _affiliation, index in sorted(affiliation_counts.items(), key=itemgetter(1)):
            yield rf"    $^{{\text{{\sf {index + 1}}}}}${{{_affiliation}}} \\"  # TODO don't add on last
        yield "}"

        corresponding_email = corresponding.email.replace("_", "\_")
        yield rf"\textbf{{Contact:}} \href{{{corresponding_email}}}{{{corresponding_email}}}\\"


def _main():
    gid = "1EK3QwjQsTl2Qorpj_JRI306Uwr7VNPYgtADSkUQsB-0"
    from authorship import GoogleSheetReader

    reader = GoogleSheetReader(gid)
    writer = OxfordBioinformaticsDataWriter()
    writer.print(reader)


if __name__ == "__main__":
    _main()
