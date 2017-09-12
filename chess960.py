from itertools import permutations

def mate_in_two(configuration):


def order_valid(order):
    

mate_count = 0
backpieces = 'KQRRNNBB'

for p in permutations(backpieces):
    if order_valid(p):
        mate_count += mate_in_two(p)