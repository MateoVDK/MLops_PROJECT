let isPremium = false;

// Toggle premium
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
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (!response.ok) {
            document.getElementById("result").textContent = data.detail;
            document.getElementById("explanation").textContent =
                "Premium feature — buy Premium to unlock detailed reasoning.";
            document.getElementById("confidence-bar").style.width = "0%";
            document.getElementById("confidence-label").textContent = "Premium only";
            return;
        }

        document.getElementById("result").textContent = data.action;

        if (data.confidence !== undefined) {
            const pct = Math.round(data.confidence * 100);
            document.getElementById("confidence-bar").style.width = pct + "%";
            document.getElementById("confidence-label").textContent = pct + "%";
        } else {
            document.getElementById("confidence-bar").style.width = "0%";
            document.getElementById("confidence-label").textContent = "Premium only";
        }

        if (data.explanation !== undefined) {
            document.getElementById("explanation").textContent = data.explanation;
        } else {
            document.getElementById("explanation").textContent =
                "Premium feature — buy Premium to unlock detailed reasoning.";
        }

    } catch (error) {
        console.error(error);
        document.getElementById("result").textContent = "Could not contact API";
        document.getElementById("explanation").textContent =
            "Premium feature — buy Premium to unlock detailed reasoning.";
        document.getElementById("confidence-bar").style.width = "0%";
        document.getElementById("confidence-label").textContent = "Premium only";
    }
});
