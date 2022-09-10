import math

player, opponent = 'x', 'o'

# Check if there are any moves left by the fullness of the board.
def is_moves_left(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == '_': return True
    return False

# Check if player has won and if so return the winner.
def has_player_won(b):
    for r in range(len(b)):
        if b[r][0] != '_' and len(set(b[r])) == 1: 
            return True, b[r][0]
    
    for c in range(len(b)):
        if b[0][c] != '_' and len(set([r[c] for r in b])) == 1: 
            return True, b[0][c]

    if b[0][0] != '_' and len(set([b[x][x] for x in range(len(b))])) == 1:
        return True, b[0][0]
    
    if b[len(b) - 1][0] != '_' and len(set([b[len(b) - 1 - x][x] for x in range(len(b))])) == 1:
        return True, b[len(b) - 1][0]
    
    return False, '_'

# Evaluate if the game is in an end/win state or not.
def evaluate(b):
    won, player = has_player_won(b)

    if won:
        if player == 'x': return 10
        elif player == 'o': return -10
    
    return 0

def minimax(board, depth, is_max, alpha, beta):
    score = evaluate(board)

    # Ensure minimax tries to end the game with the minimum amount of moves needed.
    if score == 10: return score - depth
    if score == -10: return score + depth

    if not is_moves_left(board): return 0
    
    if is_max:
        best = -math.inf
        for r in range(len(board)):
            for c in range(len(board)):
                if (board[r][c] == '_'):
                    board[r][c] = player
                    best = max(best,  minimax(board, depth + 1, not is_max, alpha, beta))
                    board[r][c] = '_'
                    alpha = max(alpha, best)
                    if beta <= alpha: break
        return best
    
    else:
        best = math.inf
        for r in range(len(board)):
            for c in range(len(board)):
                if (board[r][c] == '_'):
                    board[r][c] = opponent
                    best = min(best, minimax(board, depth + 1, not is_max, alpha, beta))
                    board[r][c] = '_'
                    beta = min(beta, best)
                    if beta <= alpha: break
        return best

# Find the best move for the player based on current state of the board and possible states.
def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == '_':
                board[r][c] = player
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[r][c] = '_'
                if (move_val > best_val):
                    best_move = (r, c)
                    best_val = move_val
    
    print('The value of the best move is :', best_val)
    return best_move

def generate_empty_board(length):
    board = [['_' for c in range(length)] for r in range(length)]
    return board

def prettify_board(board):
    string = ''
    for r in range(len(board)):
        string += str(board[r]) + '\n'
    string = string.strip()
    return string

def raw_to_array(raw):
    array = raw.replace('[','').replace(']','').replace('\'','').replace(' ','').split(',')
    return array

def raw_board_to_board(raw_board):
    flat_board = raw_to_array(raw_board)
    length = int(math.sqrt(len(flat_board)))
    board = generate_empty_board(length)

    for r in range(length):
        for c in range(length):
            board[r][c] = flat_board.pop(0)
    
    return board

def find_next_player(board):
    flat_board = raw_to_array(str(board))
    if flat_board.count('o') < flat_board.count('x'): return 'o'
    else: return 'x'

def find_next_best_move():
        raw_board = input('Enter a valid board: ')
        board = raw_board_to_board(raw_board)

        # Print the inputted state of the board.
        print('\nBoard inputted:\n\n' + prettify_board(board), '\n')

        # Print the optimal move.
        best_move = find_best_move(board)
        print('The Optimal Move is: ROW:', best_move[0], 'COL:', best_move[1], '\n')

        # Print the new state of the board after the optimal move.
        print('Board after the best move:\n')
        board[best_move[0]][best_move[1]] = find_next_player(board)
        print(prettify_board(board), '\n')
    
def play_against_ai():
    board = generate_empty_board(3)
    won, player = has_player_won(board)
    turn = 2

    while is_moves_left(board) and not won:
        if turn == 1:
            raw_player_move = input('Enter your move: ')
            player_input = raw_to_array(raw_player_move)
            
            r, c = '-1', '-1'
            if len(player_input) == 2:
                r, c = player_input

            while (not r.isnumeric() or not c.isnumeric() or 
                   int(r) >= len(board) or int(c) >= len(board) or
                   int(r) < 0 or int(c) < 0 or
                   board[int(r)][int(c)] != '_'):
                raw_player_move = input('Invalid move, please try again. Enter your move: ')
                player_input = raw_to_array(raw_player_move)
                r, c = '-1', '-1'
                
                if len(player_input) == 2:
                    r, c = player_input

            board[int(r)][int(c)] = find_next_player(board)
            turn = 2
        else:
            r, c = find_best_move(board)
            board[r][c] = find_next_player(board)
            turn = 1

        print('\nCurrent board state:\n\n' + prettify_board(board), '\n')
        won, player = has_player_won(board)
    
    if won:
        print('Player', player, 'has won!')
    else:
        print('The board has run out of moves!')

def main():
    board = [
        ['o','o','x'],
        ['x','_','o'],
        ['_','_','x']
    ]

    print('\n1. Input a board to find the best move for the opponent.')
    print('2. Start a game against the AI. \n')
    option = input('Select an option from the above: ')
    valid_options = {'1':0, '2':0}

    while option not in valid_options:
        print('Invalid option. Try again.')
        option = input('Select an option from the above: ')

    if option == '1': find_next_best_move()
    else: play_against_ai()

if __name__ == '__main__':
    main()