from pydantic import BaseModel

class GameState(BaseModel):
    player_sum: int
    dealer_card: int
    usable_ace: bool = False


class PredictionResponse(BaseModel):
    action: str
    confidence: float

class GameState(BaseModel):
    player_sum: int
    dealer_card: int
    usable_ace: bool
    premium: bool = False
