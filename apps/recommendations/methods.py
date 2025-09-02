from typing import List, Tuple

from ninja.files import UploadedFile

from apps.core.schemas import Playlist, SongSchema
from apps.session.schemas import SessionData

from .emotion_recognition.processor import SERProcessor
from .emotion_slope_detection.emotion_slope_detection import get_slope_probability, update_samples
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
        valence=speech_emotion_result.valence * 2 - 1,
        arousal=speech_emotion_result.arousal * 2 - 1,
    )


def update_session_data(valence: float, arousal: float, session_data: SessionData) -> SessionData:
    """
    Update the session data with new valence and arousal values.
    :param valence: Valence value
    :param arousal: Arousal value
    :param session_data: Current session data
    :return: Updated session data
    """
    session_data["samples"] = update_samples(valence, arousal, session_data["samples"])
    return session_data


def calculate_array_switch_probability(
    session_data: SessionData,
) -> Tuple[float, float]:
    """
    Calculate the probability that a song should switch for a single array.
    :param values: List of TimeStampFloat values, containing valence or arousal information
    :return: The calculated welford mean value and the switch probability as a float (0-1)
    """

    return get_slope_probability(session_data["samples"], session_data["old_mean"])


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
        if str(song.id) not in songs_played:
            return song
    return playlist[0] if playlist else None
