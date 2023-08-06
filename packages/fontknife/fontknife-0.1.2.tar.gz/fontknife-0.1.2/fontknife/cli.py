from enum import Enum, auto

from fontknife.utils import generate_glyph_sequence

# This is probably ok
class PresetEnum(Enum):
    DEFAULT = tuple(generate_glyph_sequence())
    HEX_ONLY = tuple(hex(i)[2:].upper() for i in range(16))
    ALL_IN_FONT = auto()

#don't do enums for the class types though?
# use formatter classes?

def print_members(e: Enum):
    for member in PresetEnum:
        print(member.name)


