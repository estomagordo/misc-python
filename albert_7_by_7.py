from sys import argv
from itertools import combinations

def multiply_between(start, end):
    return reduce(lambda x,y: x*y, range(start, end+1))

tiles = [x for x in xrange(49) if not x in [0,6,42,48]]

setlist = [set([x, x+6, x+7, x+8, x+14]) for x in xrange(35) if not x%7 in [0,6]]
    
def look_for_of_size(n):
    maxperms = multiply_between(46-n, 45) / multiply_between(2, n)
    count = 0
    working = []
    
    for c in combinations(tiles, n):
        if all(any(x in s for x in c) for s in setlist):
            working.append(c)
        count += 1
        if count % 10000 == 0:
            print '%0.2f' % (100.0 * float(count) / float(maxperms)) + '%'
            
    return working
        
if __name__ == '__main__':
    n = int(argv[1])
    working = look_for_of_size(n)
    print working
    print len(working)