from typing import Dict, Generator, Tuple, Union, Optional

import bs4

from ..scraper import Scraper
from ..teletext import Teletext


class WDR(Scraper):

    NAME = "wdr"

    COLOR_CLASS_MAPPING = {
        "black": "b",
        "red": "r",
        "green": "g",
        "yellow": "y",
        "blue": "l",
        "magenta": "m",
        "cyan": "c",
        "white": "w",
    }

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:
        soup = self.get_soup("https://www1.wdr.de/wdrtext/index.html")

        for sub_index, content in self._iter_sub_pages(soup.find("div", {"id": "wdrtext_inner"})):
            yield 100, sub_index, content

        # get the link with the current session-id or whatever that is
        generic_href = self._get_href(soup)
        assert generic_href, f"special wdr page link not found"

        for page_index in range(101, 900):
            url = self._replace_page_num(generic_href, page_index)
            soup = self.get_soup(url)
            if soup:
                page_input = soup.find("input", {"name": "_page_num"})
                if page_input and page_input["value"] != str(page_index):
                    continue

                for sub_index, content in self._iter_sub_pages(soup.find("div", {"id": "wdrtext_inner"})):
                    yield page_index, sub_index, content

    def _iter_sub_pages(self, div: bs4.Tag) -> Generator[Tuple[int, str], None, None]:
        for sub_index in range(1, 100):
            sub_page = div.find("div", {"id": f"seite_{sub_index}"})
            if not sub_page:
                break

            yield sub_index, str(sub_page)

    def _get_href(self, soup: bs4.BeautifulSoup) -> Optional[str]:
        for a in soup.find_all("a"):
            href = a.get("href")
            if href and href.startswith("/wdrtext/externvtx100~_eam-") and "__page__num-" in href:
                return "https://www1.wdr.de" + href

    def _replace_page_num(self, href: str, num: int) -> str:
        idx = href.index("__page__num-")
        return href[:idx+12] + str(num) + href[idx+15:]

    def to_teletext(self, content: str) -> Teletext:
        soup = self.to_soup(content)
        tt = Teletext()
        for row in soup.find("div", {"class": "vt_table"}).find_all("div", {"class": "vt_row"}):
            if row.find("div", {"class": "vt_row"}):
                print(row)
                continue
            tt.new_line()
            for elem in row.children:
                if elem.name != "div":
                    continue

                for span in elem.find_all("span"):
                    if "invisible" in (span.get("class") or []):
                        span.clear()

                block = Teletext.Block("")

                classes = elem["class"]
                num_cols = None
                for cls in classes:
                    if cls in self.COLOR_CLASS_MAPPING:
                        block.color = self.COLOR_CLASS_MAPPING[cls]
                    elif cls[3:] in self.COLOR_CLASS_MAPPING:
                        block.bg_color = self.COLOR_CLASS_MAPPING[cls[3:]]
                    elif cls.startswith("col"):
                        num_cols = int(cls[3:])

                block.text = elem.find("span").text.replace("\n", "")
                a = elem.find("a")
                if a:
                    block.text = a.text
                    link = int(a["href"].split("?", 1)[0][-8:-5])
                    block.link = link

                if num_cols:
                    block.text = block.text[:num_cols]

                if block.text:
                    tt.add_block(block)

        return tt
