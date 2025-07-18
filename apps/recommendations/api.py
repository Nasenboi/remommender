from typing import Optional

from ninja import Router
from ninja.files import UploadedFile

from apps.core.schemas import SongFeaturesSchema
from apps.session.schemas import SessionData

from .methods import (
    calculate_array_switch_probability,
    get_emotion_features_from_speech,
    get_song_recommendation,
)
from .recommender.consts import GENRE_DATA_BASE
from .recommender.methods import generate_playlist
from .schemas import RecommendFromSpeechResponseSchema

router = Router(tags=["recommendations"])


@router.post("/from-speech", response=RecommendFromSpeechResponseSchema)
def recommend_from_speech(
    request,
    file: UploadedFile,
    genre: Optional[GENRE_DATA_BASE] = "none",
    authenticity: Optional[float] = None,
    timeliness: Optional[float] = None,
    complexity: Optional[float] = None,
    danceability: Optional[float] = None,
    tonal: Optional[float] = None,
    voice: Optional[float] = None,
    bpm: Optional[float] = None,
):
    session_data = request.session.get("session_data", SessionData().model_dump())

    emotion_features = get_emotion_features_from_speech(file)

    features = SongFeaturesSchema(
        valence=emotion_features.valence,
        arousal=emotion_features.arousal,
        authenticity=authenticity,
        timeliness=timeliness,
        complexity=complexity,
        danceability=danceability,
        tonal=tonal,
        voice=voice,
        bpm=bpm,
    )

    playlist = generate_playlist(genre=genre, features=features)

    switch_probablity = calculate_array_switch_probability(
        session_data["arousal_values"],
        session_data["valence_values"],
        session_data["value_index"],
    )

    song = get_song_recommendation(playlist, session_data["songs_played"])

    return RecommendFromSpeechResponseSchema(
        song=song,
        features=features,
        switch_probability=switch_probablity,
    )
