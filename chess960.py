from itertools import permutations

def get_pawn_row():
    return ['P' for x in xrange(8)]
    
def get_empty_row():
    return [' ' for x in xrange(8)]

def build_board(configuration):
    return list(configuration) + get_pawn_row() + get_empty_row() * 4 + get_pawn_row() + list(configuration)

def mate_in_two(configuration):
    board = build_board(configuration)

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
backpieces = 'KQRRNNBB'

for p in permutations(backpieces):
    if order_valid(p):
        mate_count += mate_in_two(p)
        
print mate_count