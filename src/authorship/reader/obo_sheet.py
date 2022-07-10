"""Pandas dataframe reader."""

import logging
from typing import Union

import pandas as pd

from ..api import Author, Authorship, Institution, Reader
from ..constants import get_obo_google_sheets_df, safe

__all__ = [
    "OboSheetReader",
    "OboGoogleSheetReader",
]

logger = logging.getLogger(__name__)

EXAMPLE = "1NfhibWHOKgV2glmgRdKMzHEzTCw2_dUq_t0Zq64cgeQ"
COLUMNS = [
    "First name",
    "Middle (optional)",
    "Last name",
    "Author Position",
    "Author Confirm",
    "Email",
    "ORCID",
    "Wikidata",
    "Twitter",
    "Organization + location (will separate later)",
]


class OboSheetReader(Reader):
    """Read from a pandas dataframe."""

    def __init__(self, df: pd.DataFrame):
        """Initialize the sheet reader.

        :param df:
            The dataframe representing the authorship. Find an example of a
            spreadsheet following the appropriate format at one of:

            - SSSOM paper https://docs.google.com/spreadsheets/d/1NfhibWHOKgV2glmgRdKMzHEzTCw2_dUq_t0Zq64cgeQ
            - ODK paper https://docs.google.com/spreadsheets/d/1JMo1ZyytnJGXr7biYqxMzV7DIAzlfyum5jcrtetG8lI
            - CL paper https://docs.google.com/spreadsheets/d/1G9b6NOyUkMJUI2ZiCWoFSDdoKf1KWdfTwlDoTJ4zntM
              (broken since many authors missing email/orcid)
        """
        self.df = df

    def get_authorship(self) -> Authorship:
        """Get authors and institutions."""
        df = self.df
        org_sheet = df[df.columns[-2:]]
        org_sheet.columns = ["code", "institution"]
        code_to_institution: dict[int, Institution] = {
            int(code): get_org(text) for code, text in org_sheet[org_sheet["code"].notna()].values
        }

        author_sheet = df[df.columns[:-2]]
        author_sheet = author_sheet[author_sheet[author_sheet.columns[0]].notna()]
        authors = [get_author(row, code_to_institution) for _, row in author_sheet.iterrows()]
        return Authorship(authors=authors, institutions=list(code_to_institution.values()))


class OboGoogleSheetReader(OboSheetReader):
    """Read from google sheets.

    An example sheet that has the right template can be found at:
    https://docs.google.com/spreadsheets/d/1NfhibWHOKgV2glmgRdKMzHEzTCw2_dUq_t0Zq64cgeQ
    using ``skiprows=1``
    """

    def __init__(
        self,
        google_sheet: str,
        *,
        gid: Union[str, int] = 0,
        skiprows=None,
    ):
        """Initialize the sheet reader.

        :param google_sheet: The identifier of the google sheet
        :param gid: The sheet identifier (in case there are more than one)
        :param skiprows: Should rows be skipped?
        """
        df = get_obo_google_sheets_df(google_sheet, gid, skiprows=skiprows)
        super().__init__(df)


def get_org(text: str) -> Institution:
    """Get an institution."""
    return Institution(
        name=text,  # todo parse out address
    )


def get_author(row, code_to_institution: dict[int, Institution]) -> Author:
    """Get an author from a row."""
    first = row["First name"]
    last = row["Last name"]
    codes = [
        int(key.strip()) for key in row["Organization + location (will separate later)"].split(",")
    ]
    institutions = []
    for code in codes:
        if code not in code_to_institution:
            logger.warning("missing organization code %d for %s%s", code, first, last)
        else:
            institutions.append(code_to_institution[code])
    if not institutions:
        raise ValueError(f"no affiliation for {first} {last}")

    return Author(
        first=row["First name"],
        middle=safe(row["Middle (optional)"]),
        last=row["Last name"],
        email=safe(row["Email"]),
        orcid=row["ORCID"],
        wikidata=row["Wikidata"].removeprefix("https://www.wikidata.org/wiki/")
        if pd.notna(row["Wikidata"])
        else None,
        twitter=row["Twitter"].removeprefix("@") if pd.notna(row["Twitter"]) else None,
        institutions=institutions,
    )
