import dataclasses

import math
from typing import Optional, List

from datetime import datetime

from ninja import Router
from ninja.files import UploadedFile

from ..session.models import SessionData, TimeStampFloat

from packages.emotion_recognition.processor import SERProcessor
from packages.hsd_recommender.hsd_recommender import HSDRecommender
from packages.hsd_recommender.models import SongFeatures
from packages.hsd_recommender.consts import GENRE_DATA_BASE
from packages.emotion_recognition.models import EmotionFeatures

from .schemas import (
    RecommendFromSpeechResponseSchema,
)

router = Router()
hsd_recommender = HSDRecommender()
serprocessor = SERProcessor()


def get_emotion_features_from_speech(file: UploadedFile) -> EmotionFeatures:
    """
    Extract emotion features from a speech audio file.
    :param file: Uploaded audio file
    :return: EmotionFeatures dataclass containing valence, arousal, dominance, authenticity, timeliness, and complexity
    """
    speech_emotion_result = serprocessor.process_audio_file(file)
    speech_emotion_result = dataclasses.asdict(speech_emotion_result)

    valence = float(speech_emotion_result["valence"])
    arousal = float(speech_emotion_result["arousal"])
    dominance = float(speech_emotion_result["dominance"])

    return EmotionFeatures(
        valence=valence,
        arousal=arousal,
    )


def calculate_array_switch_probability(values: List[TimeStampFloat]) -> float:
    """
    Calculate the probability that a song should switch for a single array.
    :param values: List of TimeStampFloat values, containing valence or arousal information
    :return: Switch probability as a float (0-1)
    """
    # todo
    return 1.0


@router.post("/from-speech", response=RecommendFromSpeechResponseSchema)
def recommend_from_speech(
    request,
    file: UploadedFile,
    genre: Optional[GENRE_DATA_BASE] = "none",
    authenticity: Optional[float] = None,
    timeliness: Optional[float] = None,
    complexity: Optional[float] = None,
    danceable: Optional[float] = None,
    tonal: Optional[float] = None,
    voice: Optional[float] = None,
    bpm: Optional[int] = None,
) -> RecommendFromSpeechResponseSchema:
    """
    Recommend a playlist based on speech emotion recognition.
    :param request: The request object
    :param file: Uploaded audio file
    :param genre: Genre filter for the recommendation
    :param authenticity: Authenticity feature for the recommendation
    :param timeliness: Timeliness feature for the recommendation
    :param complexity: Complexity feature for the recommendation
    :param danceable: Danceable feature for the recommendation
    :param tonal: Tonal feature for the recommendation
    :param voice: Voice feature for the recommendation
    :param bpm: Beats per minute feature for the recommendation
    :return: A playlist based on the emotion features extracted from the speech
    """

    session = request.session
    session_data = session.get("data", SessionData())
    # todo add min play length, add song switch proba

    emotion_features = get_emotion_features_from_speech(file)
    features = SongFeatures(
        valence=emotion_features.valence,
        arousal=emotion_features.arousal,
        authenticity=authenticity,
        timeliness=timeliness,
        complexity=complexity,
        danceable=danceable,
        tonal=tonal,
        voice=voice,
        bpm=bpm,
    )

    # todo combine emotion features from speech and text

    playlist = hsd_recommender.generate_playlist(songFeatures=features, genre=genre)

    # Calculate Switch Probability
    timestamp = datetime.now()
    session_data.valence_values.append(
        TimeStampFloat(timestamp=timestamp, value=emotion_features.valence)
    )
    session_data.arousal_values.append(
        TimeStampFloat(timestamp=timestamp, value=emotion_features.arousal)
    )

    # todo
    valence_switch_probability = calculate_array_switch_probability(
        session_data.valence_values
    )
    arousal_switch_probability = calculate_array_switch_probability(
        session_data.arousal_values
    )
    switch_probability = (valence_switch_probability + arousal_switch_probability) / 2

    # todo use a song thats not in played_songs
    response = RecommendFromSpeechResponseSchema(
        song=playlist[0], features=features, switch_probability=switch_probability
    )

    session.save()
    return response
