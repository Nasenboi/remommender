import dataclasses

from ninja import Router
from ninja.files import UploadedFile

from packages.emotion_recognition.processor import SERProcessor
from packages.hsd_recommender.hsd_recommender import HSDRecommender
from packages.hsd_recommender.models import SongFeatures
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


@router.post("/from-speech", response=RecommendFromSpeechResponseSchema)
def recommend_from_speech(
    request, file: UploadedFile  # todo add genre query
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
    # todo add min play length, add song switch proba

    emotion_features = get_emotion_features_from_speech(file)
    features = SongFeatures(
        valence=emotion_features.valence,
        arousal=emotion_features.arousal,
    )

    # todo combine emotion features from speech and text

    playlist = hsd_recommender.generate_playlist(songFeatures=features)

    # todo use a song thats not in played_songs
    response = RecommendFromSpeechResponseSchema(
        song=playlist[0], features=features  # todo
    )

    session.save()
    return response
