import math

player, opponent = 'x', 'o'

# Check if there are any moves left by the fullness of the board
def is_moves_left(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '_': return True
    return False

# Evaluate if the game is in an end/win state or not
def evaluate(b):
    for row in range(len(b)):
        if len(set(b[row])) == 1:
            if b[row][0] == 'x': return 10
            elif b[row][0] == 'o': return -10
    
    for column in range(len(b)):
        if len(set([row[column] for row in b])) == 1:
            if b[0][column] == 'x': return 10
            elif b[0][column] == 'o': return -10

    if len(set([b[x][x] for x in range(len(b))])) == 1:
        if b[0][0] == 'x': return 10
        elif b[0][0] == 'o': return -10
    
    if len(set([b[len(b) - 1 - x][x] for x in range(len(b))])) == 1:
        if b[len(b) - 1][0] == 'x': return 10
        elif b[len(b) - 1][0] == 'o': return -10
    
    return 0

def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)

    # Ensure minimax tries to end the game with the minimum amount of moves needed
    if score == 10: return score - depth
    if score == -10: return score + depth

    if not is_moves_left(board): return 0
    
    if is_max:
        best = -math.inf
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == '_'):
                    board[i][j] = player
                    best = max(best,  minimax(board, depth + 1, is_max, alpha, beta))
                    board[i][j] = '_'
                    alpha = max(alpha, best)
                    if beta <= alpha: break
        return best
    
    else:
        best = math.inf
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == '_'):
                    board[i][j] = opponent
                    best = min(best,  minimax(board, depth + 1, not is_max, alpha, beta))
                    board[i][j] = '_'
                    beta = min(beta, best)
                    if beta <= alpha: break
        return best

# Find the best move for the 'x' based on current state of the board and possible states
def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '_':
                board[i][j] = player
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = '_'
                if (move_val > best_val):
                    best_move = (i, j)
                    best_val = move_val
    
    print("The value of the best Move is :", best_val)
    return best_move

def main():
    board = [
        ['o','o','x'],
        ['x','o','o'],
        ['_','_','x']
    ]

    best_move = find_best_move(board)

    print("The Optimal Move is:")
    print("ROW:", best_move[0], "COL:", best_move[1])

if __name__ == '__main__':
    main()