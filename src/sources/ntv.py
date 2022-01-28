import json
from typing import Dict, Generator, Tuple, Union, Optional

from ..scraper import Scraper


class NTV(Scraper):

    NAME = "ntv"
    FILE_EXTENSION = "json"

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:
        url = f"https://teletext.n-tv.de/teletext-api/100/0"

        page_index = 0
        while page_index < 900:
            data = self.get_html(url).json()

            new_page_index = int(data["content"]["page"][:3])
            if new_page_index <= page_index:
                break
            page_index = new_page_index

            yield self._to_yield_page(page_index, 1, data)

            for sub_page_index in data["subpages"]["subpage"][1:]:
                sub_page_index = int(sub_page_index)
                url = f"https://teletext.n-tv.de/teletext-api/{page_index}/{sub_page_index}"
                sub_data = self.get_html(url).json()

                yield self._to_yield_page(page_index, sub_page_index, sub_data)

            # get next page
            url = f"https://teletext.n-tv.de/teletext-api/ascend/{page_index}"

    def _to_yield_page(self, page_index: int, sub_page_index: int, data: json) -> Tuple[int, int, Union[str, bool]]:
        if self._is_page_different(page_index, sub_page_index, data):
            content = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            content = True
        return page_index, sub_page_index, content

    def _is_page_different(self, page_index: int, sub_page_index: int, new_data: json) -> bool:
        filename = self.to_filename(page_index, sub_page_index)
        if not filename.exists():
            return True

        old_data = json.loads(filename.read_text())

        # see if something else than the date has changed
        old_data["date"] = new_data["date"]
        old_data["content"]["date"] = new_data["content"]["date"]

        return old_data != new_data
