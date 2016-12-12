from struct import pack

__author__ = 'igor'

from Util import *
import operator


class DeepFistSearch(object):
    def __init__(self):
        self.game = None

    def setProblem(self, game):
        self.game = game

    def getPlan(self):
        if not self.game:
            raise 'problem is not set, call setProblem(gameObject)'
        states = []
        states.append((["STOP"], self.game, 0))
        expanded = List()
        numState = 0
        while not len(states) == 0:
            move, state, cost = states.pop()
            if state not in expanded:
                numState += 1
                expanded.append(state)
                if state.isTerminal():
                    move.remove('STOP')
                    return move
                for (action, nextState, nextCost) in state.getSuccessorsForPacman(True):
                    states.append((move + [action], nextState, cost + nextCost))


class BreadthFirstSearch(object):
    def __init__(self):
        self.game = None

    def setProblem(self, game):
        self.game = game

    def getPlan(self):
        if not self.game:
            raise 'problem is not set, call setProblem(gameObject)'
        states = Queue()
        states.append((["STOP"], self.game, 0))
        expanded = List()

        while not states.isEmpty():
            move, state, cost = states.pop()
            if state not in expanded:
                expanded.append(state)
                if state.isTerminal():
                    print 'success'
                    move.remove('STOP')
                    return move
                for (action, nextState, nextCost) in state.getSuccessorsForPacman(True):
                    states.append((move + [action], nextState, cost + nextCost))
        print 'failure'

    def getPlanForMiniMax(self, point, gameState):
        states = Queue()
        states.append((["STOP"], gameState, 0))
        expanded = List()

        while not states.isEmpty():
            move, state, cost = states.pop()
            if state not in expanded:
                expanded.append(state)
                pacPos = state.getPacmanPos()
                if point == pacPos:
                    print 'success'
                    move.remove('STOP')
                    return len(move)
                for (action, nextState, nextCost) in state.getSuccessorsForPacman():
                    states.append((move + [action], nextState, cost + nextCost))
        print 'failure'


class UniformCostSearch(object):
    def __init__(self):
        self.game = None

    def setProblem(self, game):
        self.game = game

    def getPlan(self):
        if not self.game:
            raise 'problem is not set, call setProblem(gameObject)'
        states = PriorityQueue()
        states.append((["STOP"], self.game, 0), 0)
        expanded = List()

        while not states.isEmpty():
            move, state, cost = states.pop()
            if state not in expanded:
                expanded.append(state)
                if state.isTerminal():
                    move.remove('STOP')
                    return move
                for (action, nextState, nextCost) in state.getSuccessorsForPacman(True):
                    states.append((move + [action], nextState, cost + nextCost), cost + nextCost)


class AStar(object):
    def __init__(self):
        self.game = None

    def setProblem(self, game):
        self.game = game

    def getPlan(self):
        if not self.game:
            raise 'problem is not set, call setProblem(gameObject)'
        states = PriorityQueue()
        states.append((["STOP"], self.game, 0), 0)
        expanded = List()

        while not states.isEmpty():
            move, state, cost = states.pop()
            if state not in expanded:
                expanded.append(state)
                if state.isTerminal():
                    move.remove('STOP')
                    return move
                for (action, nextState, nextCost) in state.getSuccessorsForPacman(True):
                    states.append((move + [action], nextState, cost + nextCost),
                                  cost + nextCost + self.heuristic(state))

    def heuristic(self, game):
        minDistance = float('inf')
        pacmanPos = game.getPacmanPos()
        for foodPos in game.getFoodPositions():
            distance = manhattanDistance(pacmanPos, foodPos)
            if distance < minDistance:
                minDistance = distance
        return minDistance / 20

    def getPlanForMiniMax(self, point, gameState):
        states = PriorityQueue()
        states.append((["STOP"], gameState, 0), 0)
        expanded = List()

        while not states.isEmpty():
            move, state, cost = states.pop()
            if state not in expanded:
                expanded.append(state)
                pacPos = state.getPacmanPos()
                if pacPos == point:
                    move.remove('STOP')
                    return len(move)
                for (action, nextState, nextCost) in state.getSuccessorsForPacman():
                    states.append((move + [action], nextState, cost + nextCost),
                                  cost + nextCost + self.heuristic(state))


