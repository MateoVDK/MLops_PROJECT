from fastapi import FastAPI, Request
from app.schemas import GameState
from app.dummy_model import predict_action
from app.rate_limit import check_rate_limit
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
def predict(state: GameState, request: Request):

    check_rate_limit(request, state.premium)

    action, confidence = predict_action(
        state.player_sum,
        state.dealer_card,
        state.usable_ace
    )

    # Only premium users get confidence
    if state.premium:
        return {
            "action": action,
            "confidence": confidence
        }
    else:
        return {
            "action": action
        }

