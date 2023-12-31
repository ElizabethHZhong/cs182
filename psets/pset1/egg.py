# -*- coding: utf-8 -*-
"""
CS 182 Problem Set 1: Python Coding Questions - Fall 2023
Due October 4, 2023 at 11:59pm
"""

### Package Imports ###
import heapq
import abc
from typing import List, Optional, Tuple
### Package Imports ###


#### Coding Problem Set General Instructions - PLEASE READ ####
# 1. All code should be written in python 3.7 or higher to be compatible with the autograder
# 2. Your submission file must be named "pset1.py" exactly
# 3. No additional outside packages can be referenced or called, they will result in an import error on the autograder
# 4. Function/method/class/attribute names should not be changed from the default starter code provided
# 5. All helper functions and other supporting code should be wholly contained in the default starter code declarations provided.
#    Functions and objects from your submission are imported in the autograder by name, unexpected functions will not be included in the import sequence


class Stack:
    """A container with a last-in-first-out (LIFO) queuing policy."""
    def __init__(self):
        self.list = []

    def push(self,item):
        """Push 'item' onto the stack"""
        self.list.append(item)

    def pop(self):
        """Pop the most recently pushed item from the stack"""
        return self.list.pop()

    def isEmpty(self):
        """Returns true if the stack is empty"""
        return len(self.list) == 0

