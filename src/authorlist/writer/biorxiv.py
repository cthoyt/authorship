"""Generate author list text from a Google Sheet."""

import click
import pandas as pd

from ..constants import get_google_sheets_df, sort_key

HEADER = [
    "Email",
    "Institution",
    "First Name",
    "Middle Name(s)/Initial(s)",
    "Last Name",
    "Suffix",
    "Corresponding Author",
    "Home Page URL",
    "Collaborative Group/Consortium",
    "ORCiD",
]


@click.command()
@click.option("--google_sheet")
@click.option("--gid", type=int, default=0)
@click.option("--output", type=click.File("w"))
def main(google_sheet: str, gid: int, output):
    """Create author list text from a google sheet."""
    df = get_google_sheets_df(google_sheet, gid)
    column_to_idx = {column: i for i, column in enumerate(df.columns)}

    rows = sorted(df.values, key=sort_key)
    affiliation_counts = {}
    output_rows = []
    for row in rows:
        affiliations = []
        for affiliation_key in ["Affiliation", "Affiliation 2"]:
            affiliation = row[column_to_idx[affiliation_key]]
            if pd.notna(affiliation):
                affiliations.append(affiliation)
                if affiliation not in affiliation_counts:
                    affiliation_counts[affiliation] = len(affiliation_counts)

        output_rows.append(
            (
                row[4],  # email
                row[8],  # institution
                row[0],  # first name
                row[1],  # middle name
                row[2],  # last name
                "",  # suffix,
                "x" if row[3] == "Senior" else "",  # corresponding
                row[6],  # home page
                "",  # Collaborative Group/Consortium
                row[5],  # orcid
            )
        )

    # TODO sanitize unicode characters
    df = pd.DataFrame(output_rows, columns=HEADER)
    df.to_csv(output, sep="\t", index=False)


if __name__ == "__main__":
    main()
