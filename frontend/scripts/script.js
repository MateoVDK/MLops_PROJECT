let isPremium = false;

document.getElementById("premium-btn").addEventListener("click", () => {
    isPremium = !isPremium;

    if (isPremium) {
        alert("You are now a PREMIUM user! Unlimited predictions unlocked.");
        document.getElementById("premium-btn").innerText = "Premium Active";
        document.getElementById("premium-btn").style.opacity = "0.7";
    } else {
        alert("Premium disabled. You are now a FREE user again.");
        document.getElementById("premium-btn").innerText = "Buy Premium";
        document.getElementById("premium-btn").style.opacity = "1";
    }
});

document.getElementById("predict-btn").addEventListener("click", async () => {

    const payload = {
        player_sum: Number(document.getElementById("player-sum").value),
        dealer_card: Number(document.getElementById("dealer-card").value),
        usable_ace: document.getElementById("usable-ace").checked,
        premium: isPremium
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // ⭐ Handle rate limit errors (429)
        if (!response.ok) {
            document.getElementById("result").textContent = data.detail;
            return;
        }

        // ⭐ Show confidence only for premium users
        if (data.confidence !== undefined) {
            document.getElementById("result").textContent =
                `${data.action} (${Math.round(data.confidence * 100)}%)`;
        } else {
            document.getElementById("result").textContent = data.action;
        }

    } catch (error) {
        console.error(error);
        document.getElementById("result").textContent =
            "Could not contact API";
    }
});
