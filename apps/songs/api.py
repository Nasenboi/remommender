import os
from typing import Optional

from django.conf import settings
from ninja import File, Form, Router
from ninja.errors import ValidationError
from ninja.files import UploadedFile

from apps.core.models import ArtworkFile, Song, SongFeatures, SongFile, SongGenres
from apps.core.schemas import SongCreateSchema, SongSchema

router = Router(tags=["songs"])


@router.post("/song-file/")
def upload_song_file(
    request,
    use_existing_file: Optional[bool] = Form(True),
    audio_file: UploadedFile = File(...),
):
    if not audio_file.name.endswith((".mp3", ".wav")):
        raise ValidationError("Unsupported file format. Please upload an audio file.")

    # Could be weird if two different songs have the same file name
    # But this will never happen right? :D
    existing_songfile = SongFile.objects.filter(audio_file=audio_file.name).first()
    if existing_songfile:
        return {"id": existing_songfile.id}

    # Create model instance without re-saving the file
    file_path = os.path.join(settings.MEDIA_ROOT, "Audio", audio_file.name)
    if use_existing_file and os.path.exists(file_path):
        song_file = SongFile()
        song_file.audio_file = file_path
        song_file.full_clean()
        song_file.save()
        return {"id": song_file.id}

    song_file = SongFile.objects.create(audio_file=audio_file)
    return {"id": song_file.id}


@router.post("/artwork-file/")
def upload_artwork_file(
    request,
    use_existing_file: Optional[bool] = Form(True),
    artwork: UploadedFile = File(...),
    album: str = Form(...),
    artist: str = Form(...),
):
    if not artwork.name.endswith((".jpg", ".jpeg", ".png")):
        raise ValidationError("Unsupported file format. Please upload an audio file.")

    # Check if the artwork already exists
    # will not return an error!
    # should do this in the future, maybe
    existing_artwork = ArtworkFile.objects.filter(album=album, artist=artist).first()
    if existing_artwork:
        return {"id": existing_artwork.id}

    # Create model instance without re-saving the file
    file_path = os.path.join(settings.MEDIA_ROOT, "Album_Art", artwork.name)
    if use_existing_file and os.path.exists(file_path):
        artwork_file = ArtworkFile(album=album, artist=artist)
        artwork_file.artwork = file_path
        artwork_file.full_clean()
        artwork_file.save()
        return {"id": artwork_file.id}

    artwork_file = ArtworkFile.objects.create(album=album, artwork=artwork)
    return {"id": artwork_file.id}


@router.post("/")
def create_song(
    request,
    song: SongCreateSchema,
):
    audio_file = SongFile.objects.get(id=song.audio_file_id)

    if song.artwork_id:
        artwork = ArtworkFile.objects.get(id=song.artwork_id)
    else:
        artwork = None

    song = Song.objects.create(
        **song.model_dump(
            exclude={"audio_file_id", "artwork_id", "features", "genres"}
        ),
        features=SongFeatures.objects.create(**song.features.model_dump()),
        genres=SongGenres.objects.create(**song.genres.model_dump()),
        audio_file=audio_file,
        artwork=artwork,
    )

    return SongSchema.from_orm(song)
