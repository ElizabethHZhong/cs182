# -*- coding: utf-8 -*-
"""
CS 182 Problem Set 1: Python Coding Questions - Fall 2022
Due September 27, 2022 at 11:59pm
"""

### Package Imports ###
import heapq
import abc
from typing import List, Optional, Tuple
### Package Imports ###


#### Coding Problem Set General Instructions - PLEASE READ ####
# 1. All code should be written in python 3.6 or higher to be compatible with the autograder
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
        f = open(file, "r")
        dim = f.readline()
        coords = list(map(int, dim.strip().split(' ')))
        self.rows = coords[0]
        self.columns = coords[1] #could be annoying if rows >= 10
        self.map = []
        for i in range(self.rows):
            line = f.readline()
            self.map.append(list(map(int, line.strip().split(' '))))
        start = f.readline()
        f.close()
        startcoords = list(map(int, start.strip().split(' ')))
        startx = startcoords[0]
        starty = startcoords[1]
        self.start = (startx, starty)
        self.residences = set()
        for row in range(self.rows):
            for col in range(self.columns): 
                if self.map[row][col] == 1:
                    self.residences.add((row,col))
        # raise NotImplementedError

    def getStartState(self) -> tuple:
        "*** YOUR CODE HERE ***"
        pos = self.start
        res = set()
        if pos in self.residences:
            res.add(pos)
        start_state = {"pos":pos, "res":res}
        return start_state

    def isGoalState(self, state: tuple) -> bool:
        "*** YOUR CODE HERE ***"
        if len(state["res"]) == len(self.residences): 
            return True 
        return False
        # raise NotImplementedError

    def getSuccessors(self, state: dict) -> List[Tuple[dict, str, int]]:
        "*** YOUR CODE HERE ***"
        succ = []
        oldrow = state["pos"][0]
        oldcol = state["pos"][1]
        for action in ACTION_LIST:
            newrow = oldrow
            newcol = oldcol
            if action == "UP":
                newrow -= 1
            elif action == "DOWN":
                newrow += 1
            elif action == "LEFT":
                newcol -= 1
            else:
                newcol += 1
            if newcol >= 0 and newcol < self.columns and newrow >= 0 and newrow < self.rows:
                newstate = {"pos":(newrow, newcol),"res": state["res"].copy()}
                if self.map[newrow][newcol] == 1: # is a residence
                    if (newrow,newcol) not in state["res"]: # new residence
                        newstate["res"].add((newrow,newcol)) # add to visited residents
                elif self.map[newrow][newcol] == -1:
                    continue # skip over this loop iteration
                succ.append((newstate, action, 1))
        return succ


    def getCostOfActions(self, actions: List[str]) -> int:
        "*** YOUR CODE HERE ***"
        return len(actions)
        # return NotImplementedError


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

    stack = Stack()
    visited = []
    start = problem.getStartState()
    stack.push({"state":start, "actions":[]})
    while not stack.isEmpty():
        pop = stack.pop()
        state = pop["state"]
        if problem.isGoalState(state):
            return pop["actions"]
        if state not in visited:
            visited.append(state)
            for succ in problem.getSuccessors(state):
                newstate = succ[0]
                action = succ[1]
                actions = []
                if pop["actions"] is not None:
                    actions = pop["actions"].copy()
                actions.append(action)
                stack.push({"state":newstate, "actions":actions})
    raise Exception("No goal state found")


def breadthFirstSearch(problem: SearchProblem) -> List[str]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = Queue()
    start = problem.getStartState()
    visited = [start]
    queue.push({"state":start, "actions":[]})
    while not queue.isEmpty():
        pop = queue.pop()
        state = pop["state"]
        if problem.isGoalState(state):
            return pop["actions"]
        for succ in problem.getSuccessors(state):
            newstate = succ[0]
            if newstate not in visited:
                visited.append(newstate)
                action = succ[1]
                actions = []
                if pop["actions"] is not None:
                    actions = pop["actions"].copy()
                actions.append(action)
                queue.push({"state":newstate, "actions":actions})
    raise Exception("No goal state found")    


def nullHeuristic(state: "State", problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def simpleHeuristic(state: dict, problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    This heuristic returns the number of residences that you have not yet visited.
    """
    total = len(problem.residences)
    visited = len(state["res"])
    todo = total - visited
    return todo


def customHeuristic(state: dict, problem: Optional[GridworldSearchProblem] = None) -> int:
    """
    Create your own heurstic. The heuristic should
        (1) reduce the number of states that we need to search (tested by the autograder by counting the number of
            calls to GridworldSearchProblem.getSuccessors)
        (2) be admissible and consistent
    """
    if len(state["res"]) == len(problem.residences):
        minDist = 0
    else: 
        minDist = problem.rows + problem.columns
        for res in problem.residences:
            if res not in state["res"]: 
                dist = abs(state["pos"][0]-res[0]) + abs(state["pos"][1]-res[1])
                if dist < minDist:
                    minDist = dist
    return minDist
    




def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[str]:
    """Search the node that has the lowest combined cost and heuristic first.
    This function takes in an arbitrary heuristic (which itself is a function) as an input."""
    "*** YOUR CODE HERE ***"

    queue = PriorityQueue()
    start = problem.getStartState()
    visited = []
    queue.update({"state":start, "actions":[]},heuristic(start, problem))
    while not queue.isEmpty():
        pop = queue.pop()
        state = pop["state"]
        if state not in visited:
            visited.append(state)
        if problem.isGoalState(state):
            return pop["actions"]
        for succ in problem.getSuccessors(state):
            newstate = succ[0]
            if newstate not in visited:
                visited.append(newstate)
                action = succ[1]
                actions = []
                if pop["actions"] is not None:
                    actions = pop["actions"].copy()
                actions.append(action)
                g = problem.getCostOfActions(actions)
                cost = g + heuristic(newstate,problem)
                queue.update({"state":newstate, "actions":actions},cost)
    raise Exception("No goal state found")      




if __name__ == "__main__":
    ### Sample Test Cases ###
    # Run the following statements below to test the running of your program
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case1.txt") # Test Case 1
    print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem, simpleHeuristic))
    
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case2.txt") # Test Case 2
    print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem, simpleHeuristic))
    
    gridworld_search_problem = GridworldSearchProblem("pset1_sample_test_case3.txt") # Test Case 3
    print(depthFirstSearch(gridworld_search_problem))
    # print(breadthFirstSearch(gridworld_search_problem))
    # print(aStarSearch(gridworld_search_problem, simpleHeuristic))
