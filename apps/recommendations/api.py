import dataclasses

from ninja import Router
from ninja.files import UploadedFile

from packages.emotion_recognition.processor import SERProcessor
from packages.hsd_recommender.hsd_recommender import HSDRecommender
from packages.hsd_recommender.models import EmotionFeatures

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
    if isinstance(speech_emotion_result, list):
        speech_emotion_result = speech_emotion_result[0]
    speech_emotion_result = dataclasses.asdict(speech_emotion_result)

    valence = float(speech_emotion_result["valence"])
    arousal = float(speech_emotion_result["arousal"])
    dominance = float(speech_emotion_result["dominance"])
    # pseudo features
    authenticity = valence * dominance
    timeliness = arousal * dominance
    complexity = dominance

    return EmotionFeatures(
        valence=valence,
        arousal=arousal,
        dominance=dominance,
        authenticity=authenticity,
        timeliness=timeliness,
        complexity=complexity,
    )


@router.post("/from-speech", response=RecommendFromSpeechResponseSchema)
def recommend_from_speech(
    request, file: UploadedFile
) -> RecommendFromSpeechResponseSchema:
    """
    Recommend a playlist based on speech emotion recognition.
    :param request: The request object
    :param file: Uploaded audio file
    :param query: Query parameters for the recommendation
    :return: A playlist based on the emotion features extracted from the speech
    """

    session = request.session
    played_songs = session.get("songs_played", [])

    emotion_features = get_emotion_features_from_speech(file)
    # todo combine emotion features from speech and text

    playlist = hsd_recommender.generate_emotional_playlist(
        emotionFeatures=emotion_features[0]
    )

    emotion_features = emotion_features[0]

    response = RecommendFromSpeechResponseSchema(
        song=playlist[0], emotion_features=emotion_features  # todo
    )

    session.save()
    return response
