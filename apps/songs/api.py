import os
from typing import Optional

from django.conf import settings
from ninja import File, Form, Router
from ninja.errors import ValidationError
from ninja.files import UploadedFile
from ninja.pagination import paginate, PageNumberPagination
from uuid import UUID

from apps.core.models import Album, Song, SongFeatures, SongFile, SongGenres
from apps.core.schemas import SongCreateSchema, SongSchema

songs_router = Router(tags=["songs"])
albums_router = Router(tags=["albums"])

@albums_router.post("/")
def upload_album(
    request,
    artwork_file: UploadedFile = File(...),
    album_name: str = Form(...),
    artist: str = Form(...),
):
    if not artwork_file.name.endswith((".jpg", ".jpeg", ".png")):
        raise ValidationError("Unsupported file format. Please upload an image file.")

    # Check if the artwork_file already exists
    # will not return an error!
    # should do this in the future, maybe
    existing_artwork_file = Album.objects.filter(album=album_name, artist=artist).first()
    if existing_artwork_file:
        return {"id": existing_artwork_file.id}

    album = Album.objects.create(album=album_name, artwork=artwork_file, artist=artist)
    return {"id": album.id}

@songs_router.post("/")
def create_song(
    request,
    song: SongCreateSchema,
):
    audio_file = SongFile.objects.get(id=song.audio_file_id)

    if song.album_id:
        album = Album.objects.get(id=song.album_id)
    else:
        album = None

    song = Song.objects.create(
        **song.model_dump(exclude={"audio_file_id", "artwork_id", "features", "genres"}),
        features=SongFeatures.objects.create(**song.features.model_dump()),
        genres=SongGenres.objects.create(**song.genres.model_dump()),
        audio_file=audio_file,
        album=album,
    )

    return SongSchema.from_orm(song)

@songs_router.post("/files/")
def upload_song_file(
    request,
    audio_file: UploadedFile = File(...),
):
    if not audio_file.name.endswith((".mp3", ".wav")):
        raise ValidationError("Unsupported file format. Please upload an audio file.")

    # Could be weird if two different songs have the same file name
    # But this will never happen right? :D
    existing_songfile = SongFile.objects.filter(audio_file=audio_file.name).first()
    if existing_songfile:
        return {"id": existing_songfile.id}

    song_file = SongFile.objects.create(audio_file=audio_file)
    return {"id": song_file.id}



