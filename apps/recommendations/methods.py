import dataclasses
from typing import List, Tuple

from ninja.files import UploadedFile

from apps.core.schemas import Playlist, SongSchema

from .emotion_recognition.processor import SERProcessor
from .schemas import EmotionFeaturesSchema

serprocessor = SERProcessor()


def get_emotion_features_from_speech(file: UploadedFile) -> EmotionFeaturesSchema:
    """
    Extract emotion features from a speech audio file.
    :param file: Uploaded audio file
    :return: EmotionFeatures dataclass containing valence, arousal, dominance, authenticity, timeliness, and complexity
    """
    speech_emotion_result = serprocessor.process_audio_file(file)

    return EmotionFeaturesSchema(
        valence=speech_emotion_result.valence,
        arousal=speech_emotion_result.arousal,
    )


def calculate_array_switch_probability(
    arousal_values: List[float],
    valence_values: List[float],
    value_index: int,
) -> float:
    """
    Calculate the probability that a song should switch for a single array.
    :param values: List of TimeStampFloat values, containing valence or arousal information
    :return: Switch probability as a float (0-1)
    """
    # todo
    return 1.0


def get_song_recommendation(
    playlist: Playlist,
    songs_played: List[str],
) -> SongSchema:
    """
    Return either a song that was not played yet or the first song from the playlist.
    :param playlist: Playlist containing SongSchema objects.
    :param songs_played: List of song IDs that have already been played.
    :return: A SongSchema object representing the recommended song.
    """
    for song in playlist:
        if song.id not in songs_played:
            return song
    return playlist[0] if playlist else None
