from ninja import Router

from .schemas import SessionData

router = Router(tags=["sessions"])


@router.post("/start")
def start_session(request):
    request.session["data"] = SessionData().model_dump()
    return {"message": "Session started"}


@router.post("/add-played-song")
def add_played_song(request, song_id: str):
    session_data = request.session.get("data", SessionData().model_dump())
    session_data["songs_played"].append(song_id)
    request.session["data"] = session_data
    return {"message": "Song added to played list", "song_id": song_id}


@router.post("/end")
def end_session(request):
    request.session.flush()
    return {"message": "Session ended"}


@router.post("/clear")
def clear_session(request):
    request.session["data"] = SessionData().model_dump()
    return {"message": "Session cleared"}
