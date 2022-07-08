"""Generate author list text from a Google Sheet."""

from operator import itemgetter

import click
import pandas as pd

from ..constants import ROLE, SUPERSCRIPTS, SUPERSCRIPTS_TRANS, get_google_sheets_df, sort_key


@click.command()
@click.option("--google_sheet")
@click.option("--gid", type=int, default=0)
def main(google_sheet: str, gid: int):
    """Create author list text from a google sheet."""
    df = get_google_sheets_df(google_sheet, gid)
    column_to_idx = {column: i for i, column in enumerate(df.columns)}

    rows = sorted(df.values, key=sort_key)
    affiliation_counts = {}
    names = []
    corresponding_name = None
    for row in rows:
        affiliations = []
        for affiliation_key in ["Affiliation", "Affiliation 2"]:
            affiliation = row[column_to_idx[affiliation_key]]
            if pd.notna(affiliation):
                affiliations.append(affiliation)
                if affiliation not in affiliation_counts:
                    affiliation_counts[affiliation] = len(affiliation_counts)

        affiliation_text = ",".join(
            str(affiliation_counts[affiliation] + 1) for affiliation in affiliations
        )
        if pd.notna(row[1]):
            # there's a middle name/initial
            name = f"{row[0]} {row[1]} {row[2]}"
        else:
            name = f"{row[0]} {row[2]}"
        if row[3] == "Lead":
            affiliation_text = f"{affiliation_text},*"
            corresponding_name = name

        names.append(rf"\author[{affiliation_text}]{{{name}}}")

    print(*names, sep="\n")

    for affiliation, index in sorted(affiliation_counts.items(), key=itemgetter(1)):
        print(rf"\affil[{index + 1}]{{{affiliation}}}")

    print(rf"\affil[*]{{corresponding author(s): {corresponding_name} (FIXME)}}")


if __name__ == "__main__":
    main()
