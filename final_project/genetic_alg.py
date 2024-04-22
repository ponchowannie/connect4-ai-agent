import numpy as np
import copy
import random

ROWS = 6
COLS = 7

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = None
        self.row = None
        self.col = None

class GeneticAlgorithm:
    def __init__(self, population_size, chromosome_length, crossover_rate, mutation_rate):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.population = [Individual([random.random() for _ in range(COLS)]) for _ in range(population_size)]

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            CUTOFF = 4
            child1 = []
            child2 = []

            for j in range(CUTOFF):
                child1.append(parent1.chromosome[j])
                child2.append(parent1.chromosome[j])

            for j in range(CUTOFF, COLS):
                child1.append(parent2.chromosome[j])
                child2.append(parent2.chromosome[j])

            return Individual(child1), Individual(child2)
        else:
            return parent1, parent2

    def mutate(self, individual):
        if random.random() < self.mutation_rate:
            mutation_point = random.randint(0, self.chromosome_length-1)
            individual.chromosome[mutation_point] = random.random()
        return individual
    
    def select_parents(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        selected_parents = [self.population[i] for i in range(self.population_size)]
        return selected_parents

    def evolve(self, fitness_function, generations, board, opp_num):
        best_fitness = 0
        threshold_fitness = 100

        for generation in range(generations):
            for individual in self.population:
                individual.fitness, row, col = fitness_function(individual.chromosome, board, opp_num)
                individual.row = row
                individual.col = col

            self.population.sort(key=lambda x: x.fitness, reverse=True)
            # print("Generation:", generation, "Best Fitness:", self.population[0].fitness)
            if self.population[0].fitness >= threshold_fitness:
                best_fitness = self.population[0].fitness
                best_choice = self.population[0].row, self.population[0].col

            # EDIT, MUTATE AND EVERYTHING FOR THE NEXT GEN
            selected_parents = self.select_parents()
            new_population = []
            for i in range(0, self.population_size, 2):
                parent1, parent2 = selected_parents[i], selected_parents[i+1]
                child1, child2 = self.crossover(parent1, parent2)
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)
                new_population.extend([child1, child2])
            self.population = new_population
        if best_fitness > 0:
            return best_choice
        else:
            return None

def get_open_row(board, col):
    for row in range(ROWS-1, -1, -1):
        if board[row][col] == 0:
            return row 

def fitness_function(chromosome, board, opp_num):
    max_col_index = chromosome.index(max(chromosome))
    sim_board = copy.deepcopy(board)
    bomb_row = get_open_row(board, max_col_index)
    if bomb_row == None:
        return -10000, None, None

    original_score = evaluate_board(board=board, opponent_num=opp_num)

    sim_board[bomb_row][max_col_index] = 0
    available_bomb_row = min(5, bomb_row+1)
    sim_board[available_bomb_row][max_col_index] = 0
    sim_score = evaluate_board(board=sim_board, opponent_num=opp_num)

    return (sim_score - original_score), available_bomb_row, max_col_index

def evaluate_board(board, opponent_num):
    score = 0
    for col in range(COLS - 3):  # horizontally
        for row in range(ROWS):
            window = [board[row][col], board[row][col + 1], board[row][col + 2], board[row][col + 3]]
            score += evaluate_window(window, opponent_num, window_type=1)

    for col in range(COLS):  # vertically
        for row in range(ROWS - 3):
            window = [board[row][col], board[row + 1][col], board[row + 2][col], board[row + 3][col]]
            score += evaluate_window(window, opponent_num, window_type=1)

    for col in range(COLS - 3):  # (down-right)
        for row in range(3, ROWS):
            window = [board[row][col], board[row - 1][col + 1], board[row - 2][col + 2], board[row - 3][col + 3]]
            score += evaluate_window(window, opponent_num)

    for col in range(3, COLS):  # (down-left)
        for row in range(3, ROWS):
            window = [board[row][col], board[row - 1][col - 1], board[row - 2][col - 2], board[row - 3][col - 3]]
            score += evaluate_window(window, opponent_num)
    return score

def evaluate_window(window, opponent_num, window_type=None):
    if opponent_num == 1:
        player_num = 2
    else:
        player_num = 1
    score = 0
    if window.count(opponent_num) == 3 and window.count(0) == 1:
        score -= 100  # Opponent has 3 pieces with an empty space
        if window_type: score -= 100
    elif window.count(opponent_num) == 2 and window.count(0) == 2:
        score -= 10  # Opponent has 2 pieces with 2 empty spaces
    if window.count(player_num) == 3 and window.count(0) == 1:
        score += 100  # Player has 3 pieces with an empty space
        if window_type: score += 100
    elif window.count(player_num) == 2 and window.count(0) == 2:
        score += 10  # Player has 2 pieces with 2 empty spaces
    return score



# population_size = 28
# chromosome_length = 7
# crossover_rate = 0.8
# mutation_rate = 0.1
# generations = 10
