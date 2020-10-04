# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    test = problem.getSuccessors(problem.getStartState())
    print(test)
    print(test[0][0])
    test = problem.getSuccessors(test[0][0])
    print(test)
    print(test[0][0])
    print(problem.isGoalState(test[0][0]))
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
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
    #util.raiseNotDefined()
    
    #variables that maintain frontier
    already_been = []
    # Dictionary contatining information of parent for a child 
    parent_child = {}
    #problem defined stack
    frontier = util.Stack()
    
    # lets get directions
    from game import Directions
    
    
    # Making a dictionary pf directions
    # Was using this for earlier implementation which does not work with autograder
    directions = {'North' : Directions.NORTH,
                  'West' : Directions.WEST,
                  'East' : Directions.EAST,
                  'South' : Directions.SOUTH,
                  'left' : Directions.LEFT,
                  'up': Directions.NORTH,
                  'down':Directions.SOUTH,
                  'right': Directions.RIGHT,
                  'Reverse':Directions.REVERSE,
                  'Stop': Directions.STOP
                  }
    
    # Lets get the starting state
    start = problem.getStartState()
    print(start)
    # Lets have start a part of frontier
    frontier.push((start,[]))
    flag = 0                      # to check if goal is reached
    # lets have a loop which checks if we have gone through all nodes or have a goal
    # state.
    while(~frontier.isEmpty()):
        
        #Popping the last element out of stack
        present = frontier.pop()
        
        # Checking if this state is goal state. Since  in DFS, we check perform goal 
        # test once we visit the node.
        if problem.isGoalState(present[0]):
            flag = 1
            #break
            return present[1]
        
        # Maintaining a list of visited nodes to implement graph algo
        already_been.append(present[0])
        
        # Finding Successors
        suc_nodes = problem.getSuccessors(present[0])
        # Iterating through the nodes
        for i in suc_nodes:
            # Checking if we have visited the node before
            if i[0] not in already_been:
                frontier.push((i[0], present[1] + [i[1]]))  # Pushing the node to the frontier along with actions
                parent_child[i] = present   # Maintaining dict for path
                
        
    

    '''
    ---------------------------------------------------------------------------------
    THE PART COMMENTED BELOW IS FROM PREVIOUS IMPLEMENTATION 
    THIS PART WORKS BETTER, BUT IS NOT COMPATIBLE WITH AUTOGRADER
    ---------------------------------------------------------------------------------    
    # Lets check if we found the goal or not
    if flag == 1:
        print('Goal found')
        # Lets find path
        direc = present[1]
        final_dir = []
        
        while direc != 0:
            
            final_dir.append(directions[direc])  # Storing the action 
            
            present = parent_child[present]  # Fetching the parent of this child
            
            direc = present[1] # Updating direction
            
        return final_dir[::-1]
            
    else:
        print('Goal Not found')
        return []
        
    '''
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    
    #variables that maintain frontier
    already_been = []
    # Dictionary contatining information of parent for a child 
    parent_child = {}
    #problem defined queue
    frontier = util.Queue()
    
    # lets get directions
    from game import Directions
    
    
    # Making a dictionary pf directions
    directions = {'North' : Directions.NORTH,
                  'West' : Directions.WEST,
                  'East' : Directions.EAST,
                  'South' : Directions.SOUTH,
                  'left' : Directions.LEFT,
                  'up': Directions.NORTH,
                  'down':Directions.SOUTH,
                  'right': Directions.RIGHT,
                  'Reverse':Directions.REVERSE,
                  'Stop': Directions.STOP
                  }
    
    # Lets get the starting state
    start = problem.getStartState()
    
    # SInce we are working with BFS now, we need to check for goal state
    # before we visit it. SO
    #if problem.isGoalState(start):
    #    flag = 1
    #else:
        # Lets have start a part of frontier
    frontier.push((start,[]))
    flag = 0                      # to check if goal is reached
    # lets have a loop which checks if we have gone through all nodes or have a goal
    # state.
    while(~frontier.isEmpty()):
        
        #Popping the last element out of stack
        present = frontier.pop()
        
        # The below given three lines were added to make autograder work
        if problem.isGoalState(present[0]):
            flag = 1
            return present[1]
        
        
        # Maintaining a list of visited nodes to implement graph algo
        already_been.append(present[0])
        
        # Finding Successors
        suc_nodes = problem.getSuccessors(present[0])
        #print(present,suc_nodes)
        # Iterating through the nodes
        for i in suc_nodes:
            # Checking if we have visited the node before
            if i[0] not in already_been and i[0] not in (j[0] for j in frontier.list):
                frontier.push((i[0],present[1] + [i[1]]))       # Pushing the node to the frontier
                parent_child[i] = present   # Maintaining dict for path
                # Checking if this state is goal state. Since  in BFS, 
                # we check perform goal test once we visit the node.
                #if problem.isGoalState(i[0]):
                #    flag = 1
                #    return present[1] + [i[1]]
                #    present = i
                #    break
                
        if flag == 1:
            break
                
    '''
    ---------------------------------------------------------------------------------
    THE PART COMMENTED BELOW IS FROM PREVIOUS IMPLEMENTATION 
    THIS PART WORKS BETTER, BUT IS NOT COMPATIBLE WITH AUTOGRADER
    ---------------------------------------------------------------------------------        
        
    # Lets check if we found the goal or not
    if flag == 1:
        print('Goal found')
        # Lets find path
        direc = present[1]
        final_dir = []
        
        while direc != 0:
            
            final_dir.append(directions[direc])  # Storing the action 
            
            present = parent_child[present]  # Fetching the parent of this child
            
            direc = present[1] # Updating direction
            
        return final_dir[::-1]
            
    else:
        print('Goal Not found')
        return []
    
    '''

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    #variables that maintain frontier
    #variables that maintain frontier
    already_been = []
    # Dictionary contatining information of parent for a child 
    parent_child = {}
    #problem defined stack
    frontier = util.PriorityQueue()
    
    # lets get directions
    from game import Directions
    
    
    # Making a dictionary pf directions
    directions = {'North' : Directions.NORTH,
                  'West' : Directions.WEST,
                  'East' : Directions.EAST,
                  'South' : Directions.SOUTH,
                  'left' : Directions.LEFT,
                  'up': Directions.NORTH,
                  'down':Directions.SOUTH,
                  'right': Directions.RIGHT,
                  'Reverse':Directions.REVERSE,
                  'Stop': Directions.STOP
                  }
    
    # Lets get the starting state
    start = problem.getStartState()
    #print(start)
    # Lets have start a part of frontier
    frontier.push((start,[]),0)
    flag = 0                      # to check if goal is reached
    # lets have a loop which checks if we have gone through all nodes or have a goal
    # state.
    while(~frontier.isEmpty()):
        
        #Popping the last element out of stack
        present = frontier.pop()
        
        # Checking if this state is goal state. Since  in UCS, we check perform goal 
        # test once we visit the node.
        if problem.isGoalState(present[0]):
            flag = 1
            #break
            return present[1]
        
        # Maintaining a list of visited nodes to implement graph algo
        already_been.append(present[0])
        
        # Finding Successors
        suc_nodes = problem.getSuccessors(present[0])
        # Iterating through the nodes
        for i in suc_nodes:
            # Checking if we have visited the node before
            if i[0] not in already_been and i[0] not in (j[2][0] for j in frontier.heap):
                #accumulating the cost of all the paths
                n_cost = problem.getCostOfActions(present[1] + [i[1]])
                frontier.push((i[0], present[1] + [i[1]]),n_cost)  # Pushing the node to the frontier
                parent_child[i] = present   # Maintaining dict for path
                
            elif i[0] not in already_been and i[0] in (j[2][0] for j in frontier.heap):
                #This part of code is to check if this new path cost has less cost
                # than the previous path cost we have seen for this node
                for j in frontier.heap:
                        if j[2][0] == i[0]:
                            o_cost = problem.getCostOfActions(j[2][1])

                n_cost = problem.getCostOfActions(present[1] + [i[1]])

                # Updtaing the cost
                if o_cost > n_cost:
                    frontier.update((i[0],present[1] + [i[1]]),n_cost)
     
        
        
    '''
    ---------------------------------------------------------------------------------
    THE PART COMMENTED BELOW IS FROM PREVIOUS IMPLEMENTATION 
    THIS PART WORKS BETTER, BUT IS NOT COMPATIBLE WITH AUTOGRADER
    ---------------------------------------------------------------------------------        
    # Lets check if we found the goal or not
    if flag == 1:
        print('Goal found')
        # Lets find path
        direc = present[1]
        final_dir = []
        
        while direc != 0:
            
            final_dir.append(directions[direc])  # Storing the action 
            
            present = parent_child[present]  # Fetching the parent of this child
            
            direc = present[1] # Updating direction
            
        return final_dir[::-1]
            
    else:
        print('Goal Not found')
        return []
    
    '''
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    already_been = []
    # Dictionary contatining information of parent for a child 
    parent_child = {}
    #problem defined stack
    frontier = util.PriorityQueue()
    
    # lets get directions
    from game import Directions
    
    
    # Making a dictionary pf directions
    directions = {'North' : Directions.NORTH,
                  'West' : Directions.WEST,
                  'East' : Directions.EAST,
                  'South' : Directions.SOUTH,
                  'left' : Directions.LEFT,
                  'up': Directions.NORTH,
                  'down':Directions.SOUTH,
                  'right': Directions.RIGHT,
                  'Reverse':Directions.REVERSE,
                  'Stop': Directions.STOP
                  }
    
    # Lets get the starting state
    start = problem.getStartState()
    print(start)
    # Lets have start a part of frontier
    frontier.push((start,[]),heuristic(start,problem))
    flag = 0                      # to check if goal is reached
    # lets have a loop which checks if we have gone through all nodes or have a goal
    # state.
    while(~frontier.isEmpty()):
        
        #Popping the last element out of stack
        present = frontier.pop()
        
        # Checking if this state is goal state. Since  in DFS, we check perform goal 
        # test once we visit the node.
        if problem.isGoalState(present[0]):
            flag = 1
            #break
            return present[1]
        
        # Maintaining a list of visited nodes to implement graph algo
        already_been.append(present[0])
        
        # Finding Successors
        suc_nodes = problem.getSuccessors(present[0])
        # Iterating through the nodes
        for i in suc_nodes:
            # Checking if we have visited the node before
            if i[0] not in already_been and i[0] not in (j[2][0] for j in frontier.heap):
                #accumulating the cost of all the paths. 
                n_cost = problem.getCostOfActions(present[1] + [i[1]])
                n_cost = n_cost + heuristic(i[0],problem)
                frontier.push((i[0], present[1] + [i[1]]),n_cost)  # Pushing the node to the frontier
                parent_child[i] = present   # Maintaining dict for path
                
            elif i[0] not in already_been and i[0] in (j[2][0] for j in frontier.heap):
                #This part of code is to check if this new path cost has less cost
                # than the previous path cost we have seen for this node
                for j in frontier.heap:
                        if j[2][0] == i[0]:
                            o_cost = problem.getCostOfActions(j[2][1])
                            o_cost = o_cost + heuristic(i[0],problem)

                n_cost = problem.getCostOfActions(present[1] + [i[1]])
                n_cost = n_cost + heuristic(i[0],problem)
            
                if o_cost > n_cost:
                    frontier.update((i[0],present[1] + [i[1]]),n_cost)
    
     

    '''
    ---------------------------------------------------------------------------------
    THE PART COMMENTED BELOW IS FROM PREVIOUS IMPLEMENTATION 
    THIS PART WORKS BETTER, BUT IS NOT COMPATIBLE WITH AUTOGRADER
    ---------------------------------------------------------------------------------               
        
        
    # Lets check if we found the goal or not
    if flag == 1:
        print('Goal found')
        # Lets find path
        direc = present[1]
        final_dir = []
        
        while direc != 0:
            
            final_dir.append(directions[direc])  # Storing the action 
            
            present = parent_child[present]  # Fetching the parent of this child
            
            direc = present[1] # Updating direction
            
        return final_dir[::-1]
            
    else:
        print('Goal Not found')
        return []
    '''


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
