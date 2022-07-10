"""Constants."""

from typing import Literal, Union, cast

import pandas as pd

__all__ = [
    "ROLE",
    "SUPERSCRIPTS",
    "SUPERSCRIPTS_TRANS",
    "hoyt_sort_key",
    "get_hoyt_google_sheets_df",
]

ROLES = Literal["Lead", "Senior"]

ROLE: dict[ROLES, int] = {"Lead": 0, "Senior": 2}

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


def hoyt_sort_key(row: tuple[str, ...]) -> tuple[int, str]:
    """Sort a row by author role.

    Lead goes first, senior goes last, everyone else middle) then by last name within the middle authors.

    :param row: A row from a hoyt-style sheet.
    :returns: A valid sort tuple
    """
    return ROLE.get(cast(ROLES, row[3]), 1), row[2]


def get_hoyt_google_sheets_df(google_sheet: str, gid: Union[str, int] = 0) -> pd.DataFrame:
    """Get the dataframe from google."""
    url = f"https://docs.google.com/spreadsheets/d/{google_sheet}/export?format=tsv&gid={gid}"
    return pd.read_csv(url, sep="\t", skiprows=1)


def get_obo_google_sheets_df(
    google_sheet: str, gid: Union[str, int] = 0, skiprows=None
) -> pd.DataFrame:
    """Get the dataframe from google."""
    url = f"https://docs.google.com/spreadsheets/d/{google_sheet}/export?format=tsv&gid={gid}"
    return pd.read_csv(url, sep="\t", skiprows=skiprows)


def safe(y):
    """Get a value or convert NaN to none."""
    return None if pd.isna(y) else y
