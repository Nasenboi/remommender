from typing import Dict, List, Optional
from uuid import UUID

from ninja import Schema


class SongFeaturesSchema(Schema):
    valence: Optional[float] = None
    arousal: Optional[float] = None
    authenticity: Optional[float] = None
    timeliness: Optional[float] = None
    complexity: Optional[float] = None
    danceability: Optional[float] = None
    tonal: Optional[float] = None
    voice: Optional[float] = None
    bpm: Optional[float] = None


class SongGenresSchema(Schema):
    top3_genres: Dict[str, float] = {}
    all_genres: Dict[str, float] = {}


class SongSchema(Schema):
    id: UUID
    title: str
    album: Optional[str] = None
    artist: str
    duration_s: float
    features: SongFeaturesSchema
    genres: SongGenresSchema
    song_url: Optional[str]
    artwork_url: Optional[str]


Playlist = List[SongSchema]


class SongCreateSchema(Schema):
    title: str
    album_id: Optional[UUID] = None
    audio_file_id: Optional[UUID]
    artist: str
    duration_s: float
    features: SongFeaturesSchema
    genres: SongGenresSchema
