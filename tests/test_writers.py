"""Tests for writers."""

import unittest

from authorship import writer_resolver
from authorship.readers import GoogleSheetReader, Reader


class TestWriters(unittest.TestCase):
    """Test writers."""

    reader: Reader

    def setUp(self) -> None:
        """Set up the test case with a reader."""
        self.reader = GoogleSheetReader("1Fo1YH3ZzOVrQ4wzKnBm6sPha5hZG66-u-uSMDGUvguI")

    def test_print(self):
        """Test the print function."""
        for writer_cls in writer_resolver:
            with self.subTest(writer=writer_resolver.normalize_cls(writer_cls)):
                self.reader.print(writer_cls)
