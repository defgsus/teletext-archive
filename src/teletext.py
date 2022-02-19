import io
import json
from typing import List, Optional, TextIO, Tuple

from .console import ConsoleColors


class Colors:
    """
    mapping of color name to one-character code


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
    Single page representation.

    Colors:
        https://en.wikipedia.org/wiki/Videotex_character_set#C1_control_codes

    G1 and G3 to unicode mapping:
        https://en.wikipedia.org/wiki/Teletext_character_set#Graphics_character_sets
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

    G1_TO_UNICODE_MAPPING = {
        0x20: 0x20,
        0x21: 0x1fb00,
        0x22: 0x1fb01,
        0x23: 0x1fb02,
        0x24: 0x1fb03,
        0x25: 0x1fb04,
        0x26: 0x1fb05,
        0x27: 0x1fb06,
        0x28: 0x1fb07,
        0x29: 0x1fb08,
        0x2a: 0x1fb09,
        0x2b: 0x1fb0a,
        0x2c: 0x1fb0b,
        0x2d: 0x1fb0c,
        0x2e: 0x1fb0d,
        0x2f: 0x1fb0e,
        0x30: 0x1fb0f,
        0x31: 0x1fb10,
        0x32: 0x1fb11,
        0x33: 0x1fb12,
        0x34: 0x1fb13,
        0x35: 0x258c,
        0x36: 0x1fb14,
        0x37: 0x1fb15,
        0x38: 0x1fb16,
        0x39: 0x1fb17,
        0x3a: 0x1fb18,
        0x3b: 0x1fb19,
        0x3c: 0x1fb1a,
        0x3d: 0x1fb1b,
        0x3e: 0x1fb1c,
        0x3f: 0x1fb1d,
        0x60: 0x1fb1e,
        0x61: 0x1fb1f,
        0x62: 0x1fb20,
        0x63: 0x1fb21,
        0x64: 0x1fb22,
        0x65: 0x1fb23,
        0x66: 0x1fb24,
        0x67: 0x1fb25,
        0x68: 0x1fb26,
        0x69: 0x1fb27,
        0x6a: 0x2590,
        0x6b: 0x1fb28,
        0x6c: 0x1fb29,
        0x6d: 0x1fb2a,
        0x6e: 0x1fb2b,
        0x6f: 0x1fb2c,
        0x70: 0x1fb2d,
        0x71: 0x1fb2e,
        0x72: 0x1fb2f,
        0x73: 0x1fb30,
        0x74: 0x1fb31,
        0x75: 0x1fb32,
        0x76: 0x1fb33,
        0x77: 0x1fb34,
        0x78: 0x1fb35,
        0x79: 0x1fb36,
        0x7a: 0x1fb37,
        0x7b: 0x1fb38,
        0x7c: 0x1fb39,
        0x7d: 0x1fb3a,
        0x7e: 0x1fb3b,
        0x7f: 0x2588,
    }

    G3_TO_UNICODE_MAPPING = {
        0x20: 0x1fb3c,
        0x21: 0x1fb3d,
        0x22: 0x1fb3e,
        0x23: 0x1fb3f,
        0x24: 0x1fb40,
        0x25: 0x25e3,
        0x26: 0x1fb41,
        0x27: 0x1fb42,
        0x28: 0x1fb43,
        0x29: 0x1fb44,
        0x2a: 0x1fb45,
        0x2b: 0x1fb46,
        0x2c: 0x1fb68,
        0x2d: 0x1fb69,
        0x2e: 0x1fb70,
        0x2f: 0x2592,
        0x30: 0x1fb47,
        0x31: 0x1fb48,
        0x32: 0x1fb49,
        0x33: 0x1fb4a,
        0x34: 0x1fb4b,
        0x35: 0x25e2,
        0x36: 0x1fb4c,
        0x37: 0x1fb4d,
        0x38: 0x1fb4e,
        0x39: 0x1fb4f,
        0x3a: 0x1fb50,
        0x3b: 0x1fb51,
        0x3c: 0x1fb6a,
        0x3d: 0x1fb6b,
        0x3e: 0x1fb75,
        0x3f: 0x2588,
        0x40: 0x2537,
        0x41: 0x252f,
        0x42: 0x251d,
        0x43: 0x2525,
        0x44: 0x1fba4,
        0x45: 0x1fba5,
        0x46: 0x1fba6,
        0x47: 0x1fba7,
        0x48: 0x1fba0,
        0x49: 0x1fba1,
        0x4a: 0x1fba2,
        0x4b: 0x1fba3,
        0x4c: 0x253f,
        0x4d: 0x2022,
        0x4e: 0x25cf,
        0x4f: 0x25cb,
        0x50: 0x2502,
        0x51: 0x2500,
        0x52: 0x250c,
        0x53: 0x2510,
        0x54: 0x2514,
        0x55: 0x2518,
        0x56: 0x251c,
        0x57: 0x2524,
        0x58: 0x252c,
        0x59: 0x2534,
        0x5a: 0x253c,
        0x5b: 0x2b62,
        0x5c: 0x2b60,
        0x5d: 0x2b61,
        0x5e: 0x2b63,
        0x5f: 0x20,
        0x60: 0x1fb52,
        0x61: 0x1fb53,
        0x62: 0x1fb54,
        0x63: 0x1fb55,
        0x64: 0x1fb56,
        0x65: 0x25e5,
        0x66: 0x1fb57,
        0x67: 0x1fb58,
        0x68: 0x1fb59,
        0x69: 0x1fb5a,
        0x6a: 0x1fb5b,
        0x6b: 0x1fb5c,
        0x6c: 0x1fb6c,
        0x6d: 0x1fb6d,
        0x70: 0x1fb5d,
        0x71: 0x1fb5e,
        0x72: 0x1fb5f,
        0x73: 0x1fb60,
        0x74: 0x1fb61,
        0x75: 0x25e4,
        0x76: 0x1fb62,
        0x77: 0x1fb63,
        0x78: 0x1fb64,
        0x79: 0x1fb65,
        0x7a: 0x1fb66,
        0x7b: 0x1fb67,
        0x7c: 0x1fb6e,
        0x7d: 0x1fb6f,
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
                    Teletext.COLOR_CONSOLE_MAPPING[self.color or "w"],
                    Teletext.COLOR_CONSOLE_MAPPING[self.bg_color or "b"]
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
            print(json.dumps(json_line, ensure_ascii=False, separators=(',', ':')), file=file)

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

    @classmethod
    def from_matrix(cls, matrix: List[List[Tuple[str, str]]]) -> "Teletext":
        tt = cls()
        for row in matrix:
            tt.new_line()
            prev_color = None
            block = cls.Block("")
            for char, color in row:
                if color != prev_color:
                    if block.text:
                        tt.add_block(block)
                        block = cls.Block("")
                    block.color, block.bg_color = color
                    prev_color = color
                block.text += char

            if block.text:
                tt.add_block(block)

        return tt

    @classmethod
    def g1_to_unicode(cls, code: int) -> int:
        return cls.G1_TO_UNICODE_MAPPING.get(code, "?")

    @classmethod
    def g3_to_unicode(cls, code: int) -> int:
        return cls.G3_TO_UNICODE_MAPPING.get(code, "?")
