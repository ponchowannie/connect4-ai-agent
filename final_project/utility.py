import random
from bfs_winning_move import winning_move

ROWS = 6
COLS = 7
CENTER_COL_SCORE = 6

def print_player_wins():
    msg = """
 __  __ __        _____ _   _ ____  
 \ \/ / \ \      / /_ _| \ | / ___| 
  \  /   \ \ /\ / / | ||  \| \___ \ 
  /  \    \ V  V /  | || |\  |___) |
 /_/\_\    \_/\_/  |___|_| \_|____/
                                                                                                                             
    """
    print(msg)


def print_ai_wins():
    msg = """
   ___   __        _____ _   _ ____  
  / _ \  \ \      / /_ _| \ | / ___| 
 | | | |  \ \ /\ / / | ||  \| \___ \ 
 | |_| |   \ V  V /  | || |\  |___) |
  \___/     \_/\_/  |___|_| \_|____/ 
                                                                
    """
    print(msg)

def print_draw():
    msg = """
     ____  ____      ___        __
    |  _ \|  _ \    / \ \      / /
    | | | | |_) |  / _ \ \ /\ / / 
    | |_| |  _ <  / ___ \ V  V /  
    |____/|_| \_\/_/   \_\_/\_/  
    """
    print(msg)

def create_board():
    board = [[0]*COLS for _ in range(ROWS)]
    return board

def print_board(board):
    for i in board:
        print("|", end="")
        for j in i:
            if j == 0:
                print("   |", end="")
            elif j == 1:
                print(" X |", end="")
            elif j == 2:
                print(" O |", end="")
            elif j == -1:  # Blocked cell
                print(" B |", end="")
        print()
        print("+---+---+---+---+---+---+---+")
    print("  1   2   3   4   5   6   7\n\n")

def winning_board_location(board, player_num):
    for col in range(COLS - 3):  # horizontally
        for row in range(ROWS):
            if board[row][col] == player_num and board[row][col + 1] == player_num and board[row][col + 2] == player_num and board[row][col + 3] == player_num:
                return [[row, col], [row, col + 1], [row, col + 2], [row, col + 3]]

    for col in range(COLS):  # vertically
        for row in range(ROWS - 3):
            if board[row][col] == player_num and board[row + 1][col] == player_num and board[row + 2][col] == player_num and board[row + 3][col] == player_num:
                return [[row, col], [row + 1, col], [row + 2, col], [row + 3, col]]

    for col in range(COLS - 3):  # (down-right)
        for row in range(3, ROWS):
            if board[row][col] == player_num and board[row - 1][col + 1] == player_num and board[row - 2][col + 2] == player_num and board[row - 3][col + 3] == player_num:
                return [[row, col], [row - 1, col + 1], [row - 2, col + 2], [row - 3, col + 3]]

    for col in range(3, COLS):  # (down-left)
        for row in range(3, ROWS):
            if board[row][col] == player_num and board[row - 1][col - 1] == player_num and board[row - 2][col - 2] == player_num and board[row - 3][col - 3] == player_num:
                return [[row, col], [row - 1, col - 1], [row - 2, col - 2], [row - 3, col - 3]]
    return 0

def print_winning_board(board):
    if winning_board_location(board, 1):
        winning_positions = winning_board_location(board, 1)
    else:
        winning_positions = winning_board_location(board, 2)

    for row_index, row in enumerate(board):
        print("|", end="")
        for col_index, cell in enumerate(row):
            is_winning_position = [row_index, col_index] in winning_positions
            if is_winning_position:
                print("\033[31m", end="")  # Red color for winning move
            if cell == 0:
                print("   |", end="")
            elif cell == 1:
                print(" X |", end="")
            elif cell == 2:
                print(" O |", end="")
            elif cell == -1:  # Blocked cell
                print(" B |", end="")
            if is_winning_position:
                print("\033[0m", end="")  # Reset color
        print()
        print("+---+---+---+---+---+---+---+")
    print("  1   2   3   4   5   6   7\n\n")

def gen_blocked_space(board, amount):
    if amount is not None:
        for i in range(amount):        
            board[random.randint(1,5)][random.randint(0,6)] = -1 # Doesnt block highest row
    return board

def is_board_full(board):
    for i in range(7):
        if board[0][i] == 0 and board[0][i] != -1:
            return 0
    return 1

# cases for invalid choice
def is_column_full(board, col):
    if board[0][col] == 0:
        return 0 # False is returned for not full
    return 1 # True is returned for full

def get_open_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == 0:
            return row # returns the height index to be placed
        
def drop_coin(board, row, col, player_num):
    board[row][col] = player_num


# get valid locations
def get_valid_location(board):
    valid_locations = []
    for col in range(COLS):
        if not is_column_full(board, col):
            valid_locations.append(col)
    return valid_locations

# terminal case
def is_terminal_case(board):
    if winning_move(board, 1) or winning_move(board, 2) or get_valid_location(board) == 0:
        return 1
    else:
        return 0

# finding heuristics
def heuristic_window(window, player_num):
    if player_num == 1:
        opp_num = 2
    if player_num == 2:
        opp_num = 1
    
    score = 0
    count = window.count(player_num)
    empty_count = window.count(0)
    if count == 4:
        score += 100
    elif count == 3 and empty_count == 1:
        score += 20 
    elif count == 2 and empty_count == 2:
        score += 5
    
    if window.count(opp_num) == 3 and empty_count == 1:
        score -= 10
    return score
    
def heuristic_board_played(board, player_num):
    score = 0
    for row in board:
        if row[3] == player_num:
            score += CENTER_COL_SCORE

    # calculate heuristic scores of each window of 4
    # horizontally
    for row in board:
        for col in range(COLS-3):
            window = row[col:col+4]
            score += heuristic_window(window, player_num)

    # vertically
    for col in range(COLS):
        for row in range(ROWS-3):
            window = [board[row][col], board[row+1][col], board[row+2][col], board[row+3][col]]
            score += heuristic_window(window, player_num)
    
    # positive diagonal
    for row in range(3, ROWS):
        for col in range(COLS-3):
            window = [board[row-i][col+i] for i in range(4)]
            score += heuristic_window(window, player_num)
    
    # negative diagonal
    for row in range(3, ROWS):
        for col in range(3, COLS):
            window = [board[row-i][col-i] for i in range(4)]
            score += heuristic_window(window, player_num)

    return score