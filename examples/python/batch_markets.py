"""Collect one bounded snapshot per requested market."""
import argparse
import json

from request import fetch_result, start


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markets", nargs="+", choices=("us", "es", "gb"))
    args = parser.parse_args()
    for market in dict.fromkeys(args.markets):
        run_id = start({"country": market, "maxArticles": 5})
        print(json.dumps({"market": market, **fetch_result(run_id)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
