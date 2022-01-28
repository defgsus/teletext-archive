from typing import Dict, Generator, Tuple, Union, Optional

import bs4

from ..scraper import Scraper


class WDR(Scraper):

    NAME = "wdr"

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
