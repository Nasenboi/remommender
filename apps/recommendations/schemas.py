from ninja import ModelSchema, Schema
from typing import Literal, List
from pydantic import BaseModel

# Details
EMOTION_RETRIVAL_TYPES = Literal["speech", "text"]

# Model Schemas


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


PlaylistSchema = List[SongSchema]


class EmotionFeaturesSchema(BaseModel):
    valence: float
    arousal: float
    authenticity: float
    timeliness: float
    complexity: float


# Router Schemas
class RecommendFromSpeechQuerySchema(Schema):
    speech_to_emotion: bool = False
    text_to_emotion: bool = False


class RecommendFromSpeechResponseSchema(Schema):
    song: SongSchema
    emotion_features: EmotionFeaturesSchema
