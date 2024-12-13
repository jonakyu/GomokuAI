import numpy as np

def feature_extractor(state, action, player):
    # player: 1 = X, 2 = O
    opponent = 3 - player
    board_size = state.shape[0]
    r, c = action

    # create a temp board
    temp_state = state.copy()
    temp_state[r, c] = player

    features = np.zeros(100)

    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    # count the number of consecutive stones
    def count_line(rr, cc, dr, dc, plr, board):
        count = 1
        # Forward direction
        step = 1
        while True:
            nr, nc = rr + dr * step, cc + dc * step
            if 0 <= nr < board_size and 0 <= nc < board_size and board[nr, nc] == plr:
                count += 1
                step += 1
            else:
                break
        # Backward direction
        step = 1
        while True:
            nr, nc = rr - dr * step, cc - dc * step
            if 0 <= nr < board_size and 0 <= nc < board_size and board[nr, nc] == plr:
                count += 1
                step += 1
            else:
                break
        return count

    # get detailed line info: total stones and if either ends are open
    def line_details(rr, cc, dr, dc, plr, board):
        # forward
        forward_stones = 0
        step = 1
        while True:
            nr, nc = rr + dr * step, cc + dc * step
            if 0 <= nr < board_size and 0 <= nc < board_size and board[nr, nc] == plr:
                forward_stones += 1
                step += 1
            else:
                forward_end_r, forward_end_c = nr, nc
                break

        # backward
        backward_stones = 0
        step = 1
        while True:
            nr, nc = rr - dr * step, cc - dc * step
            if 0 <= nr < board_size and 0 <= nc < board_size and board[nr, nc] == plr:
                backward_stones += 1
                step += 1
            else:
                backward_end_r, backward_end_c = nr, nc
                break

        total_stones = forward_stones + backward_stones + 1  # +1 for the placed stone
        forward_end_open = (0 <= forward_end_r < board_size and 0 <= forward_end_c < board_size 
                            and board[forward_end_r, forward_end_c] == 0)
        backward_end_open = (0 <= backward_end_r < board_size and 0 <= backward_end_c < board_size 
                             and board[backward_end_r, backward_end_c] == 0)

        return total_stones, forward_end_open, backward_end_open

    # --- Player's patterns ---
    for (dr, dc) in directions:
        line_count = count_line(r, c, dr, dc, player, temp_state)
        total_stones, forward_end_open, backward_end_open = line_details(r, c, dr, dc, player, temp_state)

        # Feature [0]: Immediate win (≥5 in a row)
        if line_count >= 5:
            features[0] = 1

        # Feature [1]: Player open four - exactly 4 stones with both ends open
        if total_stones == 4 and forward_end_open and backward_end_open:
            features[1] = 1

        # Feature [2]: Player open three - exactly 3 stones with both ends open
        if total_stones == 3 and forward_end_open and backward_end_open:
            features[2] = 1

    # Feature [3]
    # check if the placing of the stone stops the opponent from winning
    temp_test = state.copy()
    temp_test[r, c] = opponent
    opp_wins = False
    for (dr, dc) in directions:
        opp_line_count = count_line(r, c, dr, dc, opponent, temp_test)
        if opp_line_count >= 5:
            opp_wins = True
            break
    if opp_wins:
        features[3] = 1

    # Feature [4] and Feature [5]: Prevent opponenet's open patterns with 3 and 4 stones
    # Leaving those patterns must lead to the player's defeat
    temp_opponent = state.copy()
    temp_opponent[r, c] = opponent
    for (dr, dc) in directions:
        opp_total_stones, opp_forward_open, opp_backward_open = line_details(r, c, dr, dc, opponent, temp_opponent)

        # Feature [4]: Opponent open four (if opponent placing here would lead to open four)
        if opp_total_stones == 4 and opp_forward_open and opp_backward_open:
            features[4] = 1

        # Feature [5]: Opponent open three (if opponent placing here would lead to open three)
        if opp_total_stones == 3 and opp_forward_open and opp_backward_open:
            features[5] = 1
    # Feature [6]
    # Encourages placing stones in the middle since it has more potentail for expansion
    center = board_size // 2
    dist_from_center = max(abs(r - center), abs(c - center))
    max_dist = center  # max distance from center to an edge
    # the closer to the center hte more value it has
    centrality_value = 1.0 - (dist_from_center / max_dist)
    features[6] = centrality_value

    return features
