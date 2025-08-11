from pydantic import BaseModel
from typing import Optional, List, Tuple

from datetime import datetime


class TimeStampFloat(BaseModel):
    timestamp: datetime
    value: float


class SessionData(BaseModel):
    songs_played: Optional[List[str]] = []
    valence_values: Optional[List[TimeStampFloat]] = []
    arousal_values: Optional[List[TimeStampFloat]] = []
