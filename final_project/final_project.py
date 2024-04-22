import random
import math
import copy
from utility import *
from bfs_winning_move import *
from genetic_alg import Individual, GeneticAlgorithm, fitness_function

ROWS = 6
COLS = 7

def create_board():
    board = [[0]*COLS for _ in range(ROWS)]
    return board

# cases for invalid choice
def is_column_full(board, col):
    if board[0][col] == 0:
        return 0 # False is returned for not full
    return 1 # True is returned for full

def get_open_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == 0:
            return row # returns the height index to be placed

# terminal case
def is_terminal_case(board):
    if winning_move(board, 1) or winning_move(board, 2) or get_valid_location(board) == 0:
        return 1
    else:
        return 0

# get valid locations
def get_valid_location(board):
    valid_locations = []
    for col in range(COLS):
        if not is_column_full(board, col):
            valid_locations.append(col)
    return valid_locations

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
        # 3 is center col
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

def drop_coin(board, row, col, player_num):
    board[row][col] = player_num

def minimax(board, depth, alpha, beta, is_max_player):
    if DEBUG:
        print(f'\n------\n')
        print_board(board)

    valid_locations = get_valid_location(board)
    
    is_terminal = is_terminal_case(board)

    if is_terminal or valid_locations == []:
        if winning_move(board, 2):
            if DEBUG: print(f'Move Win')
            return None, 1000000 # This Agent Wins
        elif winning_move(board, 1): 
            if DEBUG: print(f'Move Lose')
            return None, -1000000 # This Agent Loses
        else:
            return None, 0 # Draw
        
    if depth == 0:
        if is_max_player: # Was called for max_player but max depth reached, so evaluate for min
            if DEBUG: print(f'Score Min: {heuristic_board_played(board, 1)}')
            return None, heuristic_board_played(board, 1)
        if not is_max_player:
            if DEBUG: print(f'Score Max: {heuristic_board_played(board, 2)}')
            return None, heuristic_board_played(board, 2)
    
    if is_max_player:
        value = -math.inf
        column = random.choice(valid_locations)
        if DEBUG: print(f'Valid Locations: {valid_locations}')
        for col in valid_locations:
            row = get_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_coin(temp_board, row, col, 2)
            new_score = minimax(temp_board, depth-1, alpha, beta, False)[1]
            if DEBUG: print(f'\n------\nChoice: {col}\nScore: {new_score}')
            
            if new_score > value:
                value = new_score
                column = col
            
            alpha = max(value, alpha)
            if alpha >= beta:
                if DEBUG: print(f'MaxPlayer - Alpha > Beta: {alpha}, {beta}')
                break
        return column, value
    
    else: # for thte minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_open_row(board, col)
            temp_board = copy.deepcopy(board)
            drop_coin(temp_board, row, col, 1)
            new_score = minimax(temp_board, depth-1, alpha, beta, True)[1]

            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta) 
            if alpha >= beta:
                if DEBUG: print(f'Alpha > Beta: {alpha}, {beta}')
                break
        return column, value


# Parameters
CENTER_COL_SCORE = 6
generations = 10
#

# random.seed(6) # draw

#
game_over = False
turn = 0
DEBUG = False
itr = 0
A_BOMB = 1 # SET TO "0" IF NOT ALLOW BOMBS
B_BOMB = 1 # SET TO "0" IF NOT ALLOW BOMBS
#

# # #   G A M E    I N I T I A L I Z I N G   # # # 
board = create_board()
board = gen_blocked_space(board, 2)


print("\n\n")
print_board(board)

while not game_over:
    itr += 1
    print("."*itr)
    
    if is_board_full(board):
        print_draw()
        print_board(board)
        game_over = True
        continue

    # X's Turn
    if turn == 0:
        if DEBUG:
            col = int(input("Player's turn (1-7):"))
            col -= 1
        
        # Genetic Algorithm for Bomb
        ga = GeneticAlgorithm(population_size=28, chromosome_length=7, crossover_rate=0.8, mutation_rate=0.1)
        bomb_choice = ga.evolve(fitness_function, generations, board, opp_num=2)
        if bomb_choice and A_BOMB:
            print_board(board)
            print(bomb_choice)
            board[bomb_choice[0]][bomb_choice[1]] = 0
            print('A USED BOMB!!', f'ON ROW: {6-bomb_choice[0]}, COL:{bomb_choice[1]+1}')
            print_board(board)
            A_BOMB = 0

        col, minimax_score = minimax(board=board, depth=5, alpha=-math.inf, beta=math.inf, is_max_player=True)
        if not is_column_full(board, col):
            row = get_open_row(board, col)
            drop_coin(board, row, col, 1)
            if is_terminal_case(board):
                print_player_wins()
                game_over = True
                print_winning_board(board)
            turn = 1

    # O's Turn
    else:
        if DEBUG:
            print('------')
            print_board(board)
            print(col, minimax_score)

        # Genetic Algorithm for Bomb
        ga = GeneticAlgorithm(population_size=28, chromosome_length=7, crossover_rate=0.6, mutation_rate=0.2)
        bomb_choice = ga.evolve(fitness_function, generations, board, opp_num=1)
        if bomb_choice and B_BOMB:
            print_board(board)
            # print(bomb_choice)
            board[bomb_choice[0]][bomb_choice[1]] = 0
            print('B USED BOMB!!', f'ON ROW: {6-bomb_choice[0]}, COL:{bomb_choice[1]+1}')
            print_board(board)
            B_BOMB = 0

        col, minimax_score = minimax(board=board, depth=5, alpha=-math.inf, beta=math.inf, is_max_player=True)
        if not is_column_full(board, col):
            row = get_open_row(board, col)
            drop_coin(board, row, col, 2)
            if is_terminal_case(board):
                print_ai_wins()
                game_over = True
                print_winning_board(board)
            turn = 0