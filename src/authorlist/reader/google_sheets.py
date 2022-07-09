"""Pandas dataframe reader."""

from typing import Union

import pandas as pd

from ..api import Author, Authorship, Institution, Reader
from ..constants import get_hoyt_google_sheets_df, hoyt_sort_key, safe

__all__ = [
    "SheetReader",
    "GoogleSheetReader",
]

AFFILIATION_KEYS = ["Affiliation", "Affiliation 2"]


class SheetReader(Reader):
    """Read from a pandas dataframe."""

    def __init__(self, df: pd.DataFrame, *, sort_middle_authors: bool = True):
        """Initialize the sheet reader.

        :param df:
            The dataframe representing the authorship. Find an example of a
            spreadsheet following the appropriate format at
            https://docs.google.com/spreadsheets/d/1Fo1YH3ZzOVrQ4wzKnBm6sPha5hZG66-u-uSMDGUvguI
        :param sort_middle_authors:
            Should the middle authors (i.e., ones that don't have "Lead" or "Senior" in their
            role column) be automatically sorted by last name alphabetical order? Defaults
            to true, since middle authorship order isn't usually meaningful.
        """
        self.df = df
        self.sort_middle_authors = sort_middle_authors

    def get_authorship(self) -> Authorship:
        """Get authors and institutions."""
        df = self.df
        column_to_idx = {column: i for i, column in enumerate(df.columns)}
        rows = sorted(df.values, key=hoyt_sort_key) if self.sort_middle_authors else list(df.values)

        institutions = {}
        for row in rows:
            for keys in [
                ("Affiliation", "Affiliation Address", "Affiliation ROR/Wikidata"),
                ("Affiliation 2", "Affiliation 2 Address", "Affiliation 2 ROR/Wikidata"),
            ]:
                name, address, uri = (safe(row[column_to_idx[key]]) for key in keys)
                if name is None:
                    continue
                if pd.isna(uri):
                    ror = None
                    wikidata = None
                elif uri.startswith("https://ror.org/"):
                    ror = uri.removeprefix("https://ror.org/")
                    wikidata = None
                elif uri.startswith("https://www.wikidata.org/wiki/"):
                    ror = None
                    wikidata = uri.removeprefix("https://www.wikidata.org/wiki/Q10279363")
                else:
                    ror = None
                    wikidata = None
                institutions[name] = Institution(
                    name=name,
                    address=address,
                    wikidata=wikidata,
                    ror=ror,
                )

        authors = []
        for row in rows:
            author = Author(
                first=safe(row[0]),
                middle=safe(row[1]),
                last=safe(row[2]),
                role=safe(row[3]),
                corresponding=row[3] == "Senior",
                email=safe(row[4]),
                orcid=safe(row[5]),
                wikidata=row[6].removeprefix("https://www.wikidata.org/wiki/")
                if pd.notna(row[6])
                else None,
                twitter=row[7].removeprefix("@") if pd.notna(row[7]) else None,
                institutions=[
                    institutions[row[column_to_idx[key]]]
                    for key in ["Affiliation", "Affiliation 2"]
                    if pd.notna(row[column_to_idx[key]])
                ],
                conflict=safe(row[14]),
            )
            authors.append(author)
        return Authorship(authors=authors, institutions=list(institutions.values()))


class GoogleSheetReader(SheetReader):
    """Read from google sheets.

    An example sheet that has the right template can be found at:
    https://docs.google.com/spreadsheets/d/1Fo1YH3ZzOVrQ4wzKnBm6sPha5hZG66-u-uSMDGUvguI
    """

    def __init__(
        self, google_sheet: str, *, gid: Union[str, int] = 0, sort_middle_authors: bool = True
    ):
        """Initialize the sheet reader.

        :param google_sheet: The identifier of the google sheet
        :param gid: The sheet identifier (in case there are more than one)
        :param sort_middle_authors:
            Should the middle authors (i.e., ones that don't have "Lead" or "Senior" in their
            role column) be automatically sorted by last name alphabetical order? Defaults
            to true, since middle authorship order isn't usually meaningful.
        """
        df = get_hoyt_google_sheets_df(google_sheet, gid)
        super().__init__(df, sort_middle_authors=sort_middle_authors)
