from typing import Dict, Generator, Tuple, Union, Optional

import bs4

from ..scraper import Scraper


class ARD(Scraper):

    NAME = "ard"

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:
        page_index = 100
        while page_index < 900:
            response = self.get_html(self._get_url(page_index, 1), allow_redirects=False)
            if response.status_code == 302:
                new_page_index = int(response.headers["location"][-3:])
                if new_page_index < page_index:
                    break
                page_index = new_page_index
                continue

            soup = bs4.BeautifulSoup(response.text, features="html.parser")
            if soup:
                teletext = soup.find("div", {"id": "ardtext_classic"})
                if teletext:
                    yield page_index, 1, str(teletext)

                sub_page_div = soup.find("div", {"id": "output_unterseite"})
                if sub_page_div:
                    num_pages = int(sub_page_div.text.split("/")[-1])

                    for sub_page_index in range(2, num_pages + 1):
                        soup = self.get_soup(self._get_url(page_index, sub_page_index))
                        if soup:
                            teletext = soup.find("div", {"id": "ardtext_classic"})
                            if teletext:
                                yield page_index, sub_page_index, str(teletext)
            page_index += 1

    def _get_url(self, page_index: int, sub_page_index: int) -> str:
        return f"https://www.ard-text.de/index.php?page={page_index}&sub={sub_page_index}"
