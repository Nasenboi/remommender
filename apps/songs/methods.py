import json
import os
from typing import Tuple

from django.core.files import File

from apps.core.models import Album, Song, SongFeatures, SongGenres


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
        "album": song["album"],
        "artist": song["artist"],
    }
    return db_song, db_album


def add_album_to_db(name: str, album_name: str = None, artist: str = None) -> str:
    """
    Adds an album artwork_file to the db if it does not exist yet.
    Returns the id of the object.
    """
    path = os.path.join(os.getenv("PRE_CALC_ALBUM_ART_PATH"), name)
    artwork_file = Album.objects.filter(album=album_name, artist=artist).first()
    if not artwork_file:
        with open(path, "rb") as f:
            artwork_file = Album.objects.create(artwork_file=File(f, name=name), album=album_name, artist=artist)
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
        album_id = add_album_to_db(raw_data["ids"]["artwork_id"], db_album["album"], db_album["artist"])
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
