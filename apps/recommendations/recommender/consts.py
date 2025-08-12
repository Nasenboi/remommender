from typing import Dict, Literal

from dotenv import load_dotenv

load_dotenv()

PLAYLIST_LENGTH = 16

GENRE_DATA_BASE = Literal[
    "rock",
    "pop",
    "alternative",
    "indie",
    "electronic",
    "dance",
    "alternative rock",
    "jazz",
    "metal",
    "chillout",
    "classic rock",
    "soul",
    "indie rock",
    "electronica",
    "folk",
    "chill",
    "instrumental",
    "punk",
    "blues",
    "hard rock",
    "ambient",
    "acoustic",
    "experimental",
    "Hip-Hop",
    "country",
    "easy listening",
    "funk",
    "electro",
    "heavy metal",
    "Progressive rock",
    "rnb",
    "indie pop",
    "House",
    "none",
]
