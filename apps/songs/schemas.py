from typing import Optional

from apps.core.schemas import AlbumSchema, SongSchema


class AlbumDetailSchema(AlbumSchema):
    songs: Optional[list[SongSchema]] = None


class AlbumUpdateSchema(AlbumSchema):
    album_name: Optional[str] = None
    artist: Optional[str] = None


class SongUpdateSchema(SongSchema):
    title: Optional[str] = None
    artist: Optional[str] = None
