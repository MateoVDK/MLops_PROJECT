from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.explaination import generate_explanation
from app.model import get_policy_decision, model_metadata
from app.models import Prediction
from app.rate_limit import check_rate_limit
from app.schemas import GameState

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": True, "model_metadata": model_metadata}


@app.post("/predict")
@app.post("/api/predict")
def predict(state: GameState, request: Request, db: Session = Depends(get_db)):
    allowed, detail = check_rate_limit(request, state.premium)
    if not allowed:
        raise HTTPException(status_code=429, detail=detail)

    decision = get_policy_decision(
        state.player_sum,
        state.dealer_card,
        state.usable_ace,
    )

    action = decision["action"]
    confidence = decision["confidence"]

    prediction_payload = {
    "player_sum": state.player_sum,
    "dealer_card": state.dealer_card,
    "usable_ace": state.usable_ace,
    "action": action,
    "action_code": decision["action_code"],
    "confidence": confidence,
    "premium": state.premium,
    "policy_found": decision["policy_found"],
    "policy_state": str(decision["state"]),
    }

    try:
        prediction_log = Prediction(**prediction_payload)
        db.add(prediction_log)
        db.commit()
    except Exception as error:
        print("DB logging error:", error)
        try:
            db.rollback()
        except Exception:
            pass

        try:
            init_db()
            prediction_log = Prediction(**prediction_payload)
            db.add(prediction_log)
            db.commit()
        except Exception as retry_error:
            print("DB retry failed:", retry_error)

    if state.premium:
        explanation = generate_explanation(
            state.player_sum,
            state.dealer_card,
            state.usable_ace,
            action,
            confidence,
        )

        return {
            "action": action,
            "confidence": confidence,
            "explanation": explanation,
        }

    return {"action": action}


@app.on_event("startup")
def on_startup():
    try:
        init_db()
    except Exception:
        print("Failed to initialize DB on startup")
