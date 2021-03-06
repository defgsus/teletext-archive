import json
from typing import Dict, Generator, Tuple, Union, Optional

import bs4

from ..scraper import Scraper
from ..teletext import Teletext


class SR(Scraper):

    NAME = "sr"

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:

        page_index = 100
        sub_page_index = 1
        while page_index < 900:
            url = f"https://www.saartext.de/{page_index}/{sub_page_index:02d}"
            soup = self.get_soup(url)

            content_tag = soup.find("pre", {"class": "saartext_page"})
            yield self._to_yield_page(page_index, sub_page_index, str(content_tag))

            next_a = soup.find("a", {"id": "nextButton"})
            next_page = next_a["href"].strip("/").split("/")

            new_page_index = int(next_page[0])
            if len(next_page) == 1:
                sub_page_index = 1
            else:
                sub_page_index = int(next_page[1].lstrip("0"))

            if new_page_index < page_index:
                break

            page_index = new_page_index

    def _to_yield_page(self, page_index: int, sub_page_index: int, content: str) -> Tuple[int, int, Union[str, bool]]:
        if not self._is_page_different(page_index, sub_page_index, content):
            content = True
        return page_index, sub_page_index, content

    def _is_page_different(self, page_index: int, sub_page_index: int, new_content: str) -> bool:
        filename = self.to_filename(page_index, sub_page_index)
        if not filename.exists():
            return True

        # see if something else than the date has changed

        old_content = filename.read_text().splitlines()[1:]
        new_content = new_content.splitlines()[1:]

        return old_content != new_content

    def to_teletext(self, content: str) -> Teletext:
        soup = self.to_soup(content)
        tt = Teletext()
        tt.new_line()
        for elem in soup.find("pre").children:

            if isinstance(elem, bs4.NavigableString):
                tt.add_block(Teletext.Block(elem))

            elif elem.name == "a":
                link = tuple(int(n) for n in filter(bool, elem["href"].split("/")))
                tt.add_block(Teletext.Block(elem.text, link=link))

            else:
                self.log(f"unhandled element {elem}")

        return tt
