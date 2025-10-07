from typing import Optional

from ninja import Router
from ninja.errors import HttpError
from ninja.files import UploadedFile

from apps.core.schemas import SongFeaturesSchema
from apps.session.schemas import SessionData

from .methods import (
    calculate_array_switch_probability,
    get_emotion_features_from_speech,
    get_song_recommendation,
    update_session_data,
)
from .recommender.consts import GENRE_DATA_BASE
from .recommender.methods import generate_playlist
from .schemas import RecommendFromSpeechResponseSchema

router = Router(tags=["recommendations"])


@router.post("/from-speech", response=RecommendFromSpeechResponseSchema)
def recommend_from_speech(
    request,
    file: UploadedFile,
    genre: Optional[GENRE_DATA_BASE] = None,
    authenticity: Optional[float] = None,
    timeliness: Optional[float] = None,
    complexity: Optional[float] = None,
    danceability: Optional[float] = None,
    tonal: Optional[float] = None,
    voice: Optional[float] = None,
    bpm: Optional[float] = None,
    arousal_weight: Optional[float] = 0.5,
    valence_weight: Optional[float] = 0.5,
    invert_arousal: Optional[bool] = False,
    invert_valence: Optional[bool] = False,
):
    session_data = request.session.get("data", SessionData().model_dump())

    emotion_features = get_emotion_features_from_speech(file)

    valence = emotion_features.valence
    arousal = emotion_features.arousal

    if invert_valence:
        valence = -valence
    if invert_arousal:
        arousal = -arousal

    print(invert_valence)

    features = SongFeaturesSchema(
        valence=valence,
        arousal=arousal,
        authenticity=authenticity,
        timeliness=timeliness,
        complexity=complexity,
        danceability=danceability,
        tonal=tonal,
        voice=voice,
        bpm=bpm,
    )

    playlist = generate_playlist(genre=genre, features=features)

    if len(playlist) == 0:
        raise HttpError(
            500,
            "No recommendation could be generated. This is probably because the song library is empty or you have set filters for which no song could be found within the library.",
        )

    session_data = update_session_data(valence, arousal, session_data)

    session_data["old_mean"], switch_probability = calculate_array_switch_probability(
        session_data, arousal_weight, valence_weight
    )

    song = get_song_recommendation(playlist, session_data["songs_played"])

    # save updated session data
    request.session["data"] = session_data

    return RecommendFromSpeechResponseSchema(
        song=song,
        speech_features=emotion_features,
        switch_probability=switch_probability
    )
