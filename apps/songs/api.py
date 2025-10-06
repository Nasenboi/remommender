import os
import tempfile
from typing import List
from uuid import UUID

from django.shortcuts import get_object_or_404
from ninja import File, Form, Router
from ninja.errors import ValidationError
from ninja.files import UploadedFile
from ninja.pagination import PageNumberPagination, paginate

from apps.core.models import Album, Song, SongFeatures, SongGenres
from apps.core.schemas import AlbumSchema, SongCreateSchema, SongFeaturesSchema, SongGenresSchema, SongSchema

from .feature_extraction.song_info_extractor import SongInfoExtractor
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
    existing_artwork_file = Album.objects.filter(album=album_name, artist=artist).first()
    if existing_artwork_file:
        return {"id": existing_artwork_file.id}

    album = Album.objects.create(album=album_name, artwork_file=artwork_file, artist=artist)
    return {"id": album.id}


@albums_router.get("/", response=List[AlbumSchema])
@paginate(PageNumberPagination, page_size=10)
def list_albums(request):
    return Album.objects.all()


@albums_router.get("/all", response=List[AlbumSchema])
def list_all_albums(request):
    return Album.objects.all()


@albums_router.get("/{album_id}", response=AlbumDetailSchema)
def get_album_details(request, album_id: UUID):
    album = Album.objects.filter(id=album_id).first()
    if not album:
        return 404, {"detail": "Album not found"}

    detail_album = AlbumDetailSchema.from_orm(album)
    detail_album.songs = Song.objects.filter(album=album)

    return detail_album

@songs_router.delete("/{song_id}")
def delete_song(request, song_id: UUID):
    song = get_object_or_404(Song, id=song_id)
    song.delete()
    return {"deleted": True}

@songs_router.post("/")
def create_and_upload_song(
    request,
    song: SongCreateSchema = Form(...),
    audio_file: UploadedFile = File(...),
):
    print(song)

    if song.album_id:
        album = Album.objects.get(id=song.album_id)
    else:
        album = None

    # calculate features if not present:
    if not song.features or not song.genres:
        # ToDo: Move to methods
        with tempfile.NamedTemporaryFile(delete=True, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
            # Write uploaded file content to temporary file
            tmp_file.write(audio_file.file.read())
            tmp_path = tmp_file.name

            song_info_extractor = SongInfoExtractor(tmp_path)
            song.duration_s = song_info_extractor.get_duration()
            essentia_genre_features = song_info_extractor.extract_essentia_genre_features()
            print(essentia_genre_features)
            song.genres = SongGenresSchema(
                all_genres=essentia_genre_features["all_genres"], top3_genres=essentia_genre_features["top3_genres"]
            )

            gmbi_features_frames = song_info_extractor.extract_gmbi_features_frames()
            print(gmbi_features_frames)
            essentia_dl_features = song_info_extractor.extract_essentia_dl_features()
            print(essentia_dl_features)

            song.features = SongFeaturesSchema(
                valence=gmbi_features_frames["mean"]["valence"],
                arousal=gmbi_features_frames["mean"]["arousal"],
                authenticity=gmbi_features_frames["mean"]["authenticity"],
                timeliness=gmbi_features_frames["mean"]["timeliness"],
                complexity=gmbi_features_frames["mean"]["complexity"],
                danceability=essentia_dl_features["mean"]["danceability"],
                tonal=essentia_dl_features["mean"]["tonal"],
                voice=essentia_dl_features["mean"]["voice"],
                bpm=essentia_dl_features["mean"]["bpm"],
            )

    song = Song.objects.create(
        **song.model_dump(exclude={"audio_file_id", "artwork_id", "features", "genres"}),
        features=SongFeatures.objects.create(**song.features.model_dump()),
        genres=SongGenres.objects.create(**song.genres.model_dump()),
        audio_file=audio_file,
        album=album,
    )

    return SongSchema.from_orm(song)