class Minimax(object):
    def __init__(self):
        self.pacmanIndex = 0
        self.depth = 1
        self.bfs = BreadthFirstSearch()
        self.astar = AStar()

    def getAction(self, gameState):
        depth = self.depth * gameState.getNumAgents()
        (val, action) = self.minimax(gameState, depth, 0)
        print ('choosen action ', action)
        print '######################################'
        return action

    def minimax(self, gameState, depth, player):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalFunction(gameState, self.bfs), None

        if player == 0 or player == gameState.getNumAgents():
            player = 0
            maxVal = -float('inf')
            maxAction = None
            for action in gameState.getLegalActions(player):
                successor = gameState.getSuccessorForMiniMax(player, action)
                (val, move) = self.minimax(successor, depth - 1, player + 1)
                print('val', val, 'action ', action)
                if val >= maxVal:
                    maxVal = val
                    maxAction = action
            return (maxVal, maxAction)
        elif (player + 1) == gameState.getNumAgents():
            minVal = float('inf')
            minAction = None
            for action in gameState.getLegalActions(player):
                successor = gameState.getSuccessorForMiniMax(player, action)
                (val, move) = self.minimax(successor, depth - 1, 0)
                if val <= minVal:
                    minVal = val
                    minAction = action
            return (minVal, minAction)
        else:
            minVal = float('inf')
            minAction = None
            for action in gameState.getLegalActions(player):
                successor = gameState.getSuccessorForMiniMax(player, action)
                (val, move) = self.minimax(successor, depth - 1, player + 1)
                if val <= minVal:
                    minVal = val
                    minAction = action
            return (minVal, minAction)

class ExpectionMax(object):
    def __init__(self):
        self.pacmanIndex = 0
        self.depth = 1
        self.bsf = BreadthFirstSearch()

    def getAction(self, gameState):
        val, action = self.expectionMax(gameState, self.depth, self.pacmanIndex)
        print ('val', val, 'action', action)
        return action

    def expectionMax(self, gameState, depth, player):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return evalFunction(gameState, self.bsf), None

        if player == 0 or player == gameState.getNumAgents():
            player = 0
            maxVal = -float('inf')
            maxAction = None
            for action in gameState.getLegalActions(player):
                successor = gameState.getSuccessorForMiniMax(player, action)
                val, move = self.expectionMax(successor, depth-1, player+1)
                if val > maxVal:
                    maxAction = action
                    maxVal = val
            return maxVal, maxAction
        elif (player +1) == gameState.getNumAgents():
            average = 0
            actionsNum = len(gameState.getLegalActions(player))
            expAction = None
            for action in gameState.getLegalActions(player):
                successor = gameState.getSuccessorForMiniMax(player, action)
                val, move = self.expectionMax(successor, depth-1, 0)
                average += val
                expAction = move
            return (average/actionsNum), expAction
        else:
            average = 0
            actionsNum = len(gameState.getLegalActions(player))
            expAction = None
            for action in gameState.getLegalActions(player):
                successor = gameState.getSuccessorForMiniMax(player, action)
                val, move = self.expectionMax(successor, depth-1, player+1)
                average += val
                expAction = move
            return (average/actionsNum), expAction



def evalFunction(gameState, bfs):
    if gameState.isWin():
        return float('inf')
    if gameState.isLose():
        return -float('inf')
    score = gameState.getScore()
    pacPos = gameState.getPacmanPos()
    distances = []
    for food in gameState.getFoodPositions():
        distances.append((food, manhattanDistance(pacPos, food)))
    distances.sort(key=operator.itemgetter(1))
    minDistance = float('inf')
    if len(distances) > 2:
        for index in range(2):
            (pos, dis) = distances[index]
            distance = bfs.getPlanForMiniMax(pos, gameState)
            if distance < minDistance:
                minDistance = distance
    else:
        for (pos, dis) in distances:
            distance = bfs.getPlanForMiniMax(pos, gameState)
            if distance < minDistance:
                minDistance = distance

    score -= (minDistance)
    score -= 3 * (len(gameState.getFoodPositions()))

    print(score, 'score')
    return score


