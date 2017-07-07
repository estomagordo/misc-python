from sys import argv

def pyramid(n):
    return (n**3 - n) / 6

def pyramidal_to(n):
    pyramidals = []
    p = 2
    pyramidal = pyramid(p)
    
    while pyramidal <= n:
        pyramidals.append(pyramidal)
        p += 1
        pyramidal = pyramid(p)
        
    return pyramidals
    
def pyramidal_sums_to(n):
    sums = [-1 for x in xrange(n+1)]
    sums[0] = 0
    pyramidals = pyramidal_to(n)
    found = 0
    
    step = 0
    while found < n:
        for x in xrange(n):
            if sums[x] == step:
                for pyramidal in pyramidals:
                    total = x + pyramidal
                    if total > n:
                        break
                    if sums[total] == -1:
                        found += 1
                        sums[total] = step+1
                        
        step += 1
        
    return step-1, sums
    
if __name__ == '__main__':
    num = int(argv[1])
    max_steps, result = pyramidal_sums_to(num)
    print max_steps if sum(n == 0 for n in result) == 1 else 'Failure!'