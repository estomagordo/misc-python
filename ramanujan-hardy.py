from sys import argv

def rh_less_than(n):
    numbers = set()

    for d in xrange(n-1, 0, -1):
        dcub = d**3
        for b in xrange(d-1, 0, -1):
            bcub = b**3
            for a in xrange(1, b):
                left = a**3 + bcub
                for c in xrange(1, d):
                    right = c**3 + dcub
                    if right >= left:
                        if right == left:
                            numbers.add(right)
                        break
                        
    return numbers
    
if __name__ == '__main__':
    n = int(argv[1])
    count = len(rh_less_than(n))
    print 'there are', count, 'Ramanujan-Hardy numbers where all term bases are less than ', n