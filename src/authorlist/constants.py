"""Constants."""

from typing import Union

import pandas as pd

__all__ = [
    "ROLE",
    "SUPERSCRIPTS",
    "SUPERSCRIPTS_TRANS",
    "sort_key",
    "get_google_sheets_df",
]

ROLE = {"Lead": 0, "Senior": 2}

SUPERSCRIPTS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}
SUPERSCRIPTS_TRANS = str.maketrans(SUPERSCRIPTS)


def sort_key(row: tuple[str, ...]) -> tuple[int, str]:
    """
    Sort rows first by author role (i.e., lead goes first, senior goes
    last, everyone else middle) then by last name within the middle authors.
    """
    return ROLE.get(row[3], 1), row[2]


def get_google_sheets_df(google_sheet: str, gid: Union[str, int]) -> pd.DataFrame:
    """Get the dataframe from google."""
    url = f"https://docs.google.com/spreadsheets/d/{google_sheet}/export?format=tsv&gid={gid}"
    return pd.read_csv(url, sep="\t", skiprows=1)
