## NPuzzle Synopsis

The program provides a simple solver for the [Npuzzle game](http://mypuzzle.org/sliding), written for some project work in python 3.5.1. 

The solver takes in two arguments:
 
* a choice of algoritm - (BFS, DFS, A* using manhattan distance heuristic)
* an initial Npuzzle game state

The solver then returns, as a dictionary, the following information:

* path - a valid sequence of movement that arrives at the solution
* expanded_nodes - the number of game states that were reviewed to find the solution
* cost - the total number of steps needed to arrive at the solution
* tree depth - depth of the farthest path that was reviewed
* max queue size - maximum number of game states that were stored in memory during the solver's work
