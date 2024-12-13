import tkinter as tk
from GomokuEnv import GomokuEnv
from players import HumanPlayer, AIPlayer, SimpleAdjacentPlayer

class GomokuGUI:
    def __init__(self, root, player1, player2, board_size=15, cell_size=30):
        self.root = root
        self.env = GomokuEnv(board_size=board_size)
        self.player1 = player1
        self.player2 = player2
        self.board_size = board_size
        self.cell_size = cell_size
        self.canvas_size = board_size * cell_size
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="light yellow")
        self.canvas.pack()

        
        self.game_over = False

        self.info_frame = tk.Frame(root)
        self.info_frame.pack()
        self.player_info_label = tk.Label(self.info_frame, text=f"Player 1: Black ({type(self.player1).__name__}) | Player 2: White ({type(self.player2).__name__})", font=("Arial", 14))
        self.player_info_label.pack()
        self.turn_label = tk.Label(self.info_frame, text="Turn: Player 1 (Black)", font=("Arial", 14, "bold"))
        self.turn_label.pack()

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.human_move)
        self.check_ai_move()

    def draw_grid(self):
        for i in range(self.board_size):
            # Vertical lines
            self.canvas.create_line(i * self.cell_size, 0, i * self.cell_size, self.canvas_size)
            # Horizontal lines
            self.canvas.create_line(0, i * self.cell_size, self.canvas_size, i * self.cell_size)

    def human_move(self, event):
        if self.game_over:
            return

        current_player = self.env.current_player
        player = self.get_current_player()

        # only take the clicks if humans turn
        if not isinstance(player, HumanPlayer):
            return

        row = event.y // self.cell_size
        col = event.x // self.cell_size

        if (row, col) not in self.env.get_available_actions():
            return

        # place a stone if the human move is valid
        self.place_stone(row, col)

    def place_stone(self, row, col):
        # determine the turn
        moving_player = self.env.current_player
        # execute the move
        state, reward, done, info = self.env.step((row, col))

        # draw the moving player's stone
        self.draw_stone(row, col, moving_player)

        if not done:
            next_player = "Player 1 (Black)" if self.env.current_player == 1 else "Player 2 (White)"
            self.turn_label.config(text=f"Turn: {next_player}")
        if done:
            # Game over (win or draw)
            self.game_over = True
            self.show_result(info)
        else:
            # check if it's ai's turn
            self.check_ai_move()

    def draw_stone(self, row, col, player):
        # graphically represent the stone
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 2
        color = "black" if player == 1 else "white"
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def show_result(self, info):
        winner = info.get("winner")
        if winner == 1:
            message = "Player 1 (black) wins!"
        elif winner == 2:
            message = "Player 2 (white) wins!"
        else:
            message = "It's a draw!"

        print(message)
        self.canvas.create_text(self.canvas_size // 2, self.canvas_size // 2, text=message, font=("Arial", 24), fill="red")

    def get_current_player(self):
        return self.player1 if self.env.current_player == self.player1.player_id else self.player2

    def check_ai_move(self):
        if self.game_over:
            return  # No moves needed if the game is over

        player = self.get_current_player()

        if isinstance(player, HumanPlayer):
            return
        else:
            # place ai's stone after 100ms
            self.root.after(100, self.ai_move, player)

    def ai_move(self, player):
        if self.game_over:
            return

        action = player.select_action(self.env)
        if action is None:
            # No available moves, possibly a draw, but this should be handled by env anyway
            return

        # place ai or simpleadjacent's player's move
        row, col = action
        self.place_stone(row, col)
