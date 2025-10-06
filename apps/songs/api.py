from typing import List
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import File, Form, Router
from ninja.errors import ValidationError
from ninja.files import UploadedFile
from ninja.pagination import PageNumberPagination, paginate

from apps.core.models import Album, Song, SongFeatures, SongGenres
from apps.core.schemas import AlbumSchema, SongCreateSchema, SongSchema

from .methods import calculate_genres_and_features
from .schemas import AlbumDetailSchema

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
    existing_artwork_file = Album.objects.filter(album_name=album_name, artist=artist).first()
    if existing_artwork_file:
        return {"id": existing_artwork_file.id}

    album = Album.objects.create(album_name=album_name, artwork_file=artwork_file, artist=artist)
    return {"id": album.id}


@albums_router.get("/", response=List[AlbumSchema])
@paginate(PageNumberPagination, page_size=10)
def list_albums(request, album_name: str = None):
    qs = Album.objects.all()
    if album_name:
        qs = qs.filter(album_name__icontains=album_name)
    qs = qs.order_by("album_name")
    return qs


@albums_router.get("/{album_id}", response=AlbumDetailSchema)
def get_album_details(request, album_id: UUID):
    album = Album.objects.filter(id=album_id).first()
    if not album:
        return 404, {"detail": "Album not found"}

    detail_album = AlbumDetailSchema.from_orm(album)
    detail_album.songs = Song.objects.filter(album=album)

    return detail_album


@albums_router.delete("/{album_id}")
def delete_album(request, album_id: UUID, delete_songs: bool = True):
    album = get_object_or_404(Album, id=album_id)
    album.delete()

    if delete_songs:
        songs = Song.objects.filter(album_id=album_id)
        songs.delete()

    return {"deleted": True}


@songs_router.post("/")
def create_and_upload_song(
    request,
    song: SongCreateSchema = Form(...),
    audio_file: UploadedFile = File(...),
):
    if song.album_id:
        album = Album.objects.get(id=song.album_id)
    else:
        album = None

    # calculate features if not present:
    if not song.features or not song.genres:
        # ToDo: Move to methods
        song.genres, song.features, song.duration_s = calculate_genres_and_features(audio_file)

    song = Song.objects.create(
        **song.model_dump(exclude={"audio_file_id", "artwork_id", "features", "genres"}),
        features=SongFeatures.objects.create(**song.features.model_dump()),
        genres=SongGenres.objects.create(**song.genres.model_dump()),
        audio_file=audio_file,
        album=album,
    )

    return SongSchema.from_orm(song)


@songs_router.get("/", response=List[SongSchema])
@paginate(PageNumberPagination, page_size=10)
def list_songs(request, title: str = None):
    qs = Song.objects.all()
    if title:
        qs = qs.filter(title__icontains=title)
    qs = qs.order_by("title")
    return qs


@songs_router.delete("/{song_id}")
def delete_song(request, song_id: UUID):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return {"deleted": True}
