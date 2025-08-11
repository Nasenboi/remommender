from ninja import Schema

from packages.hsd_recommender.models import Song, SongFeatures

# for song schema maybe create a song return schema and rm: features, features_frames, songStructure, ids


class RecommendFromSpeechResponseSchema(Schema):
    song: Song
    features: SongFeatures
    switch_probability: float
