class room():
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



