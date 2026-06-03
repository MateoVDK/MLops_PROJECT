# this is temporary code to test the api, it will be replaced with the actual model code later

import random

def predict_action(player_sum: int, dealer_card: int, usable_ace: bool):
    
    # simple heuristic (better than pure random for demo)
    if player_sum >= 18:
        action = "STAND"
    elif player_sum <= 11:
        action = "HIT"
    else:
        action = random.choice(["HIT", "STAND"])

    confidence = round(random.uniform(0.6, 0.95), 2)

    return action, confidence