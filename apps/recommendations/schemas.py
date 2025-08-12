from ninja import Schema

from apps.core.schemas import SongFeaturesSchema, SongSchema


class EmotionFeaturesSchema(Schema):
    valence: float
    arousal: float


class RecommendFromSpeechResponseSchema(Schema):
    song: SongSchema
    features: SongFeaturesSchema
    switch_probability: float
