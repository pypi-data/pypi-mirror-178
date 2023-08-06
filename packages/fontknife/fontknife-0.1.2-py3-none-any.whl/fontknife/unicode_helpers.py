from typing import Tuple, List

from PIL import ImageFont, Image, ImageDraw


REGIONAL_A_CODE = 0x1F1E6
REGIONAL_Z_CODE = 0x1F1FF
REGIONAL_A = "🇦"
REGIONAL_Z = "🇿"

# build regex for this?
COUNTRY_CODES = frozenset((
    '🇦🇩', '🇦🇪', '🇦🇫', '🇦🇬', '🇦🇱', '🇦🇲', '🇦🇴', '🇦🇷', '🇦🇹', '🇦🇺', '🇦🇿',
    '🇧🇦', '🇧🇧', '🇧🇩', '🇧🇪', '🇧🇫', '🇧🇬', '🇧🇭', '🇧🇮', '🇧🇯', '🇧🇳', '🇧🇴',
    '🇧🇷', '🇧🇸', '🇧🇹', '🇧🇼', '🇧🇾', '🇧🇿', '🇨🇦', '🇨🇩', '🇨🇫', '🇨🇭', '🇨🇮',
    '🇨🇱', '🇨🇲', '🇨🇳', '🇨🇴', '🇨🇷', '🇨🇺', '🇨🇻', '🇨🇾', '🇨🇿', '🇩🇪', '🇩🇯',
    '🇩🇰', '🇩🇲', '🇩🇴', '🇩🇿', '🇪🇨', '🇪🇪', '🇪🇬', '🇪🇭', '🇪🇷', '🇪🇸', '🇪🇹',
    '🇫🇮', '🇫🇯', '🇫🇲', '🇫🇷', '🇬🇦', '🇬🇧', '🇬🇩', '🇬🇪', '🇬🇭', '🇬🇮', '🇬🇱',
    '🇬🇲', '🇬🇳', '🇬🇵', '🇬🇶', '🇬🇷', '🇬🇹', '🇬🇼', '🇬🇾', '🇭🇰', '🇭🇳', '🇭🇷',
    '🇭🇹', '🇭🇺', '🇮🇩', '🇮🇪', '🇮🇱', '🇮🇳', '🇮🇶', '🇮🇷', '🇮🇸', '🇮🇹', '🇯🇲',
    '🇯🇴', '🇯🇵', '🇰🇪', '🇰🇬', '🇰🇭', '🇰🇮', '🇰🇲', '🇰🇳', '🇰🇵', '🇰🇷', '🇰🇼',
    '🇰🇿', '🇱🇦', '🇱🇧', '🇱🇨', '🇱🇮', '🇱🇰', '🇱🇷', '🇱🇸', '🇱🇹', '🇱🇺', '🇱🇻',
    '🇱🇾', '🇲🇦', '🇲🇨', '🇲🇩', '🇲🇪', '🇲🇬', '🇲🇭', '🇲🇰', '🇲🇱', '🇲🇲', '🇲🇳',
    '🇲🇴', '🇲🇵', '🇲🇶', '🇲🇷', '🇲🇹', '🇲🇺', '🇲🇻', '🇲🇼', '🇲🇽', '🇲🇾', '🇲🇿',
    '🇳🇦', '🇳🇨', '🇳🇪', '🇳🇬', '🇳🇮', '🇳🇱', '🇳🇴', '🇳🇵', '🇳🇷', '🇳🇿', '🇴🇲',
    '🇵🇦', '🇵🇪', '🇵🇫', '🇵🇬', '🇵🇭', '🇵🇰', '🇵🇱', '🇵🇷', '🇵🇸', '🇵🇹', '🇵🇼',
    '🇵🇾', '🇶🇦', '🇷🇪', '🇷🇴', '🇷🇸', '🇷🇺', '🇷🇼', '🇸🇦', '🇸🇧', '🇸🇨', '🇸🇩',
    '🇸🇪', '🇸🇬', '🇸🇮', '🇸🇰', '🇸🇱', '🇸🇲', '🇸🇳', '🇸🇴', '🇸🇷', '🇸🇹', '🇸🇻',
    '🇸🇾', '🇸🇿', '🇹🇩', '🇹🇬', '🇹🇭', '🇹🇯', '🇹🇱', '🇹🇲', '🇹🇳', '🇹🇴', '🇹🇷',
    '🇹🇹', '🇹🇻', '🇹🇼', '🇹🇿', '🇺🇦', '🇺🇬', '🇺🇸', '🇺🇾', '🇺🇿', '🇻🇦', '🇻🇨',
    '🇻🇪', '🇻🇬', '🇻🇮', '🇻🇳', '🇻🇺', '🇼🇸', '🇾🇪', '🇿🇦', '🇿🇲', '🇿🇼',
))


def is_regional_indicator(s: str) -> bool:
    return REGIONAL_A <= s <= REGIONAL_Z


# todo: replace this with country code detection
def allowed_pair(a,b):
    return


def detect_possible_country_flags_in_line(s: str) -> List[str]:

    token_length = 0
    glyphs = []

    s_length = len(s)

    current_index = 0
    while current_index < s_length:
        current_char = s[current_index]
        if is_regional_indicator(current_char):
            next_index = current_index + 1
            if next_index < s_length:
                pair_of_chars = s[current_index:current_index+2]

                if next_index < s_length and pair_of_chars in COUNTRY_CODES:
                    glyphs.append(pair_of_chars)
                else:
                    glyphs.extend(pair_of_chars)

                current_index += 2
        else:
            glyphs.append(current_char)
            current_index += 1

    return glyphs


print(detect_possible_country_flags_in_line("e🇺🇸i🇦🇦i"))


def detect_regional_flags(s: str, start, end):
    pass

raw_font = ImageFont.truetype("/home/user/Downloads/Noto_Emoji/static/NotoEmoji-Regular.ttf", 16)

#raster_font =

text = "😊🎶🥺💀😒🤠😨👽🇺🇸♻🗑💡🌩⛈🌪🗿"
bbox = raw_font.getbbox(text)
image = Image.new("RGBA", bbox[:2], 0)
draw = ImageDraw.Draw(image)
#draw.text((0,0), text)
#image.show()