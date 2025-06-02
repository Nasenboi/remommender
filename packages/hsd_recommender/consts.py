from typing import Literal

IP_MUSIC_SERVER = "http://127.0.0.1:8080/Audio/"
IP_ALBUM_ART_SERVER = "http://127.0.0.1:8080/Album_Art/"

MONGO_URL = "mongodb://host.docker.internal:27017"
MONGO_DB = "musemantiq"
MONGO_COLLECTION = "files"

PLAYLIST_LENGTH = 16

PLAYLIST_TYPES = Literal[
    "emotional",
    "essentia",
    "allFeatures",
]

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
