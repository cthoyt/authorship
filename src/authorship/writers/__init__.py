"""Writers."""

from class_resolver import ClassResolver

from .base import Writer
from .biorxiv import BiorxivWriter
from .citation_cff import CitationCFFWriter
from .nature_scientific_data import ScientificDataWriter
from .text import TextWriter

__all__ = [
    "Writer",
    "writer_resolver",
    # Concrete classes
    "TextWriter",
    "BiorxivWriter",
    "ScientificDataWriter",
    "CitationCFFWriter",
]

writer_resolver: ClassResolver[Writer] = ClassResolver.from_subclasses(Writer)
