import random

HEIGHT = 15
WIDTH = 41

def printmaze(maze):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i % 2 == 1 and j % 2 == 1:
                print(maze[i][j].name,end='')
            else:
                print(maze[i][j], end ='')

        print()

class room():
    def __init__(self,x,y):
        self.visited = False
        self.x = x
        self.y = y
        self.name = "R"
        self.neighbour = []

def initmaze(maze):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i % 2 == 1 and j % 2 == 1:
                newRoom = room(i,j)
                maze[i][j] = newRoom
    return maze


def buildneighbour(maze):
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if i % 2 == 1 and j % 2 == 1:
                currentRoom = maze[i][j]
                neighbour = []

                if(i - 2) > 0:
                    neighbour.append(maze[i-2][j])
                if(j - 2) > 0:
                    neighbour.append(maze[i][j-2])
                if (i + 2) < HEIGHT:
                    neighbour.append(maze[i + 2][j])
                if (j + 2) < WIDTH:
                    neighbour.append(maze[i][j + 2])

                currentRoom.neighbour = neighbour
    return maze

def visitRoom(curRoom,maze):

    curRoom.visited = True
    curRoom.name = " "
    random.shuffle(curRoom.neighbour)

    for room in curRoom.neighbour:

        if room.visited == False:
            maze = visitRoom(room,maze)

    return maze




maze = [['W' for i in range(WIDTH)]for j in range(HEIGHT)]
maze = initmaze(maze)
maze = buildneighbour(maze)
maze = visitRoom(maze[1][1],maze)
printmaze(maze)
