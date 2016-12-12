__author__ = 'igor'

class List(object):
    def __init__(self):
        self.list = []

    def pop(self, index=-1):
        return self.list.pop()

    def append(self, x):
        self.list.append(x)

    def remove(self, index):
        self.list.remove(index)

    def __contains__(self, item):

        for cItem in self.list:
            if cItem.getPacmanPos() == item.getPacmanPos() and cItem.getFoodPositions() == item.getFoodPositions():
                return True
        return False


class Queue(object):
    def __init__(self):
        self.list = []

    def isEmpty(self):
        if len(self.list) == 0:
            return True
        return False

    def append(self, x):
        self.list.append(x)

    def pop(self, x=-1):
        minVal = float('inf')
        minIndex = x
        for index in range(0, len(self.list)):
            (actions, game, cost) = self.list[index]
            if (len(actions)) < minVal:
                minIndex = index
                minVal = len(actions)
        return self.list.pop(minIndex)


class PriorityQueue(object):
    def __init__(self):
        self.list = []

    def isEmpty(self):
        if len(self.list) == 0:
            return True
        return False

    def append(self, x, priority):
        self.list.append((x, priority))

    def pop(self, x=-1):
        minPriority = float('inf')
        minIndex = x
        for index in range(0, len(self.list)):
            (properties, priority) = self.list[index]
            if priority < minPriority:
                minIndex = index
                minPriority = priority
        return self.list.pop(minIndex)[0]


def manhattanDistance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)

def wallsInWay(pos1, pos2, gameState):
    # doesn't work
    counter = 0
    def isWall(wallX, wallY):
        for x in range(pos1[0], pos2[0]):
            for y in range(pos1[1], pos2[1]):
                if x in range(wallX, wallX+20) and y in range(wallY, wallY+20):
                    print 'wall'
                    return 1
        return 0
    for (wallX, wallY) in gameState.getWallPositions():
        counter += isWall(wallX, wallY)
    return counter


