let isPremium = false;

async function getErrorMessage(response) {
    if (response.status === 429) {
        return "Rate limit reached: max 10 requests per hour for free users.";
    }

    const responseCopy = response.clone();

    try {
        const errorData = await responseCopy.json();
        return errorData.detail || errorData.message || "Request failed";
    } catch {
        try {
            const text = await responseCopy.text();
            return text || "Request failed";
        } catch {
            return "Request failed";
        }
    }
}

function showError(message) {
    alert(message);

    document.getElementById("result").textContent = message;
    document.getElementById("result").style.color = "red";

    document.getElementById("explanation").textContent = "";
    document.getElementById("confidence-bar").style.width = "0%";
    document.getElementById("confidence-label").textContent = "";
}

// Detect environment (local dev vs Kubernetes)
const API_URL =
    window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
        ? "http://127.0.0.1:8000/predict"   // local port-forward
        : "/api/predict";                   // Kubernetes ingress

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
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // ERROR HANDLING (rate limit, invalid input, etc.)
        if (!response.ok || data.error || (data.detail && !data.action)) {
            const errorMessage =
                data.error ||
                data.detail ||
                (await getErrorMessage(response)) ||
                "Request failed";

            showError(errorMessage);

            return;
        }

        // SUCCESSFUL RESPONSE
        document.getElementById("result").textContent = data.action;
        document.getElementById("result").style.color = "white";

        // Confidence bar
        if (data.confidence !== undefined) {
            const pct = Math.round(data.confidence * 100);
            document.getElementById("confidence-bar").style.width = pct + "%";
            document.getElementById("confidence-label").textContent = pct + "%";
        } else {
            document.getElementById("confidence-bar").style.width = "0%";
            document.getElementById("confidence-label").textContent = "Premium only";
        }

        // Explanation
        if (data.explanation !== undefined) {
            document.getElementById("explanation").textContent = data.explanation;
        } else {
            document.getElementById("explanation").textContent =
                "Premium feature — buy Premium to unlock detailed reasoning.";
        }

    } catch (error) {
        console.error(error);

        showError("Could not contact API");
    }
});
