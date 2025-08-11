from ninja import Router
from ninja.responses import Response

from .models import SessionData

router = Router()


@router.post("/start")
def start_session(request) -> Response:
    session = request.session
    session["data"] = SessionData()
    session.save()
    return {"session_key": session.session_key, "message": "Session started"}


@router.post("/end")
def end_session(request) -> Response:
    session = request.session
    session.flush()
    return {"message": "Session ended"}


@router.post("/clear")
def clear_session(request) -> Response:
    session = request.session
    session["data"] = SessionData()
    session.save()
    return {"message": "Session cleared"}
