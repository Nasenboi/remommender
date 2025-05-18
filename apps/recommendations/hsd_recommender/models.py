"""
Note to future self:
I removed the genre field from all feature models
Originally this field was there for an easier FastAPI implementation
But this is not our use case :)
"""

from pydantic import BaseModel
from typing import List


class Song(BaseModel):
    title: str
    album: str
    artist: str
    duration_s: int
    features: dict
    features_frames: dict
    songStructure: dict
    ids: dict


Playlist = List[Song]


class AllFeatures(BaseModel):
    valence: float
    arousal: float
    authenticity: float
    timeliness: float
    complexity: float
    danceable: float
    tonal: float
    voice: float


class EmotionFeatures(BaseModel):
    valence: float
    arousal: float
    authenticity: float
    timeliness: float
    complexity: float


class EssentiaFeatures(BaseModel):
    danceable: float
    tonal: float
    voice: float
    female: float
    bpm: float
