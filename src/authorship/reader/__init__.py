"""Readers."""

from class_resolver import ClassResolver

from .base import Reader
from .google_sheets import GoogleSheetReader, SheetReader
from .obo_sheet import OboGoogleSheetReader, OboSheetReader

__all__ = [
    "Reader",
    "reader_resolver",
    # Concrete classes
    "SheetReader",
    "GoogleSheetReader",
    "OboSheetReader",
    "OboGoogleSheetReader",
]

reader_resolver: ClassResolver[Reader] = ClassResolver.from_subclasses(Reader)
