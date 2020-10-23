# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        GhostPosition = successorGameState.getGhostPositions()
        "*** YOUR CODE HERE ***"
        
        # Distance of food pallets
        food_dist = []
        food_to_go_for = 0 
        # Power pallet avg distance
        power_pallet_dist_weighted = 0
        # Distance from ghost
        ghost_dist = []
        ghost_to_run_from = 0
        ghost_to_run_towards = 0
        # time_parameter
        time_to_eat_ghost = 0
        
        
        
        # Calculating food distance
        for i in newFood.asList():
            food_dist.append(manhattanDistance(newPos,i))
            #taking inverse of food distance so to maximize evaluation function
            if food_dist[-1] == 0:
                food_to_go_for += 0
            else:
                food_to_go_for += 1/(food_dist[-1])
            '''    
            THE COMMENTED CODE FAILS MOST OF THE TIMES BUT IS EFFICIENT SOMETIMES
            #if food_dist[-1] > 20:
            #    print('FOOD FAR')
            #    food_dist_weighted += (1/200)*food_dist[-1]
            #elif food_dist[-1] > 10:
            #    print('FOOD MID')
            #    food_dist_weighted += (1/100)*food_dist[-1]
            #else:
            #    print('FOOD CLOSE')
            #    food_dist_weighted += (1/50)*food_dist[-1]
            '''
            
            
            
        # Ghost states calculation with weight
        for i in GhostPosition:
            ghost_dist.append(manhattanDistance(newPos,i))
            # We need to have weghted average of distance from the ghost
            # more the distance from closest ghost the better
            temp = 0
            if newScaredTimes[len(ghost_dist)-1] == 0:
                if ghost_dist[-1] !=0:
                    ghost_to_run_from -= 1/ghost_dist[-1]
                    
                '''
                THE COMMENTED CODE IS EFFICIENT MOST OF THE TIMES BUT ONLY IS
                WEIGHTED EQUAL TO THE FOOD DISTANCE
                #if ghost_dist[-1] < 4:
                #    #print('Ghost Close')
                #    ghost_dist_weighted_active -= (5)*ghost_dist[-1]
                #    
                #    
                #elif ghost_dist[-1] < 8:
                #    #print('Ghost Mid')
                #    ghost_dist_weighted_active -= (0.5)*ghost_dist[-1]
                #else:
                #    #print('Ghost away')
                #    ghost_dist_weighted_active -= (0.05)*ghost_dist[-1]
                
                '''
            
            else:
                # If ghost is scared
                if ghost_dist[-1] < 4:
                    ghost_to_run_towards += 1/ghost_dist[-1]
                
                '''
                ONLY FOR REFERANCE
                if ghost_dist == [] or sum(ghost_dist)==0:
                    temp = 0
                else:
                    temp = -1*(1/min(ghost_dist))
                '''
        
        # Checking if we have eaten the power pallet
        # If newScaredTimes for any ghost is more than 0 then we have eaten the 
        # power pallet
        time_to_eat_ghost = min([i>0 for i in newScaredTimes])
        
        # COST
        SGSS = successorGameState.getScore()
        
        #Evaluation function
        '''
            DIFFERENT WAYS OF IMPLEMENTING EVALUATION FUNCTION TRIED
            ONLY FEW WORK EFFICIENTLY
            #if time_to_eat_ghost > 0:
            #    eva_func = SGSS +food_dist_weighted#+ min(food_dist) + sum(ghost_dist)/len(ghost_dist)
            #else:
            #    eva_func = SGSS +food_dist_weighted + ghost_dist_weighted_active
            #print(eva_func,SGSS,food_rem,min(food_dist),sum(ghost_dist)/len(ghost_dist))
            #eva_func = (2*SGSS) +(1*food_to_go_for) + (0.1*ghost_dist_weighted_active) + (0.1*ghost_dist_weighted_inactive)
        '''
        eva_func = SGSS + (2*food_to_go_for) + (2*ghost_to_run_from) + ghost_to_run_towards
        return eva_func

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined())
        depth = 0
        number_of_agents = gameState.getNumAgents()
        inf = 10000000000000.0      # variable storing infinity
        
        
        def value(state,depth,agent):
            
            #print("depth:",depth," agent:",agent)
            
            # Check if we have reached the depth
            if depth == self.depth:
                return (self.evaluationFunction(state),0)
            
            # Check if there are NO legal actions
            if not state.getLegalActions(agent):
                return (self.evaluationFunction(state),0)
            
            
                
            if agent == self.index:
                # when agent is equal to 0 
                
                v = -1*inf
                best_action = ''
                
                
                # The following code will work if MINIMIZERS Cooperate
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    
                    Eval,_ = value(new_state,depth,agent+1)
                    if Eval > v :
                        best_action = possible_action
                        v = Eval
                    
                '''
                #Below code will work if the minimizers are NOT cooperating
                
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    for minimizers in range(1,number_of_agents):
                    
                        Eval,_ = value(new_state,depth,minimizers)
                        #val stores the evaluation score
                        if Eval > v :
                            best_action = possible_action
                            v = Eval
                '''
                            
            else:
                # If the current agent is ghost
                
                v = inf
                best_action = ''
                
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    
                    if agent == number_of_agents-1:
                        Eval,_ = value(new_state,depth+1,0)
                        
                    else:
                        Eval,_ = value(new_state,depth,agent+1)
                    
                    #Eval stores the evaluation score
                    if Eval < v :
                        best_action = possible_action
                        v = Eval
            
            
                        
            return (v,best_action)
        
        _, action = value(gameState,0,0)
        
        return action
                        
                        
                
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        depth = 0
        number_of_agents = gameState.getNumAgents()
        inf = 10000000000000.0       # Variable for infinity
        
        def value(state,depth,agent,alpha,beta):
            
            
            
            #print("depth:",depth," agent:",agent)
            
            # Check if we have reached the depth
            if depth == self.depth:
                return (self.evaluationFunction(state),0)
            
            # Check if there are NO legal actions
            if not state.getLegalActions(agent):
                return (self.evaluationFunction(state),0)
            
            
                
            if agent == self.index:
                # when agent is equal to 0 
                
                v = -1*inf
                best_action = ''
                
                
                # The following code will work if MINIMIZERS Cooperate
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    
                    Eval,_ = value(new_state,depth,agent+1,alpha,beta)
                    
                    if Eval > v :
                        best_action = possible_action
                        v = Eval
                    # Check if we need prunning
                    if v > beta:
                        return (v,best_action)
                    # updating alpha value
                    alpha = max(alpha,v)
                    
                            
            else:
                # If the current agent is ghost
                
                v = inf
                best_action = ''
                
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    
                    if agent == number_of_agents-1:
                        Eval,_ = value(new_state,depth+1,0,alpha,beta)
                        
                    else:
                        Eval,_ = value(new_state,depth,agent+1,alpha,beta)
                    
                    #Eval stores the evaluation score
                    if Eval < v :
                        best_action = possible_action
                        v = Eval
                    
                    # Check if we need pruning
                    if v < alpha:
                        return (v,best_action)
                    
                    # Updating Beta value
                    beta = min(beta,v)
            
            
                        
            return (v,best_action)
        
        _, action = value(gameState,0,0,alpha = (-1*inf),beta = inf)
        
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        depth = 0
        number_of_agents = gameState.getNumAgents()
        inf = 10000000000000.0        # Variable defining infinity
        
        def value(state,depth,agent):
            
            
            # Check if we have reached the depth
            if depth == self.depth:
                return (self.evaluationFunction(state),0)
            
            # Check if there are NO legal actions
            if not state.getLegalActions(agent):
                return (self.evaluationFunction(state),0)
            
            
                
            if agent == self.index:
                # when agent is equal to 0 
                
                v = -1*inf
                best_action = ''
                
                
                # The following code will work if MINIMIZERS Cooperate
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    
                    Eval,_ = value(new_state,depth,agent+1)
                    if Eval > v :
                        best_action = possible_action
                        v = Eval
                            
            else:
                # If the current agent is ghost
                
                v = 0
                best_action = ''
                
                for possible_action in state.getLegalActions(agent):
                    new_state = state.generateSuccessor(agent,possible_action)
                    
                    if agent == number_of_agents-1:
                        # Last agent
                        Eval,_ = value(new_state,depth+1,0)
                        
                    else:
                        Eval,_ = value(new_state,depth,agent+1)
                    
                    #Eval stores the evaluation score
                    v += Eval
                
                #Lets normalize for probability
                v = v/len(state.getLegalActions(agent))
            
            
                        
            return (v,best_action)
        
        _, action = value(gameState,0,0)
        
        return action
        
    
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    '''
    ---------------------------------------------------------------------------
    DESCRIPTION:
    ---------------------------------------------------------------------------
    This Evaluation function has bee created by using following ideas:
        
        The food closest to the Pacman must be given the highest weightage and
        Pacman must move towards the closest food item.
        
        If Pacman has NOT eaten the Power Pallet, then the Pacman must give
        highest weightage to the closest ghost and move away from the closest 
        ghost.
        
        If Pacman has NOT eaten the Power Pallet and the closest ghost is 
        farther than a distance of 10, then we ignore the presence of ghost in
        the game for this state.
        
        If Pacman has eaten the Power Pallet and the scare time of a particular
        ghost is more than 4, then we should run behind that scared ghost.
        
        If Pacman is closer to the Power pallet by a value of 4, then the Pacman 
        must focus on the Power pallet as well.
        
        Check if any of the ghost is scared. If any of the ghost is scared, then
        we raise a flag. This flag is included in the evaluation function to 
        encourage Pacman to scare the ghost
        
    The evaluation functions is made up of addition of parameters which implement
    the above given ideas.
    
    For any querries related to any part of the code contact at shanbhag.d@northeastern.edu
    
    '''
    
    # Pacman pasition
    Pacman_position = currentGameState.getPacmanPosition()
    # Food and Power pallet
    Food_pallet = currentGameState.getFood()
    Power_pallet = currentGameState.getCapsules()
    # Ghost Data
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    GhostPosition = currentGameState.getGhostPositions()
    
    
    # Calculating food distance with more priority to closest food pallet
    food_dist = []             # Stores distance of Pacman from all of the food
    food_to_go_for = 0         # Wighted distance of the food items
    
    for i in Food_pallet.asList():
        food_dist.append(manhattanDistance(Pacman_position,i))
        if food_dist[-1] == 0:
            food_to_go_for = 0
        else:
            food_to_go_for += 1/(food_dist[-1])
            
    
    # Calculating ghost distance with more priority to closest ALIVE ghost 
    ghost_dist = []            # Stores distance of Pacman from all of the ghost
    ghost_to_run_from = 0      # Wighted distance of the ghosts which are NOT scared
    ghost_to_run_towards = 0   # Wighted distance of the scared ghosts
    is_ghost_scared = 0        # Updates the number of ghosts which are scared
    
    for i in GhostPosition:
        ghost_dist.append(manhattanDistance(Pacman_position,i))
        # We need to have weghted average of distance from the ghost
        # more the distance from closest ghost the better
        
        if newScaredTimes[len(ghost_dist)-1] == 0:
            # This particular Ghost is not scared
            if ghost_dist[-1] !=0:
                ghost_to_run_from -= 1/ghost_dist[-1]
            if min(ghost_dist) > 10:
                ghost_to_run_from = 0
        else:
            #This particular ghost is scared
            is_ghost_scared = 1
            if newScaredTimes[len(ghost_dist)-1] > 4:
                if ghost_dist[-1] !=0:
                    ghost_to_run_towards += 1/ghost_dist[-1]
          
            
    # Calculating distance from power Pallet
    pallet_dist = []           #Stores distance of Pacman from all of the Power pallet
    go_behind_pallet = 0       # weighted distance from the closest power pallet
    
    for i in Power_pallet:
        # Calculate the distance from particular power pallet
        pallet_dist.append(manhattanDistance(Pacman_position,i))
        
        if pallet_dist[-1] <= 4 and pallet_dist[0]>0:
            #If the pallet is closer than 4
            go_behind_pallet = 1/(pallet_dist[-1])
        else:
            # If the pallet is farther than 4
            go_behind_pallet = 0
                
    
    
    # Fetching the score of current state, this score is based on how many food
    # items are consumed and negative one for each move made
    SGSS = currentGameState.getScore()
    
    # Defining Evaluation function    
    Eval_func = 0
    # All the parameters are equally weighted
    Eval_func += (1*SGSS) + (1*food_to_go_for) + (1*ghost_to_run_from) 
    Eval_func += (1*go_behind_pallet) + (1*ghost_to_run_towards)
    Eval_func += (1*is_ghost_scared)
    
    return Eval_func
        
# Abbreviation
better = betterEvaluationFunction
