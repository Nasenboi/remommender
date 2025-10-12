from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from ninja import Schema

from apps.core.schemas import SongSchema


class EmotionFeaturesSchema(Schema):
    valence: float
    arousal: float


class RecommendFromSpeechResponseSchema(Schema):
    song: SongSchema
    speech_features: EmotionFeaturesSchema
    switch_probability: float


class RecommendationStatisticsSchema(Schema):
    # general
    session_id: Union[UUID, str]
    timestamp: Union[str, datetime]
    switch_probability: float

    # Emotion Features
    valence: float
    arousal: float

    # Song Infos
    song_id: Optional[Union[UUID, str]] = None
    song_title: Optional[str] = None
    song_artist: Optional[str] = None
    song_duration_s: Optional[float] = None
    song_valence: Optional[float] = None
    song_arousal: Optional[float] = None
    song_authenticity: Optional[float] = None
    song_timeliness: Optional[float] = None
    song_complexity: Optional[float] = None
    song_danceability: Optional[float] = None
    song_tonal: Optional[float] = None
    song_voice: Optional[float] = None
    song_bpm: Optional[float] = None
    song_top_1_genre: Optional[str] = None
    song_top_2_genre: Optional[str] = None
    song_top_3_genre: Optional[str] = None
    song_url: Optional[str] = None

    # Album Infos
    album_id: Optional[Union[UUID, str]] = None
    album_name: Optional[str] = None
    album_artist: Optional[str] = None
    artwork_url: Optional[str] = None
