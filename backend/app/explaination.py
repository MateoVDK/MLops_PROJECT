def generate_explanation(player_sum, dealer_card, usable_ace, action, confidence):
    if usable_ace:
        if action == "hit":
            return f"Your hand is soft ({player_sum}), meaning you can't bust immediately. Hitting is safe and increases your chance to improve."
        if action == "stand":
            return f"Your soft {player_sum} is already strong against dealer {dealer_card}. Standing avoids reducing your advantage."
        if action == "double":
            return f"Soft hands are ideal doubling opportunities. With dealer {dealer_card}, doubling maximizes expected value."

    if not usable_ace:
        if player_sum <= 11:
            return f"With a hard {player_sum}, you cannot bust by hitting. Taking another card is always the best move."

        if 12 <= player_sum <= 16:
            if dealer_card >= 7:
                return f"Your {player_sum} is weak against a dealer {dealer_card}. Hitting gives you the best chance to avoid losing."
            else:
                return f"Dealer {dealer_card} is likely to bust. Standing with {player_sum} takes advantage of their weak position."

        if player_sum >= 17:
            return f"A hard {player_sum} is strong. Hitting risks busting, so standing is the safest and highest‑EV move."

    return f"This action maximizes your expected value with {player_sum} vs dealer {dealer_card}."
