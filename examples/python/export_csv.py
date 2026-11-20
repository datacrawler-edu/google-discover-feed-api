"""Export the Dataset of an existing run. Does not start a new run."""
import argparse
import csv
from pathlib import Path

from request import fetch_result


def export(run_id, destination, **connection):
    items = fetch_result(run_id, **connection)["cards"]
    columns = list(dict.fromkeys(key for row in items for key in row))
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns or ["url"])
        writer.writeheader()
        writer.writerows(items)
    return len(items)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(f"Exported {export(args.run_id, args.destination)} cards.")
