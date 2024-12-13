import numpy as np
import os
import random
from feature_extractor import feature_extractor

class HumanPlayer:
    def __init__(self, player_id):
        self.player_id = player_id
    def select_action(self, env):
        return None

class AIPlayer:
    def __init__(self, player_id, weights_path="weights.npy"):
        self.player_id = player_id
        self.epsilon = 0.0  # No exploration during testing
        self.w = self.load_weights(weights_path)

    def load_weights(self, weights_path):
        if os.path.exists(weights_path):
            return np.load(weights_path)
        else:
            print(f"No weights found at {weights_path}.")
            return np.zeros(100)

    def select_action(self, env):
        actions = env.get_available_actions()
        if not actions:
            return None

        state = env._get_state()
        q_values = []
        for a in actions:
            # get q-value for each action
            phi = feature_extractor(state, a, self.player_id)
            q_values.append(np.dot(self.w, phi))

        # return the action with the highest q-value
        return actions[np.argmax(q_values)]

# simple adjacent player just placees a stone next to an existing stone
class SimpleAdjacentPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def select_action(self, env):
        # Try to pick a move adjacent to an existing stone
        actions = env.get_available_actions()
        if not actions:
            return None

        placed_stones = np.argwhere(env.board != 0)

        if placed_stones.size == 0:
            # choose a random action if there are no stones placed
            action = random.choice(actions)
            return action

        # position that this agaent can place stones
        candidate_moves = set()
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        for (r, c) in placed_stones:
            for (dr, dc) in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < env.board_size and 0 <= nc < env.board_size:
                    if env.board[nr, nc] == 0:
                        candidate_moves.add((nr, nc))

        # if there are many candidates choose one at random
        if candidate_moves:
            intersection = list(candidate_moves.intersection(actions))
            if intersection:
                chosen_action = random.choice(intersection)
                return chosen_action
        # If no adjacent moves found, pick random
        action = random.choice(actions)
        return action 
