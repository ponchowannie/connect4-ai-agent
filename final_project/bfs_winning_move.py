from collections import deque

ROWS = 6
COLS = 7

def is_valid_position(row, col):
    if row >= 0 and row < ROWS:
        if col >= 0 and col < COLS:
            return True
    return False

def check_winning_condition(board, row, col, player_num):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    for dr, dc in directions:
        count = 1
        for i in range(1, 4):
            next_row = row + (i * dr)
            next_col = col + (i * dc)
            if is_valid_position(next_row, next_col) and board[next_row][next_col] == player_num:
                count += 1
            else:
                break
        if count == 4:
            return True
    return False

def winning_move(board, player_num):
    queue = deque()

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player_num:
                queue.append((row, col))

    while queue:
        row, col = queue.popleft()
        if check_winning_condition(board, row, col, player_num):
            return 1
    return 0