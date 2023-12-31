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


ACTION_LIST = ["UP", "DOWN", "LEFT", "RIGHT"]

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
            
            # initialize row and col dim
            self.rows, self.cols = [int(x) for x in lines[0].split()]

            # grid
            g = []
            for i in range(1, len(lines) - 1):
                g.append([int(x) for x in lines[i].split()])
            self.grid = g

            # start
            row, col = lines[-1].split()
            self.start = (int(row), int(col))

            # residences
            res = set()
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 1:
                        res.add((r, c))
            self.residences = res

    def getStartState(self) -> tuple:
        "*** YOUR CODE HERE ***"
        start_pos = self.start
        res = set()
        if start_pos in self.residences:
            res.add(start_pos)
        return {"pos": start_pos, "res": res}

    def isGoalState(self, state: tuple) -> bool:
        "*** YOUR CODE HERE ***"
        return len(state["res"]) == len(self.residences)

    def getSuccessors(self, state: tuple) -> List[Tuple["State", str, int]]:
        "*** YOUR CODE HERE ***"
        successors = []
        
        # get the new position
        r, c = state["pos"]
        for action in ACTION_LIST:
            nr, nc = r, c
            if action == "UP":
                nr -= 1
            elif action == "DOWN":
                nr += 1
            elif action == "LEFT":
                nc -= 1
            else:
                nc += 1

            # add the new state accordingly
            if (nr in range(self.rows) and nc in range(self.cols)):
                new_state = {"pos": (nr, nc), "res": state["res"].copy()}
                # residence case
                if self.grid[nr][nc] == 1:
                    new_state["res"].add((nr, nc))
                # obstacle case
                elif self.grid[nr][nc] == -1:
                    continue
                successors.append((new_state, action, 1))

        return successors


    def getCostOfActions(self, actions: List[str]) -> int:
        "*** YOUR CODE HERE ***"
        return len(actions)


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
    pending, visited = Stack(), set()
    start = problem.getStartState()
    pending.push((start, []))

    while not pending.isEmpty():
        s, actions = pending.pop()

        if problem.isGoalState(s):
            return actions
        
        state_tuple = (s["pos"], frozenset(s["res"]))
        if state_tuple not in visited:
            visited.add(state_tuple)

            for neighbor in problem.getSuccessors(s):
                new_state, action, _ = neighbor
                new_actions = []
                if actions:
                    new_actions = actions.copy()
                new_actions.append(action)
                pending.push((new_state, new_actions))

    raise Exception("Rip")


def breadthFirstSearch(problem: SearchProblem) -> List[str]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    pending, visited = Queue(), set()
    start = problem.getStartState()
    pending.push((start, []))

    while not pending.isEmpty():
        s, actions = pending.pop()

        if problem.isGoalState(s):
            return actions
        
        state_tuple = (s["pos"], frozenset(s["res"]))
        if state_tuple not in visited:
            visited.add(state_tuple)

            for neighbor in problem.getSuccessors(s):
                new_state, action, _ = neighbor
                new_actions = []
                if actions:
                    new_actions = actions.copy()
                new_actions.append(action)
                pending.push((new_state, new_actions))

    raise Exception("Rip")


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
    return len(problem.residences) - len(state["res"])


def customHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    Create your own heurstic. The heuristic should
        (1) reduce the number of states that we need to search (tested by the autograder by counting the number of
            calls to GridworldSearchProblem.getSuccessors)
        (2) be admissible and consistent
    """
    # return Manhattan distance between state and closest unvisited residence
    min_dist = float('inf')
    for res in problem.residences:
        resx, resy = res
        sx, sy = state["pos"]
        d = abs(resx - sx) + abs(resy - sy)
        if d < min_dist and res not in state["res"]:
            min_dist = d
    if min_dist == float('inf'):
        return 0
    return min_dist

def getPriority(heuristic, state, problem, cost):
    return heuristic(state, problem) + cost

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[str]:
    """Search the node that has the lowest combined cost and heuristic first.
    This function takes in an arbitrary heuristic (which itself is a function) as an input."""
    "*** YOUR CODE HERE ***"
    pending, visited = PriorityQueue(), set()
    start = problem.getStartState()
    pending.update((start, []), heuristic(start, problem))

    while not pending.isEmpty():
        s, actions = pending.pop()

        state_tuple = (s["pos"], frozenset(s["res"]))
        if state_tuple not in visited:
            visited.add(state_tuple)

        if problem.isGoalState(s):
            return actions

        for neighbor in problem.getSuccessors(s):
            new_state, action, _ = neighbor
            new_tuple_state = (new_state["pos"], frozenset(new_state["res"]))
            if new_tuple_state not in visited:
                visited.add(new_tuple_state)
                new_actions = []
                if actions:
                    new_actions = actions.copy()
                new_actions.append(action)
                g = problem.getCostOfActions(new_actions)
                f = g + heuristic(new_state, problem)
                pending.update((new_state, new_actions), f)

    raise Exception("Rip")


if __name__ == "__main__":
    ### Sample Test Cases ###
    # Run the following assert statements below to test your function, all should run without raising an assertion error 
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case1.txt") # Test Case 1
    print("DFS", depthFirstSearch(gridworld_search_problem))
    print("BFS", breadthFirstSearch(gridworld_search_problem))
    print("A Star", aStarSearch(gridworld_search_problem))
    
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case2.txt") # Test Case 2
    print("DFS", depthFirstSearch(gridworld_search_problem))
    print("BFS", breadthFirstSearch(gridworld_search_problem))
    print("A Star", aStarSearch(gridworld_search_problem))
    
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case3.txt") # Test Case 3
    print("DFS", depthFirstSearch(gridworld_search_problem))
    print("BFS", breadthFirstSearch(gridworld_search_problem))
    print("A Star", aStarSearch(gridworld_search_problem))
