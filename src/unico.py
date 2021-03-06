"""
Unicode (and teletext) related stuff
"""

_G0 = r""" !"#$%&'()*+,-./
0123456789:;<=>?
@ABCDEFGHIJKLMNO
PQRSTUVWXYZ[\]^_
`abcdefghijklmno
pqrstuvwxyz{:}~■""".replace("\n", "")

G0_TO_UNICODE_MAPPING = {
    i + 0x20: ord(char)
    for i, char in enumerate(_G0)
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
