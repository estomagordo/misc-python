from itertools import permutations
from copy import copy

def get_pawn_row():
    return ['P' for x in xrange(8)]
    
def get_empty_row():
    return [' ' for x in xrange(8)]

def build_board(configuration):
    return map(lower, list(configuration)) + map(lower, get_pawn_row()) + get_empty_row() * 4 + get_pawn_row() + list(configuration)
    
def all_black_moves(state):
    moves = []
    first_move = all(state[1][col] == 'p' for col in xrange(8))    
    
    for col in xrange(8):
        if first_move:
            if state[1][col] == 'p':
                if state[2][col] == ' ':
                    new_state = copy(state)
                    new_state[2][col] = 'p'
                    new_state[1][col] = ' '
                    moves.append(new_state)
                    # if state[3][col] == ' ':
                        # new_state = copy(state)
                        # new_state[3][col] = 'p'
                        # new_state[1][col] = ' '
                        # moves.append(new_state)    
        else:
            back_piece = state[0][col]
        
            if back_piece in 'bq':
                if col > 0 and state[1][col - 1] == ' ':
                    for dist in xrange(1, col + 1):
                        if state[dist][col - dist] != ' ':
                            break
                        new_state = copy(state)
                        new_state[dist][col - dist] = back_piece
                        new_state[0][col] = ' '
                        moves.append(new_state)
                if col < 7 and state[1][col + 1] == ' ':
                    for dist in xrange(1, col + 1):
                        if state[dist][col + dist] != ' ':
                            break
                        new_state = copy(state)
                        new_state[dist][col + dist] = back_piece
                        new_state[0][col] = ' '
                        moves.append(new_state)
    
    return moves
    
def all_white_moves(state):
    moves = []
    
    for col in xrange(8):
        if state[6][col] == 'P':
            if state[5][col] == ' ':
                new_state = copy(state)
                new_state[5][col] = 'P'
                new_state[6][col] = ' '
                moves.append(new_state)
                if state[4][col] == ' ':
                    new_state = copy(state)
                    new_state[4][col] = 'P'
                    new_state[6][col] = ' '
                    moves.append(new_state)
            
    return moves

def white_mate(state):
    return white_checked(state) and white_stuck(state)

def mate_in_two(configuration):
    states = [build_board(configuration)]
    
    for move_count in xrange(4):
        new_states = []
        for state in states:
            if move_count % 2 == 0:
                new_states += all_white_moves(state)
            else:
                new_states += all_black_moves(state)
        states = new_states
        
    return any(white_mate(state) for state in states)

def order_valid(order):
    rook_count = 0
    king_valid = True
    blackbish = False
    whitebish = False
    
    for x in xrange(len(order)):
        c = order[x]
        
        if c == 'K':
            king_valid = rook_count == 1
        if c == 'R':
            rook_count += 1
        if c == 'B':
            if x % 2 == 0:
                blackbish = True
            else:
                whitebish = True
                
    return king_valid and blackbish and whitebish

mate_count = 0
variant_count = 0
backpieces = 'KQRRNNBB'

for p in permutations(backpieces):
    if order_valid(p):
        mate_count += mate_in_two(p)
        
    variant_count += 1
    
    print mate_count, '/', variant_count