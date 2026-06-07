from fastapi import FastAPI, Request
from app.schemas import GameState
from app.dummy_model import predict_action
from app.rate_limit import check_rate_limit

app = FastAPI()

@app.post("/predict")
def predict(state: GameState, request: Request):

    check_rate_limit(request, state.premium)

    action, confidence = predict_action(
        state.player_sum,
        state.dealer_card,
        state.usable_ace
    )

    return {
        "action": action,
        "confidence": confidence
    }
