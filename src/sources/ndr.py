import re
from typing import Dict, Generator, Tuple, Union

from ..scraper import Scraper


class NDR(Scraper):

    NAME = "ndr"

    FILE_EXTENSION = "htm"

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:
        for page_index, num_sub_pages in self._get_pages().items():
            for sub_page_index in range(num_sub_pages):
                url = f"https://www.ndr.de/public/teletext/{page_index}_{sub_page_index+1:02}.htm"
                response = self.get_html(url)
                if response.status_code == 200:
                    yield page_index, sub_page_index+1, response.text

    def _get_pages(self) -> Dict[int, int]:
        text = self.get_html("https://www.ndr.de/public/teletext/pages.js").text
        pages = dict()
        for match in re.findall(r"(\d+):(\d+)", text):
            pages[int(match[0])] = int(match[1])

        return pages
