import argparse
from typing import List

from src.scraper import scraper_classes
import src.sources


def parse_args() -> dict:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--filter", type=str, nargs="*",
        help="One or more scraper names to limit the download"
    )

    return vars(parser.parse_args())


def main(filter: List[str]):

    filtered_classes = []
    for name in scraper_classes.keys():
        if not filter or name in filter:
            filtered_classes.append(scraper_classes[name])

    for scraper_class in filtered_classes:

        scraper = scraper_class(verbose=True)
        scraper.full_download()


if __name__ == "__main__":
    main(**parse_args())
