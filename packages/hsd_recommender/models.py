"""
Note to future self:
I removed the genre field from all feature models
Originally this field was there for an easier FastAPI implementation
But this is not our use case :)
"""

from pydantic import BaseModel
from typing import List, Optional


class Song(BaseModel):
    title: str
    album: str
    artist: str
    duration_s: float
    features: dict
    features_frames: dict
    songStructure: dict
    ids: dict
    url: Optional[str] = None


Playlist = List[Song]


class SongFeatures(BaseModel):
    valence: Optional[float] = None
    arousal: Optional[float] = None
    authenticity: Optional[float] = None
    timeliness: Optional[float] = None
    complexity: Optional[float] = None
    danceable: Optional[float] = None
    tonal: Optional[float] = None
    voice: Optional[float] = None
