import os
from typing import List, Tuple

import pandas as pd
from ninja.files import UploadedFile

from apps.session.schemas import SessionData

from .emotion_recognition.processor import SERProcessor
from .emotion_slope_detection.emotion_slope_detection import get_slope_probability, update_samples
from .models import RecommendationStatistics
from .schemas import EmotionFeaturesSchema, RecommendationStatisticsSchema


def get_serprocessor() -> SERProcessor:
    """
    Singleton pattern to get the SERProcessor instance.
    """
    if not hasattr(get_serprocessor, "_instance"):
        get_serprocessor._instance = SERProcessor()
    return get_serprocessor._instance


# run on api server startup
if os.getenv("START_MODELS"):
    get_serprocessor()


def get_emotion_features_from_speech(file: UploadedFile) -> EmotionFeaturesSchema:
    """
    Extract emotion features from a speech audio file.
    :param file: Uploaded audio file
    :return: EmotionFeatures dataclass containing valence, arousal, dominance, authenticity, timeliness, and complexity
    """
    speech_emotion_result = get_serprocessor().process_audio_file(file)

    valence = speech_emotion_result.valence * 2 - 1
    arousal = speech_emotion_result.arousal * 2 - 1

    return EmotionFeaturesSchema(valence=valence, arousal=arousal)


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
    session_data: SessionData, arousal_weight: float = 0.5, valence_weight: float = 0.5
) -> Tuple[float, float]:
    """
    Calculate the probability that a song should switch for a single array.
    :param session_data: Current session data
    :param arousal_weight: Weight for arousal value (default: 0.5)
    :param valence_weight: Weight for valence value (default: 0.5)
    :return: The calculated welford mean value and the switch probability as a float (0-1)
    """

    return get_slope_probability(session_data["samples"], session_data["old_mean"], arousal_weight, valence_weight)


def summarize_statistics() -> pd.DataFrame:
    """
    Summarize recommendation statistics into a pandas DataFrame.
    """
    stats = RecommendationStatistics.objects.all().select_related("song", "album")
    data = []
    for stat in stats:
        data.append(RecommendationStatisticsSchema.from_orm(stat).model_dump())
    df = pd.DataFrame(data)
    return df
