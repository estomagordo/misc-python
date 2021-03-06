# Aims to probe every possible Fischer random chess, or Chess960 variant for possible fool's mate variants (mate by black in two).
# Uses a number of heuristics to speed up search, which allows it to doing expensive deepcopies as a core part of the algorithm, without the total runtime being too murderous.
# For one, the only black pieces that can threaten a white king positioned at the first row are bishops and the queen.
# A black knight can check a white king that has moved up one row. But in such occasions, after only two moves by either player, there is always safe ground for the white king, including its starting position.
# So this means that the only black moves considered are a pawn move, followed by the moving of a bishop or the queen. The distance covered by the pawn does not matter.
# White needs to move at least one pawn for its king to be threatened by a diagonally moving piece. It also turns out that since the diagonal threat would risk getting covered by a pawn otherwise,
# another pawn, having moved "ahead" of the diagional threat line is also moved by necessity. Reducing white's move schedule to two pawn moves.
# Note that this mean that the castling rules are irrelevant.

from itertools import permutations
from copy import deepcopy

def get_pawn_row():
    return ['P' for x in xrange(8)]
    
def get_empty_row():
    return [' ' for x in xrange(8)]

def build_board(configuration):
    return [map(lambda c: c.lower(), list(configuration))] + [map(lambda c: c.lower(), get_pawn_row())] + [get_empty_row()] + [get_empty_row()] + [get_empty_row()] + [get_empty_row()] + [get_pawn_row()] + [list(configuration)]
    
def all_black_moves(state):
    moves = []
    first_move = all(state[1][col] == 'p' for col in xrange(8))    
    
    for col in xrange(8):
        if first_move:
            if state[1][col] == 'p':
                if state[2][col] == ' ':
                    new_state = deepcopy(state)
                    new_state[2][col] = 'p'
                    new_state[1][col] = ' '
                    moves.append(new_state)
        else:
            back_piece = state[0][col]
        
            if back_piece in 'bq':
                if col > 0 and state[1][col - 1] == ' ':
                    for dist in xrange(1, col + 1):
                        if state[dist][col - dist] != ' ':
                            break
                        new_state = deepcopy(state)
                        new_state[dist][col - dist] = back_piece
                        new_state[0][col] = ' '
                        moves.append(new_state)
                if col < 7 and state[1][col + 1] == ' ':
                    for dist in xrange(1, 8 - col):
                        if state[dist][col + dist] != ' ':
                            break
                        new_state = deepcopy(state)
                        new_state[dist][col + dist] = back_piece
                        new_state[0][col] = ' '
                        moves.append(new_state)
    
    return moves
    
def all_white_moves(state):
    moves = []
    
    for col in xrange(8):
        if state[6][col] == 'P':
            if state[5][col] == ' ':
                new_state = deepcopy(state)
                new_state[5][col] = 'P'
                new_state[6][col] = ' '
                moves.append(new_state)
                if state[4][col] == ' ':
                    new_state = deepcopy(state)
                    new_state[4][col] = 'P'
                    new_state[6][col] = ' '
                    moves.append(new_state)
            
    return moves
    
def get_white_king_pos(state):
    for row in xrange(8):
        for col in xrange(8):
            if state[row][col] == 'K':
                return (row, col)
    
def get_checker(state):
    y, x = get_white_king_pos(state)
    
    for left_dist in xrange(1, x + 1):
        piece = state[y - left_dist][x - left_dist]
        if piece in 'bq':
            return (y - left_dist, x - left_dist)
        if piece != ' ':
            break
            
    for right_dist in xrange(1, 8 - x):
        piece = state[y - right_dist][x + right_dist]
        if piece in 'bq':
            return (y - right_dist, x + right_dist)
        if piece != ' ':
            break
            
    return (-1, -1)
    
def king_can_escape(state, king, checker):
    if state[king[0] - 1][king[1]] == ' ':
        return True
    if king[1] > checker[1]:
        if king[1] < 7 and state[king[0]][king[1] + 1] == ' ':
            return True
    else:
        if king[1] > 0 and state[king[0]][king[1] - 1] == ' ':
            return True
            
    return False
    
def checker_can_be_taken(state, king, checker, include_king = True):
    if include_king and abs(king[0] - checker[0]) < 2:
        return True
    if checker[1] > 0:
        if checker[0] < 7 and state[checker[0] + 1][checker[1] - 1] == 'P':
            return True
        if checker[0] < 6 and state[checker[0] + 2][checker[1] - 1] == 'N':
            return True
    if checker[1] < 7:
        if checker[0] < 7 and state[checker[0] + 1][checker[1] + 1] == 'P':
            return True
        if checker[0] < 6 and state[checker[0] + 2][checker[1] + 1] == 'N':
            return True
            
    return False
    
def checker_can_be_blocked(state, king, checker):
    if king[1] > checker[1]:
        for steps in xrange(1, king[1] - checker[1]):
            if checker_can_be_taken(state, king, (king[0] - steps, king[1] - steps), False):
                return True
    else:
        for steps in xrange(1, checker[1] - king[1]):
            if checker_can_be_taken(state, king, (king[0] - steps, king[1] + steps), False):
                return True
                
    return False
        
def white_stuck(state, checker):
    king = get_white_king_pos(state)
    
    if king_can_escape(state, king, checker):
        return False
    if checker_can_be_taken(state, king, checker):
        return False
    return not checker_can_be_blocked(state, king, checker)

def white_mate(state):
    checker = get_checker(state)
    
    if checker == (-1, -1):
        return False
        
    return white_stuck(state, checker)

def mate_in_two(configuration):
    states = [build_board(configuration)]
    
    for move_count in xrange(4):
        new_states = []
        for state in states:
            if move_count % 2 == 0:
                new_states += all_white_moves(state)
            else:
                new_states += all_black_moves(state)
        # if move_count == 0: print new_states
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
seen = set()

for p in permutations(backpieces):    
    if p in seen or not order_valid(p):
        continue
        
    seen.add(p)
        
    variant_count += 1
    mate_count += mate_in_two(p)
    print mate_count, '/', variant_count