# GomokuAI
This project implements a Reinforcement Learning (RL) agent using SARSA(λ) with linear function approximation to play the game of Gomoku (https://en.wikipedia.org/wiki/Gomoku). The objective is to train an agent with RL that achieves a winning rate higher than 50% when played against a player with simple heuristics of randomly placing a stone adjacent to an existing stone at its turn.

## Introduction
Gomoku is a two-player strategy board game where players alternate placing black and white stones on a 15x15 grid. The objective of the game is to align 5 stones in a row without the opponent's stone(s) interrupting. The alignment could be fromed horizontally, vertically, or diagonally.

## Features
- **Environment:** A 15x15 Gomoku board environment (`GomokuEnv.py`) that manages state transitions, legal actions, and victory conditions.
- **RL Algorithm:** SARSA(λ) with linear function approximation for Q-value estimation.
- **Feature Extraction:** Domain-specific features that I could come up with and formulate, including immediate win detection, open threes, open fours, blocking opponent threats, and centrality advantage.
- **Players:**
  - `SimpleAdjacentPlayer`: Randomly places stones adjacent to existing stones.
  - `AIPlayer`: Uses learned weights to select moves.
  - `HumanPlayer`: Allows human input through a GUI.
- **Training and Evaluation:**
  - `train_rl.py`: Trains the agent and saves learned weights.
  - `simulate_games.py`: Tests and reports AI’s performance against the SimpleAdjacentPlayer (SAP).
- **GUI:** A Tkinter-based GUI (`GomokuGUI.py`) and a mode selector (`main.py`) that enables the following modes: Human vs. Human, Human vs. AI, AI vs. AI, AI vs. SAP, and Human vs. SAP

## Project Structure
```bash
.
├─ GomokuEnv.py          # Gomoku environment definition
├─ train_rl.py           # Training script (SARSA(λ) with linear approximation)
├─ feature_extractor.py  # Extracts features from domain knowledge of this game
├─ players.py            # Player classes - Human, AI, and SAP
├─ simulate_games.py     # Simulate multiple games for AI vs. SAP
├─ GomokuGUI.py          # GUI implementation for Gomoku
├─ main.py               # Mode selector
└─ README.md             # Readme file
