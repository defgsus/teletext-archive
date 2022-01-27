import argparse
import datetime
import traceback
from typing import List

from src.scraper import scraper_classes
import src.sources


def parse_args() -> dict:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--filter", type=str, nargs="*",
        help="One or more scraper names to limit the download"
    )
    parser.add_argument(
        "-v", "--verbose", type=bool, nargs="?", default=False, const=True,
        help="Print a lot of stuff"
    )

    return vars(parser.parse_args())


def main(filter: List[str], verbose: bool):

    filtered_classes = []
    for name in sorted(scraper_classes.keys()):
        if not filter or name in filter:
            filtered_classes.append(scraper_classes[name])

    print(f"update @ {datetime.datetime.utcnow().replace(microsecond=0)} UTC")

    for scraper_class in filtered_classes:

        scraper = scraper_class(verbose=verbose)
        print(f"\n### {scraper.NAME}\n")
        try:
            report = scraper.download()

            for key, value in report.items():
                if value:
                    print(f"- {value} pages {key}")

        except Exception as e:
            print(f"```\n{traceback.format_exc(limit=-2)}```")


if __name__ == "__main__":
    main(**parse_args())
