from typing import Optional
from apps.core.schemas import SongSchema, AlbumSchema

class AlbumDetailSchema(AlbumSchema):
    songs: Optional[list[SongSchema]] = None
