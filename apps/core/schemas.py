from typing import Annotated, Dict, List, Optional, TypeVar, Union
from uuid import UUID

from ninja import Schema
from pydantic import WrapValidator
from pydantic_core import PydanticUseDefault


def _empty_str_to_default(v, handler, info):
    if isinstance(v, str) and v == "":
        raise PydanticUseDefault
    return handler(v)


T = TypeVar("T")
EmptyStrToDefault = Annotated[T, WrapValidator(_empty_str_to_default)]


class AlbumSchema(Schema):
    id: UUID
    album_name: str
    artist: str
    artwork_url: str


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
    album: Optional[AlbumSchema] = None
    artist: str
    duration_s: float
    features: SongFeaturesSchema
    genres: SongGenresSchema
    song_url: Optional[str]
    artwork_url: Optional[str]


Playlist = List[SongSchema]


class SongCreateSchema(Schema):
    title: str
    album_id: Optional[Union[UUID, str]] = None
    artist: str
    duration_s: Optional[float] = None
    features: Optional[EmptyStrToDefault[SongFeaturesSchema]] = None
    genres: Optional[EmptyStrToDefault[SongGenresSchema]] = None
