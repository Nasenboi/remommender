from typing import Optional

from apps.core.schemas import AlbumSchema, SongSchema


class AlbumDetailSchema(AlbumSchema):
    songs: Optional[list[SongSchema]] = None
