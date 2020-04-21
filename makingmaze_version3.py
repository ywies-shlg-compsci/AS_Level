import random

class cell:
    def __init__(self,row,col, rowSize, colSize, relRow, relCol, name):
        self.visited = False
        self.rowPos = row # this is the upper left hand corner of the room (which could be bigger than 1 cell)
        self.colPos = col
        self.rowSize=rowSize
        self.colSize= colSize
        self.cells = []
        self.neighbours = []
        self.name = name
        #self.name = "r:" + str(self.rowPos) + " c: " + str(self.colPos) + name

    def addCell(self, row, col):
        self.cells.append((row, col))
class room:
    def __init__(self,x,y):
        self.visited = False
        self.xPos = x
        self.yPos = y
        self.neighbours = None
        self.name = "R"

    def setNeighbours(self, neighbours):
        self.neighbours = neighbours

    #def printNeighbour(self):
        #print("Number of Neighbours: ", len(self.neighbours))
        #for node in self.neighbours:
            #print("X Pos: ", node.xPos, "Y Pos: ", node.yPos)

iSize = 15
jSize = 40
room1x1 = ["R"]
room2x2 = [ ["R", "R"],["R", "R"]]
room3x3 = [ ["R", "R", "R"],["R", "R", "R"], ["R", "R", "R"]]
room3x2 = [ ["R", "R", "R"],["R", "R", "R"] ]
room2x3 = [ ["R", "R"],["R", "R"], ["R", "R"]]
room4x3 = [ ["R", "R", "R"],["R", "R", "R"], ["R", "R", "R"],["R","R","R"]]
room4x4 = [ ["R", "R", "R","R"],["R", "R", "R","R"], ["R", "R", "R", "R"],["R","R","R","R"]]

allRooms = [room1x1, room2x2, room2x3, room3x2, room3x3, room4x3, room4x4]

def printRoom(room):

    rows = len(room)
    col = len(room[0])

    #for i in range(0 , rows):
        #for j in range(0 , col):
            #print( room[i][j].name, end = '')
        #print()
def initializeMazeWithRooms(maze):
    finished = False
    for i in range(iSize):
        for j in range(jSize):

                #check to see if we are on the edge of the map.  If so put a wall
                if i == 0 or j == 0 or i == iSize -1 or j == jSize -1:
                    wall = cell(i,j,1,1,0,0,"W")
                    maze[i][j] = wall
                    #print(maze[i][j].name)
                #check to see if cell is empty.

                elif  maze[i][j] == " ":
                    #calculate the max size room in this space
                    maxRow = 0
                    maxCol = 0
                    for rows in range(i, iSize):
                        maxRow += 1
                        if maze[i][j] != " ":
                            break

                    for cols in range(j, jSize):
                        maxCol += 1
                        if maze[i][j] != " ":
                            break

                     #now pick a room size ... -for now just 2 x 2 and place it in the current position
                    roomIndex = random.randint(0,len(allRooms)-1)
                    #print("room in: " , roomIndex)
                    choosenRoom = allRooms[roomIndex]

                    maxRoomRowLen = len(choosenRoom)
                    maxRoomColLen = len(choosenRoom[0])
                    negative = - 1
                    while i + maxRoomRowLen  >= iSize or j + maxRoomColLen  >= jSize:
                        #pick a smaller room
                        # remove largest room

                        roomIndex = random.randint(0,len(allRooms) + negative)
                        negative -= 1
                        choosenRoom = allRooms[roomIndex]
                        maxRoomRowLen = len(choosenRoom)
                        maxRoomColLen = len(choosenRoom[0])
                        #print("can't fit room")
                        # safety
                        if negative < 0:
                            choosenRoom = room1x1
                            maxRoomRowLen = len(choosenRoom)
                            maxRoomColLen = len(choosenRoom[0])
                            #print("neagtive = 0")
                            break

                    room = cell(i,j,maxRoomRowLen,maxRoomColLen,0,0,"R")

                    for roomRow in (range(-1, maxRoomRowLen + 1 )):
                        for roomCol in (range(-1, maxRoomColLen + 1  )):

                            if roomRow == -1 or roomCol == -1 or roomRow == (maxRoomRowLen )  or roomCol== (maxRoomColLen):
                                #print("row: " , roomRow + i, " col: ", roomCol + j)
                                if maze[i + roomRow][j + roomCol] == ' ':
                                    #maze[i + roomRow][j + roomCol] = 'W'
                                    wall = cell(i,j,1,1,0,0,"W")
                                    maze[i+ roomRow][j + roomCol] = wall
                            else:
                                #maze[i + roomRow][j + roomCol] = choosenRoom[roomRow][roomCol]
                                # this is the cell RELATIVE to the position the room is in the maze
                                #room.addCell(roomRow, roomCol)
                                # this is the cell ABSOLUTEto the position the room is in the maze
                                room.addCell(room.rowPos + roomRow, room.colPos + roomCol)
                                maze[i + roomRow][j + roomCol] = room

                    finished = True
                #if finished == True:
                #    break
        #if finished == True:
        #    break

    return maze

