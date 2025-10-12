import json
import os
import tempfile
from typing import Tuple

from django.core.files import File
from ninja.files import UploadedFile

from apps.core.models import Album, Song, SongFeatures, SongGenres
from apps.core.schemas import SongFeaturesSchema, SongGenresSchema

from .feature_extraction.song_info_extractor import SongInfoExtractor


def read_json(name: str) -> dict:
    path = os.path.join(os.getenv("PRE_CALC_JSON_PATH"), name)
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def convert_song_to_db_format(song: dict) -> Tuple[dict, dict]:
    db_song = {
        "title": song["title"],
        "artist": song["artist"],
        "duration_s": song["duration_s"],
        "features": {
            "valence": song["features"]["valence"],
            "arousal": song["features"]["arousal"],
            "authenticity": song["features"]["authenticity"],
            "timeliness": song["features"]["timeliness"],
            "complexity": song["features"]["complexity"],
            "danceability": song["features"]["danceability"],
            "tonal": song["features"]["tonal"],
            "voice": song["features"]["voice"],
            "bpm": song["features"]["bpm"],
        },
        "genres": song["features"]["genres"],
    }
    db_album = {
        "album_name": song["album"],
        "artist": song["artist"],
    }
    return db_song, db_album


def add_album_to_db(name: str, album_name: str = None, artist: str = None) -> str:
    """
    Adds an album artwork_file to the db if it does not exist yet.
    Returns the id of the object.
    """
    path = os.path.join(os.getenv("PRE_CALC_ALBUM_ART_PATH"), name)
    artwork_file = Album.objects.filter(album_name=album_name, artist=artist).first()
    if not artwork_file:
        with open(path, "rb") as f:
            artwork_file = Album.objects.create(artwork_file=File(f, name=name), album_name=album_name, artist=artist)
    return artwork_file.id


def add_json_to_db(name: str) -> str:
    """
    Adds a song to the db by a given json file
    Also adds the album cover and song if not already in db
    Returns the id of the song
    """
    try:
        raw_data = read_json(name)
    except json.decoder.JSONDecodeError as e:
        print(f"Could not decode json: {e}")
        return None

    db_song, db_album = convert_song_to_db_format(raw_data)

    # check if song already exists in db:
    existing_song = Song.objects.filter(title=db_song["title"], artist=db_song["artist"]).first()
    if existing_song:
        # print(f"Existing {existing_song.title} from {existing_song.artist} found in db!")
        return existing_song.id
    try:
        album_id = add_album_to_db(raw_data["ids"]["artwork_id"], db_album["album_name"], db_album["artist"])
        album = Album.objects.get(id=album_id)

        song_path = os.path.join(os.getenv("PRE_CALC_AUDIO_PATH"), raw_data["ids"]["track_id"])
        with open(song_path, "rb") as f:
            audio_file = File(f, name=raw_data["ids"]["track_id"])
            keys_to_exclude = ["audio_file_id", "artwork_id", "features", "genres"]
            song = Song.objects.create(
                **{k: v for k, v in db_song.items() if k not in keys_to_exclude},
                features=SongFeatures.objects.create(**db_song["features"]),
                genres=SongGenres.objects.create(**db_song["genres"]),
                audio_file=audio_file,
                album=album,
            )
            print(f"Added {song.title} from {song.artist} to db!")
            return song.id

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None


def check_and_add_pre_calculated_songs_to_db() -> None:
    if (
        not os.getenv("PRE_CALC_JSON_PATH")
        or not os.getenv("PRE_CALC_AUDIO_PATH")
        or not os.getenv("PRE_CALC_ALBUM_ART_PATH")
    ):
        return

    # check if files exist
    try:
        json_files = [f for f in os.listdir(os.getenv("PRE_CALC_JSON_PATH")) if f.endswith(".json")]
    except FileNotFoundError as e:
        print(f"Json Files not found: {e}")
        return

    for json_file in json_files:
        add_json_to_db(json_file)


def calculate_genres_and_features(audio_file: UploadedFile) -> Tuple[SongGenresSchema, SongFeaturesSchema, float]:
    with tempfile.NamedTemporaryFile(delete=True, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
        # Write uploaded file content to temporary file
        tmp_file.write(audio_file.file.read())
        tmp_path = tmp_file.name

        song_info_extractor = SongInfoExtractor(tmp_path)
        duration_s = song_info_extractor.get_duration()

        essentia_genre_features = song_info_extractor.extract_essentia_genre_features()

        genres = SongGenresSchema(
            all_genres=essentia_genre_features["all_genres"], top3_genres=essentia_genre_features["top3_genres"]
        )

        gmbi_features_frames = song_info_extractor.extract_gmbi_features_frames()

        essentia_dl_features = song_info_extractor.extract_essentia_dl_features()

        features = SongFeaturesSchema(
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

    return genres, features, duration_s


def add_song(title: str, artist: str, audio_file_path: str, album: Album = None) -> Song:
    """
    Adds a song to the db if it does not exist yet.
    Returns the song object.
    """
    try:
        existing_song = Song.objects.filter(title=title, artist=artist).first()
        if existing_song:
            print(f"Existing {existing_song.title} from {existing_song.artist} found in db!")
            return existing_song

        with open(audio_file_path, "rb") as f:
            audio_file = File(f, name=os.path.basename(audio_file_path))
            genres, features, duration_s = calculate_genres_and_features(audio_file)

            song = Song.objects.create(
                title=title,
                artist=artist,
                duration_s=duration_s,
                features=SongFeatures.objects.create(**features.dict()),
                genres=SongGenres.objects.create(**genres.dict()),
                audio_file=audio_file,
                album=album,
            )
            print(f"Added {song.title} from {song.artist} to db!")
            return song
    except Exception as e:
        print(f"Error adding song {title} from {artist}: {e}")
        return None


def add_albums_and_songs() -> None:
    """
    Adds songs from a folder, if there are subfolders, they are used as albums.
    """

    new_songs_path = os.getenv("NEW_SONGS_PATH")

    folders = os.listdir(new_songs_path)

    for folder in folders:
        try:
            folder_path = os.path.join(new_songs_path, folder)
            if os.path.isdir(folder_path):
                album_name = folder
                album_art_path = os.path.join(folder_path, "album_art.jpg")
                artist = "Unknown Artist"

                # First add album if it does not exist yet
                album = Album.objects.filter(album_name=album_name).first()

                if not album:
                    if os.path.exists(album_art_path):
                        with open(album_art_path, "rb") as f:
                            album = Album.objects.create(
                                artwork_file=File(f, name=f"{album_name}_art.jpg"),
                                album_name=album_name,
                                artist=artist,
                            )
                    else:
                        album = Album.objects.create(album_name=album_name, artist=artist)

                # Now add songs in this folder
                for file in os.listdir(folder_path):
                    if file.lower().endswith((".mp3")):
                        add_song(
                            title=os.path.splitext(file)[0],
                            artist=artist,
                            audio_file_path=os.path.join(folder_path, file),
                            album=album,
                        )
            print(f"Finished processing folder: {folder_path}")
        except Exception as e:
            print(f"Error processing folder {folder}: {e}")
