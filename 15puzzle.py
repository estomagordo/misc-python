from sys import stdin
from heapq import heappop, heappush

goal = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)

def is_odd(state):
    count = 0
    seen = set()
    for x in xrange(16):
        number = state[x]
        if number == 0:
            count += 3 - x/4
            continue
        count += sum(1 for x in xrange(1,number) if not x in seen)
        seen.add(number)
    return count%2

def distance(position, number):
    if number == 0:
        return 0

    return abs(position/4 - (number-1)/4) + abs(position%4 - (number-1)%4)

def heuristic(state):
    return sum(distance(x, state[x]) for x in xrange(16))

def get_moves(state):
    zeropos = -1
    for x in xrange(16):
        if state[x] == 0:
            zeropos = x
            break
    zerorow = zeropos/4
    zerocol = zeropos%4
    statlist = list(state)

    possibilities = []
    if zerorow > 0:
        possibilities.append(statlist[:zeropos-4] + [0] + statlist[zeropos-3:zeropos] + [statlist[zeropos-4]] + statlist[zeropos+1:])
    if zerorow < 3:
        possibilities.append(statlist[:zeropos] + [statlist[zeropos+4]] + statlist[zeropos+1:zeropos+4] + [0] + statlist[zeropos+5:])
    if zerocol > 0:
        possibilities.append(statlist[:zeropos-1] + [0] + [statlist[zeropos-1]] + statlist[zeropos+1:])
    if zerocol < 3:
        possibilities.append(statlist[:zeropos] + [statlist[zeropos+1]] + [0] + statlist[zeropos+2:])

    return map(tuple, possibilities)

def format_state(state):
    return '\n'.join(' '.join(str(state[4*y+x]) for x in xrange(4)) for y in xrange(4))

def print_trace(predecessors, state):
    trace = [state]
    predecessor = predecessors[state]
    while predecessor:
        trace.append(predecessor)
        predecessor = predecessors[predecessor]

    print '\n' + str(len(trace)-1) + ' moves\n\n' + '\n\n'.join(format_state(state) for state in trace[::-1])

def solve(state):
    if is_odd(state):
        print 'Impossible'
        return

    predecessors = {}

    seen = set()
    frontier = [(heuristic(state), 0, tuple(state), ())]
    while True:
        score, gone, state, predecessor = heappop(frontier)
        predecessors[state] = predecessor
        if state == goal:
            print_trace(predecessors, state)
            break

        seen.add(state)

        for new_state in get_moves(state):
            if not new_state in seen:
                heappush(frontier, (gone+1+heuristic(new_state), gone+1, new_state, state))

state = []
for x in xrange(4):
    state.extend(map(int, stdin.readline().split()))

solve(state)