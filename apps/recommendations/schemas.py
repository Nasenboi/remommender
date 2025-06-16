from ninja import ModelSchema, Schema
from typing import Literal, List, Optional
from pydantic import BaseModel


# for song schema maybe create a song return schema and rm: features, features_frames, songStructure, ids
class SongSchema(BaseModel):
    title: str
    album: str
    artist: str
    duration_s: int
    features: dict
    features_frames: dict
    songStructure: dict
    ids: dict
    url: Optional[str] = None


PlaylistSchema = List[SongSchema]


class EmotionFeaturesSchema(BaseModel):
    valence: float
    arousal: float
    authenticity: float
    timeliness: float
    complexity: float


class RecommendFromSpeechResponseSchema(Schema):
    song: SongSchema
    emotion_features: EmotionFeaturesSchema
