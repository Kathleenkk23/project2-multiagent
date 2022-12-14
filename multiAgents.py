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


from cmath import inf
from operator import index
from pacman import GameState
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


def getFoodList(foodGrid):
    foodList = []
    for i in range(foodGrid.width):
        for j in range(foodGrid.height):
            if foodGrid[i][j]:
                foodList.append((i,j))
    return foodList

def getClosestDist(position, lst):
    if len(lst) > 0:
        return min(abs(i[0] - position[0]) + abs(i[1] - position[1]) for i in lst)
    else:
        return float('inf')


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


        minFoodDist = getClosestDist(newPos, getFoodList(currentGameState.getFood()))  
        lstGhost = list(state.getPosition() for state in newGhostStates)
        minGhostDist = getClosestDist(newPos,lstGhost)
        # print(f"{minFoodDist} {minGhostDist}")
        if minGhostDist < 4 and minGhostDist != 0:
            ghostscore = -11 / minGhostDist
        else:
            ghostscore = 0

        if minFoodDist == 0:
            foodscore = 0.01
        else:
            foodscore = 10 / minFoodDist
        return successorGameState.getScore() + foodscore + ghostscore

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


def maxV(gamestate, depth, slf, idx):

        if depth==slf.depth or len(gamestate.getLegalActions(0))==0:
            return slf.evaluationFunction(gamestate)
        if gamestate.isLose():
            return -1
        elif gamestate.isWin():
            return 1
        v = float('-inf')
        for successor in gamestate.getLegalActions(0):
            v = max(v, minV(gamestate.generateSuccessor(idx,successor), depth, slf, 1))
        
        return v 
        
def minV(gamestate, depth, slf, idx):
        if depth==slf.depth or len(gamestate.getLegalActions(idx))==0:
            return slf.evaluationFunction(gamestate)
        if gamestate.isLose():
            return -1
        elif gamestate.isWin():
            return 1
        v = float('inf')
        for successor in gamestate.getLegalActions(idx):
            if idx == gamestate.getNumAgents()-1:
                v = min(v, maxV(gamestate.generateSuccessor(idx,successor), depth+1, slf, 0))
            else:
                v = min(v, minV(gamestate.generateSuccessor(idx,successor), depth, slf, idx+1))

        return v

def abmaxV(gamestate, depth, slf, idx, alpha, beta):

        if depth==slf.depth or len(gamestate.getLegalActions(0))==0:
            return slf.evaluationFunction(gamestate)
        if gamestate.isLose():
            return -1
        elif gamestate.isWin():
            return 1
        v = float('-inf')
        for successor in gamestate.getLegalActions(0):
            v = max(v, abminV(gamestate.generateSuccessor(idx,successor), depth, slf, 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)

        return v 
        
def abminV(gamestate, depth, slf, idx, alpha, beta):
        if depth==slf.depth or len(gamestate.getLegalActions(idx))==0:
            return slf.evaluationFunction(gamestate)
        if gamestate.isLose():
            return -1
        elif gamestate.isWin():
            return 1
        v = float('inf')
        for successor in gamestate.getLegalActions(idx):
            if idx == gamestate.getNumAgents()-1:
                v = min(v, abmaxV(gamestate.generateSuccessor(idx,successor), depth+1, slf, 0, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            else:
                v = min(v, abminV(gamestate.generateSuccessor(idx,successor), depth, slf, idx+1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
        return v
    
    
def expmaxV(gamestate, depth, slf, idx):

        if depth==slf.depth or len(gamestate.getLegalActions(0))==0:
            return slf.evaluationFunction(gamestate)
        if gamestate.isLose():
            return -1
        elif gamestate.isWin():
            return 1
        v = float('-inf')
        for successor in gamestate.getLegalActions(0):
            v = max(v, expV(gamestate.generateSuccessor(idx,successor), depth, slf, 1))
        
        return v 
    
def expV(gamestate, depth, slf, idx):
        if depth==slf.depth or len(gamestate.getLegalActions(idx))==0:
            return slf.evaluationFunction(gamestate)
        if gamestate.isLose():
            return -1
        elif gamestate.isWin():
            return 1
        v = 0
        length = len(gamestate.getLegalActions(idx))
        for successor in gamestate.getLegalActions(idx):
            if idx == gamestate.getNumAgents()-1:
                v += expmaxV(gamestate.generateSuccessor(idx,successor), depth+1, slf, 0)/length
            else:
                v += expV(gamestate.generateSuccessor(idx,successor), depth, slf, idx+1)/length
        return v
    
    
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


        "Add more of your code here if you want to"

        if (gameState.isWin()):
            return
        returning = float('-inf')
        bestAction = None 
        for actions in gameState.getLegalActions(0):
            maxv = minV(gameState.generateSuccessor(0, actions), 0, self, 1)
            if maxv>returning:
                bestAction = actions
                returning = maxv
        
        return bestAction
        #util.raiseNotDefined()
 

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #from minmax
        if (gameState.isWin()):
            return
        returning = float('-inf')
        bestAction = None
        alpha = float('-inf')
        beta = float('inf')
        for actions in gameState.getLegalActions(0):
            maxv = abminV(gameState.generateSuccessor(0, actions), 0, self, 1, alpha, beta)
            if maxv>returning:
                bestAction = actions
                returning = maxv
            if maxv > beta:
                return maxv
            alpha = max(alpha, maxv)
            
        return bestAction
        

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
        if (gameState.isWin()):
            return
        returning = float('-inf')
        bestAction = None 
        for actions in gameState.getLegalActions(0):
            maxv = expV(gameState.generateSuccessor(0, actions), 0, self, 1)
            if maxv>returning:
                bestAction = actions
                returning = maxv
        
        return bestAction
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I have effectively just copied my evaluation function from above and renamed some variables.
    ghostScore is inversely related with the distance to the CLOSEST ghost. ghostScore is 0 if the ghost is at least 4 blocks away.

    foodScore is inversely proportional to the distance of the closest food pellet.

    The final value returned is a num of the state's getScore() function, foodScore, and ghostScore.
    """
    "*** YOUR CODE HERE ***"
    currPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood()
    currGhostStates = currentGameState.getGhostStates()
    currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]


    minFoodDist = getClosestDist(currPos, getFoodList(currentGameState.getFood()))  
    lstGhost = list(state.getPosition() for state in currGhostStates)
    minGhostDist = getClosestDist(currPos,lstGhost)
    # print(f"{minFoodDist} {minGhostDist}")
    if minGhostDist < 4 and minGhostDist != 0:
        ghostscore = -10 / minGhostDist
    else:
        ghostscore = 0

    if minFoodDist == 0:
        foodscore = 0
    else:
        foodscore = 9 / minFoodDist
    if len(currFood.asList()) == 0:
        foodscore = 0

    return currentGameState.getScore() + foodscore + ghostscore + sum(currScaredTimes)

# Abbreviation
better = betterEvaluationFunction
