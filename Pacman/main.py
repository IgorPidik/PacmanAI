__author__ = 'igor'

import pygame
from Game import Game
from Agent import *
from Util import *
import copy
import datetime
import argparse

parser = argparse.ArgumentParser(description='Set algorithm and maze.')
parser.add_argument("-a", dest="algorithm", required=True,
                    help="algorithm name", type=str)
parser.add_argument("-m", dest="maze", required=True,
                    help="maze filename", type=str)

def setMaze(mazeArg, game):
    mazeBig = [
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
        "%......o.....%%............%",
        "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
        "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
        "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
        "%..........................%",
        "%.%%%%.%%.%%%%%%%%.%%.%%%%.%",
        "%.%%%%.%%.%%%%%%%%.%%.%%%%.%",
        "%......%%....%%....%%......%",
        "%%%%%%.%%%%% %% %%%%%.%%%%%%",
        "%%%%%%.%%%%% %% %%%%%.%%%%%%",
        "%%%%%%.%            %.%%%%%%",
        "%%%%%%.% %%%%  %%%% %.%%%%%%",
        "%     .  %        %  .     %",
        "%%%%%%.% %%%%%%%%%% %.%%%%%%",
        "%%%%%%.%            %.%%%%%%",
        "%%%%%%.% %%%%%%%%%% %.%%%%%%",
        "%............%%............%",
        "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
        "%.%%%%.%%%%%.%%.%%%%%.%%%%.%",
        "%...%%.......  .......%%...%",
        "%%%.%%.%%.%%%%%%%%.%%.%%.%%%",
        "%%%.%%.%%.%%%%%%%%.%%.%%.%%%",
        "%......%%....%%....%%......%",
        "%.%%%%%%%%%%.%%.%%%%%%%%%%.%",
        "%.............P............%",
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    ]
    mazeSmall = [
        "%%%%%%%%%%%%%%%%%%%%",
        "%......%   G%......%",
        "%.%%...%%  %%...%%.%",
        "%.%..%...P....%..%.%",
        "%.%%.%.%%%%%%.%.%%.%",
        "%..................%",
        "%%%%%%%%%%%%%%%%%%%%"
    ]
    point = ""
    maze = None
    size = 0,0
    if mazeArg == "small":
        size = len(mazeSmall[0])*20, len(mazeSmall)*20,
        maze = mazeSmall
        point = "."
    elif mazeArg == "big":
        size = len(mazeBig[0])*20, len(mazeBig)*20
        maze = mazeBig
        point = "o"

    x = y = 0
    radius = 4
    for row in maze:
        x = 0 #offset
        for column in row:
            if column == "%":
                game.addWall((x, y))
                x += 20
            elif column == point:
                game.addFood((x, y))
                x += 20
            elif column == "P":
                game.addAgent((x, y))
                x += 20
            elif column == "G":
                game.addFood((x, y))
                game.addAgent((x, y), False)
                x += 20
            else:
                x += 20

        y += 20
    return size

def runAlgorithm(alghorithm, game):
    running = True
    if alghorithm == "dfs":
        print 'dfs'
        dfs = DeepFistSearch()
        dfs.setProblem(game)
        moves = dfs.getPlan()
        while len(moves) > 0 and running:
            clock.tick(5)
            gameDisplay.fill((0, 0, 0))
            action = moves.pop(0)
            game.getPacman().makeMove(action)
            game.draw(gameDisplay)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    elif alghorithm == "bfs":
        print 'bfs'
        bfs = BreadthFirstSearch()
        bfs.setProblem(game)
        moves = bfs.getPlan()
        while len(moves) > 0 and running:
            clock.tick(5)
            gameDisplay.fill((0, 0, 0))
            action = moves.pop(0)
            game.getPacman().makeMove(action)
            game.draw(gameDisplay)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    elif alghorithm == "ucs":
        print 'uniform'
        uniform = UniformCostSearch()
        uniform.setProblem(game)
        moves = uniform.getPlan()
        while len(moves) > 0 and running:
            clock.tick(5)
            gameDisplay.fill((0, 0, 0))
            action = moves.pop(0)
            game.getPacman().makeMove(action)
            game.draw(gameDisplay)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    elif alghorithm == "astar":
        print 'astar'
        astar = AStar()
        astar.setProblem(game)
        moves = astar.getPlan()
        while len(moves) > 0 and running:
            clock.tick(5)
            gameDisplay.fill((0, 0, 0))
            action = moves.pop(0)
            game.getPacman().makeMove(action)
            game.draw(gameDisplay)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    elif algorithm == "minimax":
        minimax = Minimax()

        while running:
            clock.tick(5)
            gameDisplay.fill((0, 0, 0))
            action = minimax.getAction(game)
            if not action == None:
                game.getPacman().makeMove(action)
                game.draw(gameDisplay)
                pygame.display.update()
            else:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    elif algorithm == "expectionmax":
        print 'expection max'
        expMax = ExpectionMax()

        while running:
            clock.tick(5)
            gameDisplay.fill((0, 0, 0))
            action = expMax.getAction(game)
            if not action == None:
                game.getPacman().makeMove(action)
                game.draw(gameDisplay)
                pygame.display.update()
            else:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False





args = parser.parse_args()
algorithm = args.algorithm
maze = args.maze

game = Game()


pygame.init()

gameDisplay = pygame.display.set_mode((0,0))
size = setMaze(maze, game)
gameDisplay = pygame.display.set_mode(size)
print ('size', size)

gameDisplay.fill((0, 0, 0))
clock = pygame.time.Clock()

game.draw(gameDisplay)
pygame.display.update()



# while not len(moves) == 0:
#     clock.tick(5)
#     gameDisplay.fill((0, 0, 0))
#     action = moves.pop(0)
#     game.getPacman().makeMove(action)
#     game.draw(gameDisplay)
#     pygame.display.update()

runAlgorithm(algorithm, game)
running = True

pygame.quit()
quit()

