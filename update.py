import argparse
import datetime
import traceback
from multiprocessing.pool import ThreadPool
from typing import List

from src.scraper import Scraper, scraper_classes
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
    parser.add_argument(
        "-j", "--threads", type=int, default=1,
        help="Number of parallel threads (per scraper)"
    )

    return vars(parser.parse_args())


def scrape(scraper: Scraper) -> str:
    """
    Run the scraper, return result message text
    """
    msg = f"### {scraper.NAME}\n\n"

    try:
        report = scraper.download()

        for key, value in report.items():
            if value:
                msg += f"- {value} pages {key}\n"

    except Exception as e:
        msg += f"```\n{traceback.format_exc(limit=-2)}```"

    return msg


def main(filter: List[str], verbose: bool, threads: int):

    filtered_classes = []
    for name in sorted(scraper_classes.keys()):
        if not filter or name in filter:
            filtered_classes.append(scraper_classes[name])

    print(f"update @ {datetime.datetime.utcnow().replace(microsecond=0)} UTC\n")

    scrapers = [
        scraper_class(verbose=verbose)
        for scraper_class in filtered_classes
    ]

    messages = ThreadPool(threads).map(scrape, scrapers)
    messages.sort()

    print("\n".join(messages))


if __name__ == "__main__":
    main(**parse_args())
