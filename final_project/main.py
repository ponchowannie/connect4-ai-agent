import random
import math
from utility import *
from bfs_winning_move import *
from genetic_algorithm_bomb import GeneticAlgorithm, fitness_function
from minimax import minimax

# #   DO MOT TOUCH   # #
ROWS = 6
COLS = 7
game_over = False
DEBUG = False
itr = 0
# #   DO MOT TOUCH   # #


# # #   G A M E  S E T T I N G S   # # #
# #
# random.seed(6) # draw
generations = 10
turn = random.randint(0,1)
A_BOMB = 1 # SET TO "0" IF NOT ALLOW BOMBS
B_BOMB = 1 # SET TO "0" IF NOT ALLOW BOMBS
# #
# # #   G A M E  S E T T I N G S   # # #


# # #   G A M E    I N I T I A L I Z I N G   # # # 
# #
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
        
        # Genetic Algorithm for Bomb Placement
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

        # Genetic Algorithm for Bomb Placement
        ga = GeneticAlgorithm(population_size=28, chromosome_length=7, crossover_rate=0.6, mutation_rate=0.2)
        bomb_choice = ga.evolve(fitness_function, generations, board, opp_num=1)
        if bomb_choice and B_BOMB:
            print_board(board)
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