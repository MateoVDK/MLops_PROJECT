from fastapi import FastAPI
from app.schemas import GameState
from app.dummy_model import predict_action

app = FastAPI()

@app.post("/predict")
def predict(state: GameState):

    action, confidence = predict_action(
        state.player_sum,
        state.dealer_card,
        state.usable_ace
    )

    return {
        "action": action,
        "confidence": confidence
    }