#def addNieghbour(maze, cell):
    # check what is in the (row + 2, col) (row, col+ 2) (row - 2, col) (row, col - 2) position
    # first do boundry checking to make sure you aren't accessing a cell outside the boundry
    # If the cell is a "W" in that position, do nothing
    # ELSE If the cell is a "R" in that position
    # check to see if we are still in the same room
    # IF NOT, Check to see if we have already added this neighbour into the neighbour list
    # IF NOT, Add the reference into the neighbour list.

def buildNeighboursBigRoom(maze):
    for row in range(iSize):
        for col in range(jSize):

            currentCell = maze[row][col]
            # if its NOT a wall cell
            if currentCell.name != "W":
                # check what is in the (row + 2, col) (row, col+ 2) (row - 2, col) (row, col - 2) position
                # first do boundry checking to make sure you aren't accessing a cell outside the boundry
                # If the cell is a "W" in that position, do nothing
                # ELSE If the cell is a "R" in that position
                # check to see if we are still in the same room
                # IF NOT, Check to see if we have already added this neighbour into the neighbour list
                # IF NOT, Add the reference into the neighbour list.
                offset = 2
                if row + offset < iSize:
                    potentialNeighbour= maze[row+offset][col]
                    if potentialNeighbour.name == "R":
#                        print(potentialNeighbour, "is == to? " , currentCell)
                        if potentialNeighbour!= currentCell:
                            hasSameNeighbour = False
                            for nbour in currentCell.neighbours:
                                if nbour == potentialNeighbour:
                                    hasSameNeighbour = True

                            if hasSameNeighbour == False:
                                currentCell.neighbours.append(potentialNeighbour)

                if col + offset < jSize:
                    potentialNeighbour= maze[row][col+ offset]
                    if potentialNeighbour.name == "R":
                        #print(potentialNeighbour, "is == to? " , currentCell)
                        if potentialNeighbour!= currentCell:
                            hasSameNeighbour = False
                            for nbour in currentCell.neighbours:
                                if nbour == potentialNeighbour:
                                    hasSameNeighbour = True

                            if hasSameNeighbour == False:
                                currentCell.neighbours.append(potentialNeighbour)
                if row - offset > 0:
                    potentialNeighbour= maze[row-offset][col]
                    if potentialNeighbour.name == "R":
                        #print(potentialNeighbour, "is == to? " , currentCell)
                        if potentialNeighbour!= currentCell:
                            hasSameNeighbour = False
                            for nbour in currentCell.neighbours:
                                if nbour == potentialNeighbour:
                                    hasSameNeighbour = True

                            if hasSameNeighbour == False:
                                currentCell.neighbours.append(potentialNeighbour)
                if col - offset > 0:
                    potentialNeighbour= maze[row][col - offset]
                    if potentialNeighbour.name == "R":
                        #print(potentialNeighbour, "is == to? " , currentCell)
                        if potentialNeighbour!= currentCell:
                            hasSameNeighbour = False
                            for nbour in currentCell.neighbours:
                                if nbour == potentialNeighbour:
                                    hasSameNeighbour = True

                            if hasSameNeighbour == False:
                                currentCell.neighbours.append(potentialNeighbour)

    return maze


def printMazeWithRooms(maze):
    for i in range(iSize):
        for j in range(jSize):
            if maze[i][j] != None:
                    print(maze[i][j].name,end='')
        print()

def printMaze(maze):
    for i in range(iSize):
        for j in range(jSize):
            if i % 2 == 1 and j % 2 == 1 :
                print(maze[i][j].name, end='')
            else:
                print(maze[i][j],end='')
        print()

def initializeMaze(maze):
    for i in range(iSize):
        for j in range(jSize):
            if i % 2 == 1 and j % 2 == 1:
                newRoom = room(i,j)
                maze[i][j] = newRoom
    return maze

def buildNeighbours(maze):
    for i in range(iSize):
        for j in range(jSize):
            if i % 2 == 1 and j % 2 == 1:
                currentRoom = maze[i][j]
                neighbour = []
                #north
                if (i - 2) > 0:
                    neighbour.append(maze[i-2][j])
                #east
                if (j - 2) > 0:
                    neighbour.append(maze[i][j-2])
                #south
                if (i + 2) < iSize:
                    neighbour.append(maze[i+2][j])
                #west
                if (j + 2) < jSize:
                    neighbour.append(maze[i][j+2])
                currentRoom.setNeighbours(neighbour)
    return maze
