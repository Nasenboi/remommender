import dataclasses

from typing import Optional

from ninja import Router
from ninja.files import UploadedFile

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
    played_songs = session.get("songs_played", [])
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

    # todo use a song thats not in played_songs
    response = RecommendFromSpeechResponseSchema(
        song=playlist[0], features=features  # todo
    )

    session.save()
    return response
