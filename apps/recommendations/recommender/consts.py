from typing import Dict, Literal

from dotenv import load_dotenv

load_dotenv()

PLAYLIST_LENGTH = 16

GENRE_DATA_BASE = Literal[
  "Rock",
  "Pop",
  "Alternative",
  "Indie",
  "Electronic",
  "Dance",
  "Alternative Rock",
  "Jazz",
  "Metal",
  "Chillout",
  "Classic Rock",
  "Soul",
  "Indie Rock",
  "Electronica",
  "Folk",
  "Chill",
  "Instrumental",
  "Punk",
  "Blues",
  "Hard Rock",
  "Ambient",
  "Acoustic",
  "Experimental",
  "Hip-Hop",
  "Country",
  "Easy Listening",
  "Funk",
  "Electro",
  "Heavy Metal",
  "Progressive Rock",
  "RnB",
  "Indie Pop",
  "House"
]
