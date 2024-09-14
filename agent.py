import random

def evaluate(player, Grid, GridSize, check_winner):
    # Check if there is a win
    if check_winner(player):
        if player == 3:  # AI wins
            return 100  # Very high score for AI win
        elif player == 1:  # Player wins
            return -100  # Very low score for Player 1 win

    # Heuristic: reward consecutive pieces for AI and penalize for player
    ai_score = 0
    player_score = 0

    for row in range(GridSize):
        for col in range(GridSize):
            if Grid[row][col] == 3:  # AI's pieces
                ai_score += count_consecutive_pieces(3, row, col, Grid, GridSize)
            elif Grid[row][col] == 1:  # Player 1's pieces
                player_score += count_consecutive_pieces(1, row, col, Grid, GridSize)

            if count_consecutive_pieces(1, row, col, Grid, GridSize) >= 3:
                return -100  # Heavy penalty if player is about to win

    return ai_score - 2 * player_score  

def count_consecutive_pieces(player, row, col, Grid, GridSize):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)] 
    score = 0
    for dr, dc in directions:
        consecutive = 0
        for i in range(5): 
            r, c = row + dr * i, col + dc * i
            if 0 <= r < GridSize and 0 <= c < GridSize and Grid[r][c] == player:
                consecutive += 1
            else:
                break

        if consecutive >= 5:  # Winning line detected
            score += 100  
        elif consecutive == 4:  
            score += 50  
        elif consecutive == 3:
            score += 10 
    return score

def center_heuristic(row, col, GridSize):
    center = GridSize // 2
    return -(abs(row - center) + abs(col - center))  

def minimax(Grid, GridSize, depth, is_maximizing, alpha, beta, check_winner, max_depth=2):
    if depth >= max_depth:
        return 0  

    score = evaluate(3, Grid, GridSize, check_winner) 
    if score == 1:
        return score - depth  
    if score == -1:
        return score + depth 

    # Check for draw (no more moves)
    if all(Grid[row][col] != 0 for row in range(GridSize) for col in range(GridSize)):
        return 0  # Draw

    if is_maximizing:
        best = -float('inf')
        for row in range(GridSize):
            for col in range(GridSize):
                if Grid[row][col] == 0: 
                    Grid[row][col] = 3  
                    move_value = minimax(Grid, GridSize, depth + 1, False, alpha, beta, check_winner, max_depth)
                    move_value += center_heuristic(row, col, GridSize)  
                    Grid[row][col] = 0  # Undo move
                    best = max(best, move_value)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break  
        return best
    else:
        best = float('inf')
        for row in range(GridSize):
            for col in range(GridSize):
                if Grid[row][col] == 0:  
                    Grid[row][col] = 1  
                    move_value = minimax(Grid, GridSize, depth + 1, True, alpha, beta, check_winner, max_depth)
                    move_value += center_heuristic(row, col, GridSize)
                    Grid[row][col] = 0 
                    best = min(best, move_value)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break  
        return best

def find_best_move(Grid, GridSize, check_winner, ani_progress, max_depth=3):
    best_move = None
    best_value = -float('inf')


    for row in range(GridSize):
        for col in range(GridSize):
            if Grid[row][col] == 0:  
                Grid[row][col] = 3  
                move_value = minimax(Grid, GridSize, 0, False, -float('inf'), float('inf'), check_winner, max_depth)
                move_value += center_heuristic(row, col, GridSize)  
                Grid[row][col] = 0  

                if move_value > best_value:
                    best_value = move_value
                    best_move = (row, col)

    if best_move:
        row, col = best_move
        Grid[row][col] = 3  
        ani_progress[(row, col)] = 0 
        print(f"AI placed O at row {row}, col {col} with score {best_value}")
        return check_winner(3)  # Check if AI won
    return False
