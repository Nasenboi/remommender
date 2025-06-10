from ninja import Router
from ninja.responses import Response

router = Router()

@router.post("/start")
def start_session(request):
    session = request.session
    session["songs_played"] = []
    session.save()
    return {"session_key": session.session_key, "message": "Session started"}

@router.post("/end")
def end_session(request):
    request.session.flush()
    return {"message": "Session ended"}