import dataclasses

from ninja import Router
from ninja.files import UploadedFile

from packages.hsd_recommender.models import SongFeatures

from ..recommendations.api import (
    serprocessor,
)

from .schemas import SERProcessorEmotionSchema

router = Router()


def get_ser_emotion_features_from_speech(
    file: UploadedFile,
) -> SERProcessorEmotionSchema:
    """
    Extract emotion features from a speech audio file.
    :param file: Uploaded audio file
    :return: EmotionFeatures dataclass containing valence, arousal, dominance, authenticity, timeliness, and complexity
    """
    speech_emotion_result = serprocessor.process_audio_file(file)
    speech_emotion_result = dataclasses.asdict(speech_emotion_result)

    return speech_emotion_result


@router.post("/from-speech", response=SERProcessorEmotionSchema)
def from_speech(request, file: UploadedFile):
    """
    Endpoint to extract emotion features from a speech audio file.
    :param request: HTTP request object
    :param file: Uploaded audio file
    :return: EmotionFeatures dataclass containing valence, arousal, dominance, authenticity, timeliness, and complexity
    """
    session = request.session
    emotion_features = get_ser_emotion_features_from_speech(file)
    session.save()
    return emotion_features
