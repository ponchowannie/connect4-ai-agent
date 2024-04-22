import random

ROWS = 6
COLS = 7

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
