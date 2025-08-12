from typing import List, Optional, Tuple

from ninja import Schema

from apps.core.consts import EMOTION_VALUES_WINDOW_SIZE


class SessionData(Schema):
    songs_played: Optional[List[str]] = list()
    samples: Optional[Tuple[List[float], List[float]]] = (
        [0.5] * EMOTION_VALUES_WINDOW_SIZE,
        [0.5] * EMOTION_VALUES_WINDOW_SIZE,
    )
    old_mean: Optional[Tuple[float, float]] = (0.0, 0.0)
