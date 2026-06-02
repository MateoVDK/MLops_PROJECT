from fastapi import FastAPI
from app.schemas import GameState, PredictionResponse
from app.dummy_model import predict_action

app = FastAPI(title="Blackjack RL API")


@app.get("/")
def root():
    return {"message": "Blackjack RL API is running"}


@app.post("/predict", response_model=PredictionResponse)
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