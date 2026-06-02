import os
import pickle
import gymnasium as gym
import numpy as np
from collections import defaultdict

# setting up environment
env = gym.make("Blackjack-v1")
env.reset()

# training
episodes = 10_000_000
gamma = 1.0

epsilon_start = 1.0
epsilon_end = 0.05
epsilon_decay_rate = 0.9999

nA = env.action_space.n

Q = defaultdict(lambda: np.zeros(nA, dtype=np.float64))
N = defaultdict(lambda: np.zeros(nA, dtype=np.int64))


def get_epsilon(episode):
    return max(epsilon_end, epsilon_start * (epsilon_decay_rate ** episode))


def epsilon_greedy_probs(state, epsilon):
    probs = np.ones(nA) * (epsilon / nA)
    best_action = np.argmax(Q[state])
    probs[best_action] += 1.0 - epsilon
    return probs


for episode in range(episodes):
    state, _ = env.reset()
    trajectory = []
    done = False

    epsilon = get_epsilon(episode)

    while not done:
        probs = epsilon_greedy_probs(state, epsilon)
        action = np.random.choice(np.arange(nA), p=probs)

        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        trajectory.append((state, action, reward))
        state = next_state

    G = 0.0
    visited = set()

    for t in reversed(range(len(trajectory))):
        s, a, r = trajectory[t]
        G = gamma * G + r

        if (s, a) not in visited:
            visited.add((s, a))
            N[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / N[s][a]

    if (episode + 1) % 500_000 == 0:
        print(f"Episode {episode + 1}, epsilon={get_epsilon(episode):.4f}")


policy = {s: int(np.argmax(a)) for s, a in Q.items()}

artifact = {
    "policy": policy,
    "episodes": episodes,
    "gamma": gamma,
    "epsilon_start": epsilon_start,
    "epsilon_end": epsilon_end,
    "epsilon_decay_rate": epsilon_decay_rate,
}

os.makedirs("./outputs", exist_ok=True)
with open("./outputs/policy.pkl", "wb") as f:
    pickle.dump(artifact, f)

print("Training finished.")
print("Policy saved to ./outputs/policy.pkl")