import io
import json
from typing import List, Optional, TextIO

from .console import ConsoleColors

class Colors:
    """
    mapping of color name to one-character code

    https://en.wikipedia.org/wiki/Videotex_character_set#C1_control_codes
    """
    BLACK = "b"
    RED = "r"
    GREEN = "g"
    YELLOW = "y"
    BLUE = "l"
    MAGENTA = "m"
    CYAN = "c"
    WHITE = "w"


class Teletext:
    """
    Single page representation
    """
    
    COLOR_CONSOLE_MAPPING = {
        "b": ConsoleColors.BLACK,
        "r": ConsoleColors.RED,
        "g": ConsoleColors.GREEN,
        "y": ConsoleColors.YELLOW,
        "l": ConsoleColors.BLUE,
        "m": ConsoleColors.PURPLE,
        "c": ConsoleColors.CYAN,
        "w": ConsoleColors.WHITE,
    }

    class Block:
        def __init__(
                self,
                text: str,
                color: Optional[str] = None,
                bg_color: Optional[str] = None,
        ):
            assert color is None or color in Teletext.COLOR_CONSOLE_MAPPING, color
            assert bg_color is None or bg_color in Teletext.COLOR_CONSOLE_MAPPING, bg_color
            self.text = text
            self.color = color
            self.bg_color = bg_color

        def to_json(self) -> list:
            return [
                "".join((self.color or "_", self.bg_color or "_")),
                self.text
            ]

        def to_ansi(self, colors: bool = True) -> str:
            block_str = self.text

            if colors:
                block_str = ConsoleColors.escape(
                    Teletext.COLOR_CONSOLE_MAPPING[self.color],
                    Teletext.COLOR_CONSOLE_MAPPING[self.bg_color]
                ) + block_str + ConsoleColors.escape()

            return block_str

    def __init__(self):
        self.lines = []

    def new_line(self):
        self.lines.append([])

    def add_block(self, block: Block):
        self.lines[-1].append(block)

    def to_ndjson(self, file: Optional[TextIO] = None) -> Optional[str]:
        if file is None:
            file = io.StringIO()
            self.to_ndjson(file)
            file.seek(0)
            return file.read()

        for line in self.lines:
            json_line = [b.to_json() for b in line]
            print(json.dumps(json_line, ensure_ascii=False), file=file)

    def to_ansi(self, file: Optional[TextIO] = None, colors: bool = True) -> Optional[str]:
        if file is None:
            file = io.StringIO()
            self.to_ansi(file, colors=colors)
            file.seek(0)
            return file.read()

        for line in self.lines:

            for block in line:
                block_str = block.to_ansi(colors=colors)
                print(block_str, end="", file=file)

            print(file=file)
