"""Constants."""

from typing import Literal, Union, cast

import pandas as pd
from ..api import Reader, Authorship, Author, Institution
from ..constants import sort_key, get_google_sheets_df

__all__ = [
    "SheetReader",
    "GoogleSheetReader",
]

AFFILIATION_KEYS = ["Affiliation", "Affiliation 2"]


class SheetReader(Reader):
    """Read from google sheets."""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_author_list(self) -> Authorship:
        df = self.df
        column_to_idx = {column: i for i, column in enumerate(df.columns)}
        rows = sorted(df.values, key=sort_key)

        institutions = {}
        for row in rows:
            for keys in [
                ("Affiliation", "Affiliation Address", "Affiliation ROR/Wikidata"),
                ("Affiliation 2", "Affiliation 2 Address", "Affiliation 2 ROR/Wikidata"),
            ]:
                name, address, uri = (row[column_to_idx[key]] for key in keys)
                if uri.startswith("https://ror.org/"):
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
                first=row[0],
                middle=row[1],
                last=row[2],
                corresponding=row[3] == "Senior",
                instititutions=[
                    institutions[key]
                    for key in ["Affiliation", "Affiliation 2"]
                    if pd.notna(key)
                ],
            )
            authors.append(author)
        return Authorship(authors=authors, institutions=list(institutions.values()))


class GoogleSheetReader(SheetReader):
    """Read from google sheets."""

    def __init__(self, google_sheet: str, gid: Union[str, int] = 0):
        super().__init__(get_google_sheets_df(google_sheet, gid))
