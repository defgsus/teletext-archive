import re
import urllib.parse
from typing import Dict, Generator, Tuple, Union, Optional

import bs4

from ..scraper import Scraper
from ..teletext import Teletext


class DreiSAT(Scraper):

    NAME = "3sat"

    _RE_PAGE_URL = re.compile(r".*\?p=(\d\d\d)_(\d\d\d\d)&.*")

    _RE_TTX_STYLES = {
        "top": re.compile(r".*top:\s*(\d+)px"),
        "left": re.compile(r".*left:\s*(\d+)px"),
        "bc": re.compile(r".*background-color:\s*#([0-9a-f]+)"),
        "pos": re.compile(r".*background-position:\s*(-?\d+)px\s+(-?\d+)px"),
    }

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:
        page_index = 100
        sub_page_index = 1

        while page_index < 900:
            url = f"https://blog.3sat.de/ttx/index.php?p={page_index}_{sub_page_index:04d}&c=0"
            soup = self.get_soup(url)

            content_tag = soup.find("div", {"id": "ttxbody"})
            yield page_index, sub_page_index, str(content_tag)

            next_page_index, next_sub_page_index = self._get_next_page(soup, "nextsub")

            if next_page_index < page_index:
                break

            if (next_page_index, next_sub_page_index) == (page_index, sub_page_index) \
                    or next_sub_page_index < sub_page_index:
                next_page_index, next_sub_page_index = self._get_next_page(soup, "nextpage")
                if next_page_index < page_index:
                    break

            page_index, sub_page_index = next_page_index, next_sub_page_index

    def _get_next_page(self, soup: bs4.BeautifulSoup, tag_id: str) -> Tuple[int, int]:
        next_a = soup.find("a", {"id": tag_id})
        next_href = urllib.parse.urljoin("https://blog.3sat.de", next_a["href"])

        match = self._RE_PAGE_URL.match(next_href)
        new_page_index, sub_page_index = match.groups()

        return (
            int(new_page_index),
            int(sub_page_index.lstrip("0")),
        )

    def to_teletext(self, content: str) -> Teletext:
        soup = self.to_soup(content)

        matrix = [
            [(" ", "wb") for x in range(40)]
            for y in range(26)
        ]
        for elem in soup.find("div", {"id": "ttxbody"}).find_all("div"):
            style = elem["style"]
            params = dict()
            for key, regexp in self._RE_TTX_STYLES.items():
                match = regexp.match(style)
                params[key] = match.groups()

            x, y = int(params["left"][0]) // 12, int(params["top"][0]) // 12
            char_x, char_y = int(params["pos"][0]) // 12, int(params["pos"][1]) // 12
            char_code = -char_x - 16 * char_y
            char = chr(32 + char_code % 64)

            matrix[y][x] = (char, "wb")

        return Teletext.from_matrix(matrix)
