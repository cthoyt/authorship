"""Readers."""

from class_resolver import ClassResolver

from .google_sheets import GoogleSheetReader, SheetReader
from .obo_sheet import OboGoogleSheetReader, OboSheetReader
from ..api import Reader

__all__ = [
    "reader_resolver",
    # Concrete classes
    "SheetReader",
    "GoogleSheetReader",
    "OboSheetReader",
    "OboGoogleSheetReader",
]

reader_resolver: ClassResolver[Reader] = ClassResolver.from_subclasses(Reader)
