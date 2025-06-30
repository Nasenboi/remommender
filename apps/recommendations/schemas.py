from ninja import ModelSchema, Schema
from pydantic import BaseModel

from packages.hsd_recommender.models import Song, EmotionFeatures

# for song schema maybe create a song return schema and rm: features, features_frames, songStructure, ids


class RecommendFromSpeechResponseSchema(Schema):
    song: Song
    emotion_features: EmotionFeatures
