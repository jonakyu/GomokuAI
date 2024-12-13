import tkinter as tk
from GomokuGUI import GomokuGUI
from players import HumanPlayer, AIPlayer, SimpleAdjacentPlayer

class ModeSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku: Select Mode")

        btn_human_vs_human = tk.Button(root, text="Human vs. Human", command=self.start_human_vs_human, width=25, height=2)
        btn_human_vs_ai = tk.Button(root, text="Human vs. AI", command=self.start_human_vs_ai, width=25, height=2)
        btn_ai_vs_ai = tk.Button(root, text="AI vs. AI", command=self.start_ai_vs_ai, width=25, height=2)
        btn_ai_vs_simple = tk.Button(root, text="AI vs. SimpleAdjacentPlayer", command=self.start_ai_vs_simple, width=25, height=2)
        btn_human_vs_simple = tk.Button(root, text="Human vs. SimpleAdjacentPlayer", command=self.start_human_vs_simple, width=25, height=2)

        btn_human_vs_human.pack(pady=10)
        btn_human_vs_ai.pack(pady=10)
        btn_ai_vs_ai.pack(pady=10)
        btn_ai_vs_simple.pack(pady=10)
        btn_human_vs_simple.pack(pady=10)

    def start_human_vs_human(self):
        self._start_game(HumanPlayer(1), HumanPlayer(2))

    def start_human_vs_ai(self):
        self._start_game(HumanPlayer(1), AIPlayer(2, weights_path="weights.npy"))

    def start_ai_vs_ai(self):
        self._start_game(AIPlayer(1, weights_path="weights.npy"), AIPlayer(2, weights_path="weights.npy"))

    def start_ai_vs_simple(self):
        self._start_game(AIPlayer(1, weights_path="weights.npy"), SimpleAdjacentPlayer(2))

    def start_human_vs_simple(self):
        self._start_game(HumanPlayer(1), SimpleAdjacentPlayer(2))

    def _start_game(self, player1, player2):
        self.root.destroy()

        game_root = tk.Tk()
        game_root.title("Gomoku")
        gui = GomokuGUI(game_root, player1=player1, player2=player2)
        game_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModeSelector(root)
    root.mainloop()
