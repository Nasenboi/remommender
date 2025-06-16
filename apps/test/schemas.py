from typing import Literal, List, Optional
from pydantic import BaseModel


class SERProcessorEmotionSchema(BaseModel):
    valence: float
    arousal: float
    dominance: float
