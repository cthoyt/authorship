# -*- coding: utf-8 -*-

"""Generate author list text from a Google Sheet."""

from operator import itemgetter

import click
import pandas as pd

from ..constants import SUPERSCRIPTS_TRANS, get_google_sheets_df, sort_key


@click.command()
@click.argument("google_sheet")
@click.option("--gid", type=int, default=0)
def main(google_sheet: str, gid: int):
    """Create author list text from a google sheet."""
    df = get_google_sheets_df(google_sheet, gid)
    column_to_idx = {column: i for i, column in enumerate(df.columns)}

    rows = sorted(df.values, key=sort_key)
    affiliation_counts = {}
    names = []
    for row in rows:
        affiliations = []
        for affiliation_key in ["Affiliation", "Affiliation 2"]:
            affiliation = row[column_to_idx[affiliation_key]]
            if pd.notna(affiliation):
                affiliations.append(affiliation)
                if affiliation not in affiliation_counts:
                    affiliation_counts[affiliation] = len(affiliation_counts)

        affiliation_text = "𝄒".join(
            str(affiliation_counts[affiliation] + 1).translate(SUPERSCRIPTS_TRANS)
            for affiliation in affiliations
        )

        if pd.notna(row[1]):
            # there's a middle name/initial
            name = f"{row[0]} {row[1]} {row[2]}{affiliation_text}"
        else:
            name = f"{row[0]} {row[2]}{affiliation_text}"
        names.append(name)

    print(", ".join(names))

    for affiliation, index in sorted(affiliation_counts.items(), key=itemgetter(1)):
        print(f"{index + 1}. {affiliation}")


if __name__ == "__main__":
    main()
