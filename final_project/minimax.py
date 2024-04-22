from utility import *
from bfs_winning_move import *
from genetic_algorithm_bomb import *
import math

DEBUG = False

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