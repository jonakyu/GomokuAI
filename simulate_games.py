import numpy as np
from GomokuEnv import GomokuEnv
from players import AIPlayer, SimpleAdjacentPlayer

import random

# below simulates a game between the trained AI agent and SimpleAdjacnet player
env = GomokuEnv()
ai_player = AIPlayer(player_id=1, weights_path="weights.npy")
simple_player = SimpleAdjacentPlayer(player_id=2)

num_games = 1000
ai_wins = 0

for _ in range(num_games):
    state = env.reset()
    done = False
    current_player = env.current_player

    while not done:
        if current_player == ai_player.player_id:
            action = ai_player.select_action(env)
        else:
            action = simple_player.select_action(env)

        next_state, reward, done, info = env.step(action)

        # check the winner
        if done:
            if info.get("winner") == ai_player.player_id:
                ai_wins += 1
        else:
            current_player = env.current_player
ai_win_percentage = (ai_wins) / num_games * 100
print(f"{num_games} games simulated - AI won ({ai_win_percentage:.2f}%).")
