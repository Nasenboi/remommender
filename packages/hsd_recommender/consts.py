from typing import Literal, Dict
import os
from dotenv import load_dotenv

load_dotenv()

MUSIC_SERVER_URL = os.getenv("MUSIC_SERVER_URL")
ALBUM_ART_SERVER_URL = os.getenv("ALBUM_ART_SERVER_URL")

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = "musemantiq"
MONGO_COLLECTION = "files"

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

GENRE_CORR = Literal[
    "rock",
    "alternative rock",
    "alternative",
    "hard rock",
    "indie rock",
    "classic rock",
    "punk",
    "Progressive rock",
    "indie",
    "heavy metal",
    "indie pop",
    "metal",
    "blues",
    "country",
    "acoustic",
    "folk",
    "pop",
    "funk",
    "experimental",
    "instrumental",
    "soul",
    "Hip-Hop",
    "easy listening",
    "House",
    "rnb",
    "electro",
    "dance",
    "ambient",
    "jazz",
    "chillout",
    "electronic",
    "electronica",
    "chill",
]


SONG_FEATURES_SEARCH: Dict[str, bool] = {
    "features.valence": 1,
    "features.arousal": 1,
}
