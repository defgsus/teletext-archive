import os
import sys
from pathlib import Path
from typing import Generator, Tuple

import requests

scraper_classes = dict()


class Scraper:

    # must be filename compatible
    NAME: str = None

    NUM_PAGE_DIGITS: int = 3
    NUM_SUB_PAGE_DIGITS: int = 2
    FILE_EXTENSION: str = "html"

    BASE_PATH: Path = Path(__file__).resolve().parent.parent / "docs" / "snapshots"

    def __init_subclass__(cls, **kwargs):
        assert cls.NAME, cls
        if cls.NAME in scraper_classes:
            raise AssertionError(f"Duplicate name '{cls.NAME}' for class {cls.__name__}")

        scraper_classes[cls.NAME] = cls

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "github.com/defgsus/teletext-archive"
        }

    @classmethod
    def path(cls) -> Path:
        return cls.BASE_PATH / cls.NAME

    def iter_pages(self) -> Generator[Tuple[int, int, str], None, None]:
        """
        Yield tuples of (page-number, sub-page-number, html)
        """
        raise NotImplementedError

    def full_download(self):
        os.makedirs(str(self.path()), exist_ok=True)
        for page_num, sub_page_num, content in self.iter_pages():
            filename = self.path() / (
                f"{page_num:0{self.NUM_PAGE_DIGITS}}"
                f"-{sub_page_num:0{self.NUM_SUB_PAGE_DIGITS}}.{self.FILE_EXTENSION}"
            )
            self.log("storing", filename)
            filename.write_text(content)

    def log(self, *args):
        if self.verbose:
            print(f"{self.__class__.__name__}:", *args, file=sys.stderr)
