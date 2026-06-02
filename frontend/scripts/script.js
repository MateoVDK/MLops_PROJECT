const button = document.getElementById("predict-btn");
const result = document.getElementById("result");

button.addEventListener("click", () => {

    const playerSum = document.getElementById("player-sum").value;
    const dealerCard = document.getElementById("dealer-card").value;

    if (!playerSum || !dealerCard) {
        result.textContent = "Please fill all fields";
        return;
    }

    const actions = ["HIT", "STAND"];
    const randomAction =
        actions[Math.floor(Math.random() * actions.length)];

    result.textContent = randomAction;
});