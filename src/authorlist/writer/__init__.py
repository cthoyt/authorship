"""Writers."""

from class_resolver import ClassResolver

from .biorxiv import BiorxivWriter
from .nature_scientific_data import ScientificDataWriter
from .text import TextWriter
from ..api import Writer

__all__ = [
    "writer_resolver",
    # Concrete classes
    "TextWriter",
    "BiorxivWriter",
    "ScientificDataWriter",
]

writer_resolver: ClassResolver[Writer] = ClassResolver.from_subclasses(Writer)