class Queue:
    """A container with a first-in-first-out (FIFO) queuing policy."""
    def __init__(self):
        self.list = []

    def push(self,item):
        """Enqueue the 'item' into the queue"""
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        """Returns true if the queue is empty"""
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class SearchProblem(abc.ABC):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    @abc.abstractmethod
    def getStartState(self) -> "State":
        """
        Returns the start state for the search problem.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def isGoalState(self, state: "State") -> bool:
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def getSuccessors(self, state: "State") -> List[Tuple["State", str, int]]:
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def getCostOfActions(self, actions) -> int:
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        raise NotImplementedError


# ACTION_LIST = ["UP", "RIGHT", "DOWN", "LEFT"]
# DIR = [(-1, 0), (0, 1), (1, 0), (0, -1)]

ACTION_LIST = ["UP", "DOWN", "LEFT", "RIGHT"]

# ACTION_LIST = ["UP", "DOWN", "LEFT", "RIGHT"]
# DIR = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class State:
    def __init__(self, row: int, col: int, residences = set(), actions = []):
        self.r, self.c = row, col
        self.residences = residences
        # self.actions = actions

    def get_pos(self):
        return (self.r, self.c)
    
    def __repr__(self) -> str:
        return str((self.r, self.c))

def print_arr(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            num = arr[i][j]
            print(num if num < 0 else f' {num}', end=' ')
        print()

class GridworldSearchProblem(SearchProblem):
    """
    Fill in these methods to define the grid world search as a search problem.
    Actions are of type `str`. Feel free to use any data type/structure to define your states though.
    In the type hints, we use "State" to denote a data structure that keeps track of the state, and you can use
    any implementation of a "State" you want.
    """
    def __init__(self, file):
        """Read the text file and initialize all necessary variables for the search problem"""
        "*** YOUR CODE HERE ***"
        with open(file) as f:
            lines = f.readlines()

            # initialize row and col dimensions
            self.rows, self.cols = [int(x) for x in lines[0].split()]

            # initalize grid 2D array
            g = []
            for i in range(1, len(lines) - 1):
                g.append([int(x) for x in lines[i].split()])
            self.grid = g
        
            # initalize start position tuple
            row, col = lines[-1].split()
            self.start = State(int(row), int(col))
            if self.grid[int(row)][int(col)] == 1:
                self.start.residences.add((int(row), int(col)))

            # initalize residences
            residences = set()
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 1:
                        residences.add((r, c))
            self.residences = residences
            
            print("Problem Description")
            print("Dimensions: {} x {}".format(self.rows, self.cols))
            print("Grid")
            print_arr(self.grid)
            print("Starting Position: {}".format(self.start.get_pos()))

    def getStartState(self) -> State:
        "*** YOUR CODE HERE ***"
        return self.start

    def isGoalState(self, state: State) -> bool:
        "*** YOUR CODE HERE ***"
        return len(self.residences) == len(state.residences)

    def getSuccessors(self, state: State) -> List[Tuple[List[int], str, int]]:
        "*** YOUR CODE HERE ***"
        successors = []
        for i in range(len(ACTION_LIST)):
            # get new state
            rx, cx = DIR[i]
            nrow, ncol = state.r + rx, state.c + cx

            # add new state to successors if new state is a valid move
            if (nrow in range(self.rows) and
                ncol in range(self.cols) and
                self.grid[nrow][ncol] != -1):
                # make the new state
                new_state = State(nrow, 
                                  ncol, 
                                  state.residences.copy())
                # new_state = State(nrow, 
                #                   ncol, 
                #                   state.residences.copy(), 
                #                   state.actions.copy())

                # if current position is a residence, update
                if self.grid[nrow][ncol] == 1:
                    new_state.residences.add((nrow, ncol))

                # add the action to get to this new state
                action = ACTION_LIST[i]
                successors.append((new_state, action, 1))

        return successors
    
    # def getSuccessors(self, state: State) -> List[Tuple[List[int], str, int]]:
    #     "*** YOUR CODE HERE ***"
    #     successors = []
    #     for i in range(len(ACTION_LIST)):
    #         # get new state
    #         rx, cx = DIR[i]
    #         nrow, ncol = state.r + rx, state.c + cx

    #         # add new state to successors if new state is a valid move
    #         if (nrow in range(self.rows) and
    #             ncol in range(self.cols) and
    #             self.grid[nrow][ncol] != -1):
    #             # make the new state
    #             new_state = State(nrow, 
    #                               ncol, 
    #                               state.residences.copy(), 
    #                               state.actions.copy())

    #             # if current position is a residence, update
    #             if self.grid[nrow][ncol] == 1:
    #                 new_state.residences.add((nrow, ncol))

    #             # add the action to get to this new state
    #             action = ACTION_LIST[i]
    #             new_state.actions.append(action)

    #             # add the new state to the successors list
    #             successors.append((new_state, action, 1))

    #     return successors

    def getCostOfActions(self, actions: List[str]) -> int:
        "*** YOUR CODE HERE ***"
        return len(actions)

def another(problem: SearchProblem, col_type: str) -> List[str]:
    # initialize pending and visited
    empty = Stack() if col_type == "DFS" else Queue()
    pending, visited = empty, set()

    # add the starting state to pending and visited
    start = problem.getStartState()
    pending.push((start, [])) # CHECK
    visited.add((start.get_pos(), frozenset(start.residences)))
    i = 0
    # exhaustively search for the goal state
    while not pending.isEmpty():
        # pop next state
        s, actions = pending.pop()

        # if we found the goal state, return actions
        if problem.isGoalState(s):
            print(i)
            return actions

        # add to visited if not already
        s_tuple = (s.get_pos(), frozenset(s.residences))
        if s_tuple not in visited:
            visited.add(s_tuple)

        # add neighbors to pending
        neighbors = problem.getSuccessors(s)
        if col_type == "DFS":
            neighbors.reverse()
        for neighbor in neighbors:
            new_state, action, _ = neighbor
            state_tuple = (new_state.get_pos(), frozenset(new_state.residences))
            if state_tuple not in visited:
                i += 1
                new_actions = actions.copy()
                new_actions.append(action)
                # visited.add(state_tuple)
                pending.push((new_state, new_actions))

    return ["No solution"]

def abstracted(problem: SearchProblem, col_type: str) -> List[str]:
    # initialize pending and visited
    empty = Stack() if col_type == "DFS" else Queue()
    pending, visited = empty, set()

    # add the starting state to pending and visited
    start = problem.getStartState()
    pending.push(start)
    visited.add((start.get_pos(), frozenset(start.residences)))

    # exhaustively search for the goal state
    while not pending.isEmpty():
        # pop next state
        s = pending.pop()

        # if we found the goal state, return actions
        if problem.isGoalState(s):
            return s.actions

        # add neighbors to pending
        neighbors = problem.getSuccessors(s)
        if col_type == "DFS":
            neighbors.reverse()
        for neighbor in neighbors:
            new_state, action, _ = neighbor
            state_tuple = (new_state.get_pos(), frozenset(new_state.residences))
            if state_tuple not in visited:
                visited.add(state_tuple)
                pending.push(new_state)

    return ["No solution"]

def pseudoBFS(problem: SearchProblem, col_type: str) -> List[str]:
    # initialize pending and visited
    empty = Stack() if col_type == "DFS" else Queue()
    pending, visited = empty, set()

    # add the starting state to pending and visited
    start = problem.getStartState()
    pending.push(start)
    visited.add((start.get_pos(), frozenset(start.residences)))

    # exhaustively search for the goal state
    while not pending.isEmpty():
        # pop next state
        s = pending.pop()
        final = s.actions

        # if we found the goal state, return actions
        if problem.isGoalState(s):
            return s.actions

        # else we add neighbors to pending and update actions accordingly
        neighbors = problem.getSuccessors(s)
        if col_type == "DFS":
            neighbors.reverse()
        for neighbor in neighbors:
            new_state, _, _ = neighbor
            state_tuple = (new_state.get_pos(), frozenset(new_state.residences))
            if state_tuple not in visited:
                visited.add(state_tuple)
                pending.push(new_state)

    return ["No solution"]


def depthFirstSearch(problem: SearchProblem) -> List[str]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return another(problem, "DFS")


def breadthFirstSearch(problem: SearchProblem) -> List[str]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return another(problem, "BFS")


def nullHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def simpleHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    This heuristic returns the number of residences that you have not yet visited.
    """
    raise NotImplementedError


def customHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    Create your own heurstic. The heuristic should
        (1) reduce the number of states that we need to search (tested by the autograder by counting the number of
            calls to GridworldSearchProblem.getSuccessors)
        (2) be admissible and consistent
    """
    raise NotImplementedError


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[str]:
    """Search the node that has the lowest combined cost and heuristic first.
    This function takes in an arbitrary heuristic (which itself is a function) as an input."""
    "*** YOUR CODE HERE ***"
    return []
    raise NotImplementedError


if __name__ == "__main__":
    ### Sample Test Cases ###
    # Run the following assert statements below to test your function, all should run without raising an assertion error 
    # gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case1.txt") # Test Case 1
    # print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem))
    
    # gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case2.txt") # Test Case 2
    # print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem))
    
    # gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case3.txt") # Test Case 3
    # print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem))

    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case4.txt") # Test Case 4
    print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem))
