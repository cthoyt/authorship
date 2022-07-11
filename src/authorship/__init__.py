# -*- coding: utf-8 -*-

"""Format author lists for academic texts and journal submissions."""

from .models import Author, Authorship, Institution
from .readers import (
    GoogleSheetReader,
    OboGoogleSheetReader,
    OboSheetReader,
    PreparedReader,
    Reader,
    SheetReader,
    reader_resolver,
)
from .writers import (
    BiorxivWriter,
    CitationCFFWriter,
    ScientificDataWriter,
    TextWriter,
    Writer,
    writer_resolver,
)

__all__ = [
    # Models
    "Institution",
    "Author",
    "Authorship",
    # Readers
    "reader_resolver",
    "Reader",
    "PreparedReader",
    "OboSheetReader",
    "OboGoogleSheetReader",
    "SheetReader",
    "GoogleSheetReader",
    # Writers
    "writer_resolver",
    "Writer",
    "BiorxivWriter",
    "TextWriter",
    "ScientificDataWriter",
    "CitationCFFWriter",
]
