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


class EmotionFeatures(BaseModel):
    valence: float
    arousal: float
    authenticity: float
    timeliness: float
    complexity: float
