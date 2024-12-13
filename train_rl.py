import numpy as np
from GomokuEnv import GomokuEnv
from feature_extractor import feature_extractor

# Hyperparameters
alpha = 0.1     # LR
gamma = 0.9     # discount factor
lam = 0.9       # trace decay
epsilon = 0.1   # exploration rate
num_features = 100
num_episodes = 1000
# initialize weight vector for linear function approximation
w = np.zeros(num_features)
feature_indices = range(num_features)



def select_action(env, w, epsilon, player):
    actions = env.get_available_actions()
    if not actions:
        return None
    if np.random.rand() < epsilon:
        # explore - choose a random action
        return actions[np.random.choice(len(actions))]
    # Greedy w.r.t Q
    # exploit - choose the actions with the highest value
    q_values = []
    state = env._get_state()
    for a in actions:
        phi = feature_extractor(state, a, player)
        q_values.append(np.dot(w, phi))
    return actions[np.argmax(q_values)]

env = GomokuEnv()
for episode in range(num_episodes):
    state = env.reset()
    player = env.current_player
    e = np.zeros(num_features)  # eligibility traces

    # initial action
    a = select_action(env, w, epsilon, player)

    done = False
    while not done:
        # take action & observe the next state then reward
        next_state, reward, done, info = env.step(a)
        next_player = env.current_player

        # compute features for (s,a)
        phi = feature_extractor(state, a, player)

        if done:
            # update weights for the terminal state
            delta = reward - np.dot(w, phi)
            e = gamma*lam*e + phi
            w += alpha * delta * e
        else:
            # Non-terminal
            # choose next action
            a_prime = select_action(env, w, epsilon, next_player)
            # compute feature vector
            phi_prime = feature_extractor(next_state, a_prime, next_player)
            # compute the TD error
            delta = reward + gamma * np.dot(w, phi_prime) - np.dot(w, phi)
            # update eligibility traces
            e = gamma*lam*e + phi
            # update weight 
            w += alpha * delta * e

            # Move forward with the next state action pair
            state = next_state
            a = a_prime
            player = next_player
    if (episode + 1) % 100 == 0:
        print(f"Processed {episode + 1} episodes.")

np.save("weights.npy", w)
