import re
import json
from typing import Dict, Generator, Tuple, Union

from ..scraper import Scraper


class ZDFBase(Scraper):

    ABSTRACT = True

    ZDF_MANDANT = None

    def iter_pages(self) -> Generator[Tuple[int, int, Union[str, bool]], None, None]:
        status_filename = self.path() / "status.json"
        if status_filename.exists():
            status = json.loads(status_filename.read_text())
        else:
            status = dict()

        for page_index in range(100, 900):

            url = f"https://teletext.zdf.de/php/options.php?mandant={self.ZDF_MANDANT}&site={page_index}"
            response = self.get_html(url)
            num_sub_pages, date = response.text.split(",")
            num_sub_pages = int(num_sub_pages) + 1

            page_status = {"date": date, "sub_pages": num_sub_pages}

            # simply keep the files that don't have changed (according to published timestamp)
            if status.get(str(page_index)) == page_status:
                for sub_page_index in range(num_sub_pages):
                    yield page_index, sub_page_index + 1, True
                continue
                
            status[str(page_index)] = page_status

            # empty page
            if date == "-1":
                continue

            for sub_page_index in range(num_sub_pages):
                page_name = f"{page_index}"
                if sub_page_index:
                    page_name = f"{page_name}_{sub_page_index}"

                url = f"https://teletext.zdf.de/teletext/{self.ZDF_MANDANT}/seiten/klassisch/{page_name}.html"
                response = self.get_html(url)

                if response.status_code == 200:
                    yield page_index, sub_page_index + 1, response.text

        self.log("writing", status_filename)
        status_filename.write_text(json.dumps(status, indent=2))


class ZDF(ZDFBase):
    ABSTRACT = False
    NAME = "zdf"
    ZDF_MANDANT = "zdf"
