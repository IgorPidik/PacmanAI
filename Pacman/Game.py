__author__ = 'igor'

import pygame
from random import randrange
import copy


class Game(object):
    def __init__(self):
        self.walls = []
        self.food = []
        self.agents = []
        self.score = 0
        self.pacman = None
        self.ghosts = []
        self.agents = []
        self.pacmanAlive = True


    def addWall(self, position):
        self.walls.append(position)

    def addFood(self, position):
        x, y = position
        self.food.append((x + 10, y + 10))

    def isWall(self, (x, y)):
        for (wallX, wallY) in self.walls:
            if x in range(wallX, wallX + 20) and y in range(wallY, wallY + 20):
                return True
        return False

    def isFood(self, position):
        for food in self.food:
            if food == position:
                return True
        return False

    def drawWall(self, screen):
        for (x, y) in self.walls:
            pygame.draw.rect(screen, (30, 144, 255), (x, y, 17, 17), 3)

    def getWallPositions(self):
        return self.walls

    def getFoodPositions(self):
        return self.food

    def removeFood(self, position):
        if position in self.food:
            self.food.remove(position)
        else:
            raise "error in removeFood(): no food with that position"

    def drawFood(self, screen):
        for position in self.food:
            pygame.draw.circle(screen, (255, 255, 255), position, 3)

    def addAgent(self, position, pacman=True):
        if pacman:
            pacman = Agent(position, self)
            self.pacman = pacman
        else:
            ghost = Agent(position, self, False)
            self.ghosts.append(ghost)

    def draw(self, screen):
        self.drawWall(screen)
        self.drawFood(screen)
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.makeRandomMove()
            ghost.draw(screen)

    def getGhosts(self):
        return self.ghosts

    def getGhost(self, index):
        return self.ghosts[index]

    def getPacman(self):
        return self.pacman

    def getPacmanPos(self):
        return self.pacman.getTruePosition()

    def getNumAgents(self):
        return (len(self.ghosts)+1) # len of ghost list + pacman

    def pacmanGhostColide(self):
        for ghost in self.ghosts:
            ghostPos = ghost.getPos()
            ghostSize = ghost.getSize()
            pacmanPos = self.pacman.getPos()
            if (pacmanPos[0] in range(ghostPos[0], ghostPos[0] + ghostSize)) and \
                    (pacmanPos[1] in range(ghostPos[1], ghostPos[1] + ghostSize)):
                return True
        return False

    def getSuccessorsForPacman(self, eat=False):
        successors = []
        for action in self.getPacman().getPossibleMoves():
            game = copy.deepcopy(self)
            game.getPacman().makeMove(action, eat)
            successors.append((action, game, 1))
        return successors



    def getSuccessorForMiniMax(self, agentIndex, action):
        agent = None
        successor = copy.deepcopy(self)
        if agentIndex == 0:
            agent = successor.getPacman()
        else:
            agent = successor.getGhost((agentIndex-1))
        agent.makeMove(action)
        return successor

    def getLegalActions(self, agent):
        if agent == 0:
            return self.getPacman().getPossibleMoves()
        else:
            return self.getGhost((agent-1)).getPossibleMoves()

    def isTerminal(self):
        if len(self.food) == 0:
            return True
        return False

    def isWin(self):
        if self.isTerminal() and self.pacmanAlive:
            return True
        return False

    def isLose(self):
        if not self.pacmanAlive:
            return True
        return False

    def increaseScore(self, val):
        self.score += val

    def getScore(self):
        return self.score


class Agent(object):
    def __init__(self, position, game, pacman=True):
        self.isPacman = pacman
        self.action = None
        self.game = game
        self.position = position
        self.size = 20
        self.actions = ["N", "S", "E", "W"]
        self.previousRotation = 0
        if pacman:
            self.image = pygame.image.load("images/pacman.png").convert()
        else:
            self.image = pygame.image.load("images/ghost-red.png").convert()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def getSize(self):
        return self.size

    def getPos(self):
        return self.position

    def getTruePosition(self):
        x, y = self.position
        return (x + self.size / 2, y + self.size / 2)


    def draw(self, gameScreen):
        if self.isPacman:
            self.image = pygame.transform.rotate(self.image, -self.previousRotation)
            if self.action == self.actions[0]:
                self.image = pygame.transform.rotate(self.image, 90)
                self.previousRotation = 90
            elif self.action == self.actions[1]:
                self.image = pygame.transform.rotate(self.image, -90)
                self.previousRotation = -90
            elif self.action == self.actions[2]:
                self.previousRotation = 0
                pass
            elif self.action == self.actions[3]:
                self.image = pygame.transform.rotate(self.image, 180)
                self.previousRotation = 180
        gameScreen.blit(self.image, self.position)

    def getPossibleMoves(self):
        possibleMoves = []
        for action in self.actions:
            if not self.game.isWall(self.posAfterAction(action)):
                possibleMoves.append(action)
        return possibleMoves

    def makeMove(self, action, eatFood=True):
        self.action = action
        self.position = self.posAfterAction(action)
        x, y = self.position
        if self.game.pacmanGhostColide():
            self.game.pacmanAlive = False
        else:
            self.game.pacmanAlive = True

        if eatFood and self.isPacman and self.game.isFood((x + self.size / 2, y + self.size / 2)):
            self.game.increaseScore(100)
            self.game.removeFood((x + self.size / 2, y + self.size / 2))
        self.game.increaseScore(-20)

    def makeRandomMove(self):
        possibleMoves = self.getPossibleMoves()
        move = possibleMoves[randrange(0, len(possibleMoves))]
        self.makeMove(move)

    def posAfterAction(self, action):
        if action == "N":
            return self.moveN()

        if action == "S":
            return self.moveS()

        if action == "E":
            return self.moveE()

        if action == "W":
            return self.moveW()

        if action == "STOP":
            return self.position

    def moveN(self):
        x, y = self.position
        return x, y - self.size

    def moveS(self):
        x, y = self.position
        return x, y + self.size

    def moveE(self):
        x, y = self.position
        return x + self.size, y

    def moveW(self):
        x, y = self.position
        return x - self.size, y

