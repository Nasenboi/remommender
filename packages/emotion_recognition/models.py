from pydantic import BaseModel


class EmotionFeatures(BaseModel):
    valence: float
    arousal: float
