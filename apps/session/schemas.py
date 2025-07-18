from typing import List, Optional

from ninja import Schema


class SessionData(Schema):
    songs_played: Optional[List[str]] = list()
    value_index: Optional[int] = 0
    valence_values: Optional[List[float]] = list()
    arousal_values: Optional[List[float]] = list()
