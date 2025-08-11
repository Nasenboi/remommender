from typing import List, Optional, Tuple

from ninja import Schema


class SessionData(Schema):
    songs_played: Optional[List[str]] = list()
    sample_index: Optional[int] = 0
    samples: Optional[Tuple[List[float], List[float]]] = list()
    old_mean: Optional[Tuple[float, float]] = (0.0, 0.0)
