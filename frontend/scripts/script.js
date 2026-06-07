let isPremium = false;

// Toggle premium on/off
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

        // Handle rate limit errors
        if (!response.ok) {
            document.getElementById("result").textContent = data.detail;

            // Reset explanation + confidence bar
            document.getElementById("explanation").textContent =
                "Premium feature — buy Premium to unlock detailed reasoning.";

            document.getElementById("confidence-bar").style.width = "0%";
            document.getElementById("confidence-label").textContent = "Premium only";

            return;
        }

        // ⭐ Update recommendation (NO confidence here anymore)
        document.getElementById("result").textContent = data.action;

        // ⭐ Update confidence bar (premium only)
        if (data.confidence !== undefined) {
            const pct = Math.round(data.confidence * 100);
            document.getElementById("confidence-bar").style.width = pct + "%";
            document.getElementById("confidence-label").textContent = pct + "%";
        } else {
            // Free users see empty bar
            document.getElementById("confidence-bar").style.width = "0%";
            document.getElementById("confidence-label").textContent = "Premium only";
        }

        // ⭐ Update explanation
        if (data.explanation !== undefined) {
            document.getElementById("explanation").textContent = data.explanation;
        } else {
            document.getElementById("explanation").textContent =
                "Premium feature — buy Premium to unlock detailed reasoning.";
        }

    } catch (error) {
        console.error(error);

        document.getElementById("result").textContent = "Could not contact API";

        // Reset explanation + confidence bar
        document.getElementById("explanation").textContent =
            "Premium feature — buy Premium to unlock detailed reasoning.";

        document.getElementById("confidence-bar").style.width = "0%";
        document.getElementById("confidence-label").textContent = "Premium only";
    }
});
