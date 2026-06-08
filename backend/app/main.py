from fastapi import FastAPI, Request
from app.schemas import GameState
from app.dummy_model import predict_action
from app.rate_limit import check_rate_limit
from fastapi.middleware.cors import CORSMiddleware
from app.explaination import generate_explanation

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
@app.post("/api/predict")
def predict(state: GameState, request: Request):

    allowed, detail = check_rate_limit(request, state.premium)
    if not allowed:
        return {"error": detail}

    action, confidence = predict_action(
        state.player_sum,
        state.dealer_card,
        state.usable_ace
    )

    # Only premium users get explanations
    if state.premium:
        explanation = generate_explanation(
            state.player_sum,
            state.dealer_card,
            state.usable_ace,
            action,
            confidence
        )

        return {
            "action": action,
            "confidence": confidence,
            "explanation": explanation
        }

    return {"action": action}


