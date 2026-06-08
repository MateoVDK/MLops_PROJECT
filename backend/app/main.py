from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from app.schemas import GameState
from app.dummy_model import predict_action
from app.rate_limit import check_rate_limit
from fastapi.middleware.cors import CORSMiddleware
from app.explaination import generate_explanation
from app.database import get_db, init_db
from app.models import Prediction


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
def predict(state: GameState, request: Request, db: Session = Depends(get_db)):

    allowed, detail = check_rate_limit(request, state.premium)
    if not allowed:
        return {"error": detail}

    action, confidence = predict_action(
        state.player_sum,
        state.dealer_card,
        state.usable_ace
    )

    try:
        pred = Prediction(
            player_sum=state.player_sum,
            dealer_card=state.dealer_card,
            usable_ace=state.usable_ace,
            action=action,
            confidence=confidence,
            premium=state.premium,
        )
        db.add(pred)
        db.commit()
    except Exception as e:
        print("DB logging error:", e)
        # Try to initialize DB tables and retry once
        try:
            db.rollback()
        except Exception:
            pass
        try:
            init_db()
            db.add(pred)
            db.commit()
        except Exception as e2:
            print("DB retry failed:", e2)

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



@app.on_event("startup")
def on_startup():
    # ensure tables exist
    try:
        init_db()
    except Exception:
        print("Failed to initialize DB on startup")


