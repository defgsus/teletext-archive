from typing import Dict, Generator, Tuple, Union, Optional

import bs4

from ..scraper import Scraper
from ..teletext import Teletext
from ..console import ConsoleColors as C


class ARD(Scraper):

    NAME = "ard"

    COLOR_CLASS_MAPPING = {
        "bl": "l"
    }

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

    def to_teletext(self, content: str) -> Teletext:
        soup = self.to_soup(content)
        tt = Teletext()
        for line in soup.find("div", {"id": "page_1"}).find_all("div"):
            tt.new_line()

            for nobr in line.find_all("nobr"):

                block = Teletext.Block("")

                if nobr.parent.name == "span":
                    for cls in nobr.parent.get("class"):
                        if cls.startswith("fg"):
                            block.color = self.COLOR_CLASS_MAPPING.get(cls[2:], cls[2:])
                        elif cls.startswith("bg"):
                            block.bg_color = self.COLOR_CLASS_MAPPING.get(cls[2:], cls[2:])

                for c in nobr.children:
                    if isinstance(c, bs4.NavigableString):
                        block.text += c.text
                    elif c.name == "a":
                        block.text += c.text
                    elif c.name == "img":
                        block.text += self._get_img_tt_char(c.get("src"))
                    else:
                        self.log(f"unhandled element {c}")

                if block.text:
                    tt.add_block(block)

        return tt

    @classmethod
    def _get_img_tt_char(cls, url: str) -> str:
        """
        Convert image url to unicode str

        https://en.wikipedia.org/wiki/Teletext_character_set#G1_block_mosaics
        """
        try:
            code = int(url[-6:-4], 16)
            return chr(0x1fb00 + code - 0x21)
        except ValueError:
            return "?"
