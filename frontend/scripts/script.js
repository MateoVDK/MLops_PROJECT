async function getRecommendation() {

    const playerSum = document.getElementById("player-sum").value;
    const dealerCard = document.getElementById("dealer-card").value;
    const usableAce = document.getElementById("usable-ace").checked;

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                player_sum: Number(playerSum),
                dealer_card: Number(dealerCard),
                usable_ace: usableAce
            })
        });

        const data = await response.json();

        document.getElementById("result").textContent =
            `${data.action} (${Math.round(data.confidence * 100)}%)`;

    } catch (error) {
        console.error(error);
        document.getElementById("result").textContent =
            "Could not contact API";
    }
}

document.getElementById("predict-btn")
    .addEventListener("click", getRecommendation);