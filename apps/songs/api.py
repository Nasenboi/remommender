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
from .schemas import AlbumDetailSchema, AlbumUpdateSchema, SongUpdateSchema

songs_router = Router(tags=["songs"])
albums_router = Router(tags=["albums"])


@albums_router.post("/", response=AlbumSchema)
def upload_album(
    request,
    artwork_file: UploadedFile = File(...),
    album_name: str = Form(...),
    artist: str = Form(...),
):
    if not artwork_file.name.endswith((".jpg", ".jpeg", ".png")):
        raise ValidationError("Unsupported file format. Please upload an image file.")

    # Check if the album already exists
    # will not return an error!
    # should do this in the future, maybe
    existing_album = Album.objects.filter(album_name=album_name, artist=artist).first()
    if existing_album:
        return {"id": existing_album.id}

    album = Album.objects.create(album_name=album_name, artwork_file=artwork_file, artist=artist)
    return AlbumSchema.from_orm(album)


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


@albums_router.put("/{album_id}/", response=AlbumSchema)
def update_album(request, album_id: UUID, album_data: AlbumUpdateSchema):
    album = get_object_or_404(Album, id=album_id)

    update_data = album_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(album, field, value)

    album.save()
    return AlbumSchema.from_orm(album)


@albums_router.post("/{album_id}/artwork", response=AlbumSchema)
def update_album_artwork(request, album_id: UUID, artwork_file: UploadedFile = File(...)):
    album = get_object_or_404(Album, id=album_id)

    if not artwork_file.name.endswith((".jpg", ".jpeg", ".png")):
        raise ValidationError("Unsupported file format. Please upload an image file.")

    album.artwork_file = artwork_file
    album.save()
    return AlbumSchema.from_orm(album)


@albums_router.delete("/{album_id}")
def delete_album(request, album_id: UUID, delete_songs: bool = True):
    album = get_object_or_404(Album, id=album_id)
    album.delete()

    if delete_songs:
        songs = Song.objects.filter(album_id=album_id)
        songs.delete()

    return {"deleted": True}


@songs_router.post("/", response=SongSchema)
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


@songs_router.put("/{song_id}/", response=SongSchema)
def update_song(request, song_id: UUID, song_data: SongUpdateSchema):
    song = get_object_or_404(Song, id=song_id)

    update_data = song_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(song, field, value)

    song.save()
    return SongSchema.from_orm(song)


@songs_router.delete("/{song_id}")
def delete_song(request, song_id: UUID):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return {"deleted": True}