def findAdjacentCells(currentRoomCells, neighbourCells):

    adjacentCells = []
    for cell in currentRoomCells:

        downrow= cell[0] + 2
        rightcol= cell[1] + 2
        uprow = cell[0] - 2
        leftcol = cell[1] - 2
        #print(cell, " n: ", end = "")
        for ncell in neighbourCells:
            #print(ncell, " : ", end = "")

            if ncell[0] == downrow and ncell[1] == cell[1]:
                adjacentCells.append((cell[0] + 1, cell[1]))
            elif ncell[0] == uprow and ncell[1] == cell[1]:
                adjacentCells.append((cell[0] - 1, cell[1]))
            elif ncell[1] == rightcol and ncell[0] == cell[0]:
                adjacentCells.append((cell[0] , cell[1] + 1))
            elif ncell[1] == leftcol and ncell[0] == cell[0]:
                adjacentCells.append((cell[0] , cell[1] - 1))
            #else:
            #    print("None found")

            #if len(adjacentCells) >0:
                #maze[adjacentCells[len(adjacentCells) -1][0]][adjacentCells[len(adjacentCells)-1][1]].name = "A"

        #print()
    return adjacentCells
    # set current room as visited.
    # pick a random neighbour to this room
    # now check each 'cell' in this room to see which cells have a wall with that neighbouring room
    # need to figure out which direction to check for the neighbour
    #   put those cells in a 'list'
    #       randomly pick one of those cells
    #       remove the wall from the current room and that room
    #       recurse into that room
def visitNodeAdvanced(currentRoom,maze,n):
    currentRoom.visited=True
    random.shuffle(currentRoom.neighbours)
    #print(currentRoom.neighbours[0].cells)
    #return maze
    for neighbour in currentRoom.neighbours:
        if neighbour.visited == False:
            #print("neighbour #: ", len(currentRoom.neighbours))
            #randomcell = neighbour.cells[0]  # a neighbour should have at least one cell
            #adjacentCells = findAdjacentCells(currentRoom.cells, neighbour.cells)
            adjacentCells = []
            for ccell in currentRoom.cells:
                downrow= ccell[0] + 2
                rightcol= ccell[1] + 2
                uprow = ccell[0] - 2
                leftcol = ccell[1] - 2
                #print(cell, " n: ", end = "")
                for ncell in neighbour.cells:
                    #print(ncell, " : ", end = "")

                    if ncell[0] == downrow and ncell[1] == ccell[1]:
                        adjacentCells.append((ccell[0] + 1, ccell[1]))
                    elif ncell[0] == uprow and ncell[1] == ccell[1]:
                        adjacentCells.append((ccell[0] - 1, ccell[1]))
                    elif ncell[1] == rightcol and ncell[0] == ccell[0]:
                        adjacentCells.append((ccell[0] , ccell[1] + 1))
                    elif ncell[1] == leftcol and ncell[0] == ccell[0]:
                        adjacentCells.append((ccell[0] , ccell[1] - 1))
            choice = random.randint(0,len(adjacentCells)-1)

            maze[adjacentCells[choice][0]][adjacentCells[choice][1]].name = "H"
            n += 1
            #print("recurse: ", n)
            maze = visitNodeAdvanced(neighbour, maze, n)
    return maze
def visitNode(currentRoom, maze):

    currentRoom.visited=True
    currentRoom.name = " "
    random.shuffle(currentRoom.neighbours)

    for node in currentRoom.neighbours:
        if node.visited == False:

            leftorright = currentRoom.xPos - node.xPos

            upordown = currentRoom.yPos - node.yPos

            if leftorright == 0: # they are in the same column
                if upordown > 0:
                    offset = -1
                else:
                    offset = 1
                maze[currentRoom.xPos][currentRoom.yPos + offset] = " "
            elif upordown == 0: # they are in the same column
                if leftorright > 0:
                    offset = -1
                else:
                    offset = 1
                maze[currentRoom.xPos + offset][currentRoom.yPos] = " "


            maze = visitNode(node, maze)
    return maze

def biggermaze(maze):

    for i in range(100):
        x = random.randint(1,iSize-2)
        y = random.randint(1,jSize-2)

        maze[x][y] = " "

    return maze
def createNewMazeWithRooms():
    maze = [[ ' ' for i in range (jSize) ] for j in range(iSize)]
    maze = initializeMazeWithRooms(maze)
    maze = buildNeighboursBigRoom(maze)
    n = 0
    maze = visitNodeAdvanced(maze[1][1], maze, n)
    #printMazeWithRooms(maze)

    #construct level:
    newLevel = []
    line = ""
    maze[iSize-2][jSize-2].name ="E"
    for i in range(iSize):
        for j in range(jSize):
                if maze[i][j].name == "R" or maze[i][j].name == "H":
                #line += maze[i][j].name
                    line+= " "
                else:
                    line += maze[i][j].name
        newLevel.append(line)
        line = ""
    #print(newLevel)
    return newLevel
def createNewMaze():

    maze = [[ 'W' for i in range (jSize) ] for j in range(iSize)]
    maze = initializeMaze(maze)
    maze = buildNeighbours(maze)
    maze = visitNode(maze[1][1], maze)

    #printMaze(maze)
    #maze = biggermaze(maze)
    #construct level:
    newLevel = []
    line = ""
    maze[iSize-2][jSize-2].name ="E"
    for i in range(iSize):
        for j in range(jSize):
            if i % 2 == 1 and j % 2 == 1 :
                line += maze[i][j].name
            else:
                line += maze[i][j]
        newLevel.append(line)
        line = ""
    #line  = newLevel[iSize-3]
    #l = list(line)
    #l[jSize-2] = "E"
    #line = "".join(l)
    return newLevel

#createNewMaze()
#createNewMazeWithRooms()
