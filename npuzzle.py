import sys
import time


class NPuzzle(object):

    def __init__(self, n=3, state=[0, 1, 2, 3, 4, 5, 6, 7, 8]):
        self.n = n
        self.state = state
        self.parent = None
        self.parent_path = ""       # directional move from parent to child (UP, DOWN, LEFT, RIGHT)
        self.children = []
        self.cost = 0               # cost to reach this node

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def get_n(self):
        return self.n

    def set_parent(self, parent):
        self.parent = parent

    def set_parent_path(self, path):
        self.parent_path = path

    def add_child(self, child):
        self.children.append(child)

    def get_zero_index(self):
        return self.state.index(0)


def moves(board, n, zero):

    def switch(parent, i, j):
        child = list(parent)
        temp = child[i]
        child[i] = child[j]
        child[j] = temp

        return child

    boards = []

    # up
    if zero - n >= 0:
        boards.append(['UP', switch(board.get_state(), zero, zero - n)])
    # down
    if zero + n < len(board.get_state()):
        boards.append(['DOWN', switch(board.get_state(), zero, zero + n)])
    # left
    if zero % n != 0:
        boards.append(['LEFT', switch(board.get_state(), zero, zero - 1)])
    # right
    if zero % n != n - 1:
        boards.append(['RIGHT', switch(board.get_state(), zero, zero + 1)])

    return boards


def check(board):
    finished = [x for x in range(len(board.get_state()))]
    if board.get_state() == finished:
        return True
    else:
        return False


def path(start, finish):

    moves = []
    node = finish
    while node.get_state() != start.get_state():
        moves.append(node.parent_path)
        node = node.parent

    return moves[::-1]


def manhattan(board, n):

    state = board.get_state()

    def man(a, b, n):

        a_x = a % n
        b_x = b % n

        a_y = int(a/n)
        b_y = int(b/n)

        return abs(a_x - b_x) + abs(a_y - b_y)

    distance = 0
    for num in range(len(state)):
        pos = state.index(num)
        distance += man(pos, num, n)

    return distance


def puzzle_solver(board, alg):

    def expand(curr):

        nonlocal explored

        boards = moves(board=curr, n=curr.get_n(), zero=curr.get_zero_index())

        moveset = []
        for b in boards:
            direction = b[0]
            state = b[1]
            if tuple(state) not in explored:

                puzzle = NPuzzle(n=curr.get_n(), state=state)
                puzzle.set_parent(curr)
                puzzle.set_parent_path(direction)
                puzzle.cost += curr.cost + 1
                curr.add_child(puzzle)

                moveset.append(puzzle)
                explored[tuple(state)] = True

        return moveset

    def set_q(state):
        if alg == 'A*':
            state = [0, state]
        return [state]

    def pop_q():
        nonlocal q

        state = q.pop(0)
        if alg == 'A*':
            state = state[1]
        return state

    def increment_q():
        nonlocal alg, q
        if alg == 'dfs':
            q = children + q
        elif alg == 'bfs':
            q += children
        else:
            q += [[manhattan(board=child, n=child.get_n()), child] for child in children]
            q.sort(key=lambda h: h[0])

    q = set_q(board)

    expanded_nodes = 0
    max_q = 1
    tree_height = 0

    explored = {tuple(board.get_state()): True}

    while q:
        curr = pop_q()

        if curr.cost > tree_height:
            tree_height = curr.cost

        if check(curr):
            return {'cost': curr.cost,
                    'tree depth': tree_height,
                    'max queue size': max_q,
                    'expanded_nodes': expanded_nodes,
                    'path': path(board, curr),
                    'resource': None}

        expanded_nodes += 1
        children = expand(curr=curr)

        increment_q()

        if len(q) > max_q:
            max_q = len(q)


def check_square(x):
    # determines if x is a square root, eg, the entries in the game board are of size n x n
    i = 1
    square = 1

    while x > square:
        i += 1
        square = int(pow(i, 2))

    if x == square:
        return True
    else:
        return False


def check_numbers(state):

    if sorted(state) == [x for x in range(len(state))]:
        return True
    else:
        return False


def main():

    # check for valid # of arguments
    if len(sys.argv) != 3:
        print("requires two arguments (search algorithm['bfs', 'dfs', 'A*'] and string of input '0,2,1,3')")
        return

    alg = sys.argv[1]
    start = sys.argv[2]

    # check for valid alg specification
    if alg not in ['bfs', 'dfs', 'A*']:
        print("algorithm not correctly specified. please choose 'bfs', 'dfs', or 'A*' as the first argument")
        return

    # check for numbers in board
    try:
        start = start.split(',')
        start = [int(x) for x in start]
    except ValueError:
        print("puzzle (%s) must contain all integers in the form 0,1,2,3" % sys.argv[2])
        return

    # check for correct board size
    if not check_square(len(start)):
        print("input is not a square matrix")
        return

    # check for valid set of numbers, given board size
    if not check_numbers(start):
        print("starting board (%s) contains invalid numbers. Each number must be unique within [1, n^2]" % start)

    n = int(pow(len(start), 0.5))

    puzzle = NPuzzle(n=n, state=start)

    start = time.time()
    metrics = puzzle_solver(board=puzzle, alg=alg)
    end = time.time()

    print('path cost is: %s' % metrics['cost'])
    print('number of expanded nodes: %s' % metrics['expanded_nodes'])
    print('max queue size: %s' % metrics['max queue size'])
    print('max depth: %s' % metrics['tree depth'])
    print('solution path: %s' % metrics['path'])
    print('time elapsed: %s' % (end - start))


if __name__ == "__main__":
    main()
