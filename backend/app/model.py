import pickle
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

ACTION_LABELS = {
    0: "stand",
    1: "hit",
    2: "double",
}

DEFAULT_ACTION_CODE = 0
MODEL_PATH = Path(__file__).resolve().parent / "predictor" / "policy.pkl"


def _load_model(path: Path = MODEL_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Policy file was not found at {path}")

    with path.open("rb") as file:
        artifact = pickle.load(file)

    if isinstance(artifact, dict) and "policy" in artifact:
        return artifact

    return {"policy": artifact}


_model_artifact = _load_model()
policy: Dict[Tuple[int, int, bool], Any] = _model_artifact["policy"]
q_values: Optional[Dict[Tuple[int, int, bool], Any]] = (
    _model_artifact.get("q_values")
    or _model_artifact.get("Q")
    or _model_artifact.get("q_table")
)
model_metadata = {
    key: value
    for key, value in _model_artifact.items()
    if key not in {"policy", "q_values", "Q", "q_table"}
}


def _normalise_action_code(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return DEFAULT_ACTION_CODE


def _action_label(action_code: int) -> str:
    return ACTION_LABELS.get(action_code, str(action_code))


def _confidence_from_q_values(state: Tuple[int, int, bool]) -> Optional[float]:
    if not q_values:
        return None

    values = q_values.get(state)
    if values is None:
        return None

    values = [float(value) for value in values]
    if not values:
        return None

    best = max(values)
    total = sum(abs(value) for value in values)
    if total <= 1e-8:
        return None

    return max(0.0, min(1.0, abs(best) / total))


def get_policy_decision(player_sum: int, dealer_card: int, usable_ace: bool) -> Dict[str, Any]:
    state = (player_sum, dealer_card, usable_ace)
    policy_found = state in policy
    action_code = _normalise_action_code(policy.get(state, DEFAULT_ACTION_CODE))
    confidence = _confidence_from_q_values(state)

    if confidence is None:
        confidence = 1.0 if policy_found else 0.0

    return {
        "state": state,
        "policy_found": policy_found,
        "action_code": action_code,
        "action": _action_label(action_code),
        "confidence": confidence,
    }
