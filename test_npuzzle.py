from unittest import TestCase
from hw1_kjd import NPuzzle, moves, check, manhattan, puzzle_solver, main
import sys
import time


class TestNpuzzle(TestCase):

    def test_moves(self):

        # size n = 3
        t = [x for x in range(9)]
        n3 = NPuzzle(n=3, state=t)

        # upper left corner - down, and right
        self.assertEqual([['DOWN', [3, 1, 2, 0, 4, 5, 6, 7, 8]], ['RIGHT', [1, 0, 2, 3, 4, 5, 6, 7, 8]]], moves(board=n3, n=3, zero=0))

        # lower right corner - up and lef
        n3.set_state(t[::-1])
        print(n3.get_state())
        self.assertEqual([['UP', [8, 7, 6, 5, 4, 0, 2, 1, 3]], ['LEFT', [8, 7, 6, 5, 4, 3, 2, 0, 1]]], moves(board=n3, n=3, zero=8))

        # lower left corner - up and right
        t[6] = 0
        t[0] = 6
        n3.set_state(t)
        self.assertEqual([['UP', [6, 1, 2, 0, 4, 5, 3, 7, 8]], ['RIGHT', [6, 1, 2, 3, 4, 5, 7, 0, 8]]], moves(board=n3, n=3, zero=6))

        # upper right corner - down and left
        t = [x for x in range(9)]
        t[2] = 0
        t[0] = 2
        n3.set_state(t)
        self.assertEqual([['DOWN', [2, 1, 5, 3, 4, 0, 6, 7, 8]], ['LEFT', [2, 0, 1, 3, 4, 5, 6, 7, 8]]], moves(board=n3, n=3, zero=2))

        # middle up,down,left,right
        t = [x for x in range(9)]
        t[4] = 0
        t[0] = 4
        n3.set_state(t)
        self.assertEqual(moves(board=n3, n=3, zero=4),
                         [['UP', [4, 0, 2, 3, 1, 5, 6, 7, 8]],
                          ['DOWN', [4, 1, 2, 3, 7, 5, 6, 0, 8]],
                          ['LEFT', [4, 1, 2, 0, 3, 5, 6, 7, 8]],
                          ['RIGHT', [4, 1, 2, 3, 5, 0, 6, 7, 8]]])

    def test_check(self):

        # size n = 3
        t = [x for x in range(9)]
        n3 = NPuzzle(n=3, state=t)

        # test true
        self.assertTrue(check(board=n3))
        # test reverse true as false
        n3.set_state(t[::-1])
        self.assertFalse(check(board=n3))
        # check double zeros
        t = [x for x in range(9)]
        t[4] = 0
        self.assertFalse(check(board=n3))

    def test_manhattan(self):

        # size n = 3
        t = [x for x in range(9)]
        n3 = NPuzzle(n=3, state=t)

        # completed board
        self.assertEqual(manhattan(board=n3, n=3), 0)

        # board off by 1
        t[0] = 3
        t[3] = 0
        n3.set_state(t)
        self.assertEqual(manhattan(board=n3, n=3), 2)

        # three move case
        t = [1, 2, 5, 3, 4, 0, 6, 7, 8]
        n3.set_state(t)
        self.assertEqual(manhattan(board=n3, n=3), 6)

    def test_bfs(self):

        t = [x for x in range(9)]

        # base case, start board is final
        n3 = NPuzzle(n=3, state=t)

        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'cost': 0,
                               'expanded_nodes': 0,
                               'resource': None,
                               'max queue size': 1,
                               'path': [],
                               'tree depth': 0})

        # one move case, only one up move needed
        t[0] = 3
        t[3] = 0
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'max queue size': 3,
                               'resource': None,
                               'tree depth': 1,
                               'expanded_nodes': 1,
                               'path': ['UP'],
                               'cost': 1})

        # one move case, only one left move needed
        t = [x for x in range(9)]
        t[0] = 1
        t[1] = 0
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'max queue size': 5,
                               'resource': None,
                               'tree depth': 1,
                               'expanded_nodes': 2,
                               'path': ['LEFT'],
                               'cost': 1})

        # three move case, from hw1 example
        t = [1, 2, 5, 3, 4, 0, 6, 7, 8]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'max queue size': 12,
                               'resource': None,
                               'tree depth': 3,
                               'expanded_nodes': 10,
                               'path': ['UP', 'LEFT', 'LEFT'],
                               'cost': 3})

        # state from 8-puzzle from website
        t = [8, 2, 6, 3, 7, 1, 4, 0, 5]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'max queue size': 25134,
                               'resource': None,
                               'tree depth': 23,
                               'expanded_nodes': 104863,
                               'path': ['UP', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'LEFT',
                                        'DOWN', 'RIGHT', 'UP', 'LEFT', 'UP', 'RIGHT', 'RIGHT', 'DOWN', 'DOWN', 'LEFT',
                                        'LEFT', 'UP', 'UP'],
                               'cost': 23})

        t = [7, 1, 3, 2, 8, 4, 5, 0, 6]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'expanded_nodes': 174583,
                               'path': ['UP', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'DOWN',
                                        'RIGHT', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'UP',
                                        'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'UP', 'LEFT'],
                               'resource': None,
                               'cost': 27,
                               'tree depth': 27,
                               'max queue size': 25134})

        # extreme board
        t = [0, 8, 7, 6, 5, 4, 3, 2, 1]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='bfs'),
                              {'expanded_nodes': 181423,
                               'path': ['DOWN', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'DOWN', 'RIGHT',
                                        'UP', 'UP', 'LEFT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN', 'DOWN',
                                        'LEFT', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'UP', 'LEFT'],
                               'resource': None,
                               'cost': 30,
                               'tree depth': 30,
                               'max queue size': 24048})

    def test_dfs(self):

        t = [x for x in range(9)]

        # base case, start board is final
        n3 = NPuzzle(n=3, state=t)
        print(puzzle_solver(board=n3, alg='dfs'))

        # one move case, only one up move needed
        t[0] = 3
        t[3] = 0
        n3.set_state(t)
        print(puzzle_solver(board=n3, alg='dfs'))

        # one move case, only one left move needed
        t = [x for x in range(9)]
        t[0] = 1
        t[1] = 0
        n3.set_state(t)
        print(puzzle_solver(board=n3, alg='dfs'))

        # three move case, from hw1 example
        t = [1, 2, 5, 3, 4, 0, 6, 7, 8]
        n3.set_state(t)
        print(puzzle_solver(board=n3, alg='dfs'))

        # extreme board
        t = [0, 8, 7, 6, 5, 4, 3, 2, 1]
        n3.set_state(t)
        print(puzzle_solver(board=n3, alg='dfs'))

    def test_A_sharp(self):
        t = [x for x in range(9)]

        # base case, start board is final
        n3 = NPuzzle(n=3, state=t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'resource': None,
                               'expanded_nodes': 0,
                               'max queue size': 1,
                               'cost': 0,
                               'tree depth': 0,
                               'path': []})

        # one move case, only one up move needed
        t[0] = 3
        t[3] = 0
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'resource': None,
                               'expanded_nodes': 1,
                               'max queue size': 3,
                               'cost': 1,
                               'tree depth': 1,
                               'path': ['UP']})

        # one move case, only one left move needed
        t = [x for x in range(9)]
        t[0] = 1
        t[1] = 0
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'resource': None,
                               'expanded_nodes': 1,
                               'max queue size': 3,
                               'cost': 1,
                               'tree depth': 1,
                               'path': ['LEFT']})

        # three move case, from hw1 example
        t = [1, 2, 5, 3, 4, 0, 6, 7, 8]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'resource': None,
                               'expanded_nodes': 3,
                               'max queue size': 4,
                               'cost': 3,
                               'tree depth': 3,
                               'path': ['UP', 'LEFT', 'LEFT']})

        # state from 8-puzzle from website
        t = [8, 2, 6, 3, 7, 1, 4, 0, 5]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'resource': None,
                               'expanded_nodes': 262,
                               'tree depth': 39,
                               'path': ['UP', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'UP', 'LEFT',
                                        'DOWN', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP', 'RIGHT',
                                        'RIGHT', 'DOWN', 'LEFT', 'UP', 'LEFT', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'RIGHT',
                                        'DOWN', 'LEFT', 'LEFT', 'UP', 'UP'],
                               'max queue size': 167,
                               'cost': 37})

        t = [7, 1, 3, 2, 8, 4, 5, 0, 6]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'resource': None,
                               'expanded_nodes': 290,
                               'tree depth': 61,
                               'path': ['UP', 'LEFT', 'UP', 'RIGHT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'LEFT', 'DOWN',
                                        'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'LEFT', 'LEFT', 'DOWN',
                                        'RIGHT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'LEFT', 'UP', 'UP', 'RIGHT', 'DOWN',
                                        'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'LEFT', 'UP', 'LEFT', 'DOWN', 'DOWN', 'RIGHT',
                                        'UP', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'RIGHT', 'DOWN', 'LEFT', 'LEFT', 'UP', 'UP'],
                               'max queue size': 195,
                               'cost': 55}
)

        # extreme board
        t = [0, 8, 7, 6, 5, 4, 3, 2, 1]
        n3.set_state(t)
        self.assertCountEqual(puzzle_solver(board=n3, alg='A*'),
                              {'max queue size': 285,
                               'cost': 68,
                               'tree depth': 68,
                               'expanded_nodes': 427,
                               'resource': None,
                               'path': ['RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'LEFT', 'DOWN', 'DOWN', 'RIGHT', 'UP', 'UP',
                                        'RIGHT', 'DOWN', 'DOWN', 'LEFT', 'UP', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'DOWN', 'LEFT',
                                        'UP', 'UP', 'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'UP', 'RIGHT',
                                        'DOWN', 'LEFT', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'LEFT', 'UP',
                                        'RIGHT', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'UP', 'LEFT', 'DOWN', 'DOWN',
                                        'RIGHT', 'UP', 'UP', 'LEFT', 'DOWN', 'RIGHT', 'DOWN', 'LEFT', 'UP', 'UP']})

    def test_main(self):

        print('base case, start board is final')
        sys.argv[2] = '0,1,2,3,4,5,6,7,8'
        sys.argv[1] = 'bfs'
        print('bfs')
        main()
        sys.argv[1] = 'dfs'
        print('DFS')
        main()
        sys.argv[1] = 'A*'
        print('A*')
        main()

        print('one move case, only one up move needed')
        sys.argv[2] = '3,1,2,0,4,5,6,7,8'
        sys.argv[1] = 'bfs'
        print('bfs')
        main()
        sys.argv[1] = 'dfs'
        print('DFS')
        main()
        sys.argv[1] = 'A*'
        print('A*')
        main()

        print('one move case, only one left move needed')
        sys.argv[2] = '1,0,2,3,4,5,6,7,8'
        sys.argv[1] = 'bfs'
        print('bfs')
        main()
        sys.argv[1] = 'dfs'
        print('DFS')
        main()
        sys.argv[1] = 'A*'
        print('A*')
        main()

        print('three move case, from hw1 example')
        sys.argv[2] = '1,2,5,3,4,0,6,7,8'
        sys.argv[1] = 'bfs'
        print('bfs')
        main()
        sys.argv[1] = 'dfs'
        print('DFS')
        main()
        sys.argv[1] = 'A*'
        print('A*')
        main()

        print('extreme board')
        sys.argv[2] = '0,8,7,6,5,4,3,2,1'
        sys.argv[1] = 'bfs'
        print('bfs')
        main()
        sys.argv[1] = 'dfs'
        print('DFS')
        main()
        sys.argv[1] = 'A*'
        print('A*')
        main()

        sys.argv[2] = '0'

        print('random valid state from puzzle website')
        sys.argv[2] = '8,2,6,3,7,1,4,0,5'
        sys.argv[1] = 'bfs'
        print('bfs')
        main()
        sys.argv[1] = 'dfs'
        print('DFS')
        main()
        sys.argv[1] = 'A*'
        print('A*')
        main()

