import numpy as np

class GomokuEnv:
    def __init__(self, board_size=15):
        self.board_size = board_size
        self.board = None
        # Players: 1 = 'X', 2 = 'O'
        self.current_player = 1
        self.reset()

    def reset(self):
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        return self._get_state()

    def _get_state(self):
        return np.copy(self.board)

    def get_available_actions(self):
        return [(r, c) for r in range(self.board_size) 
                for c in range(self.board_size) 
                if self.board[r, c] == 0]

    def step(self, action):
        r, c = action
        # Place the stone for current_player
        self.board[r, c] = self.current_player

        if self.check_winner(r, c, self.current_player):
            # Current player wins, always give positive reward
            reward = 1.0
            info = {"winner": self.current_player}
            return self._get_state(), reward, True, info

        # Check for draw
        if len(self.get_available_actions()) == 0:
            return self._get_state(), 0.0, True, {"winner": None}  # no winner

        # if it's not a win or a draw switch the player
        self.current_player = 3 - self.current_player  # toggles 1 <-> 2
        return self._get_state(), 0.0, False, {}
    # defines the winning conditions
    def check_winner(self, row, col, player):
        directions = [(1,0), (0,1), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            # forward
            for step in range(1,5):
                r, c = row + dr*step, col + dc*step
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r,c] == player:
                    count += 1
                else:
                    break
            # backward
            for step in range(1,5):
                r, c = row - dr*step, col - dc*step
                if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r,c] == player:
                    count += 1
                else:
                    break
            # if more than 5 stones are placed in a row, it's over
            if count >= 5:
                return True
        return False
