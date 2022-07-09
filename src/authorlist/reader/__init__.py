"""Readers."""

from class_resolver import ClassResolver

from .google_sheets import GoogleSheetReader, SheetReader
from ..api import Reader

__all__ = [
    "reader_resolver",
    # Concrete classes
    "SheetReader",
    "GoogleSheetReader",
]

reader_resolver: ClassResolver[Reader] = ClassResolver.from_subclasses(Reader)
