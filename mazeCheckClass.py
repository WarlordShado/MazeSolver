import time as t

class Maze():
    WALL:str = "#"
    PATH:str = "."
    START:str = "S"
    END:str = "E"

    BEEN_ONCE:str = "X"
    BEEN_TWICE:str = "#"

    VALID_PATH:str = "$"

    UP:int = 1
    RIGHT:int = 4
    DOWN:int = 3
    LEFT:int = 2

    def __init__(self,maze:list=[]) -> None:
        self.Maze:list = maze
        self.MazeStart:list = maze
        self.prevState:list = []
        self.currentCoords:list = []
        self.prevCoords:list = []
        self.facing:int = 1

    def parseMaze(self,str:str,set:bool=False):
        maze:list = [[]]
        rowCount:int = 0
        for char in str:
            if char == "\n":
                maze.append([])
                rowCount += 1
            else:
                maze[rowCount].append(char)
        if set:
            self.Maze = maze
            self.MazeStart = self.Maze
        return maze

    def printMaze(self,array):
        string:str = ""
        for arr in array:
            for i in arr:
                string += i
            string += "\n"
        return string

    def solveMaze(self) -> str:
        solved:bool = False
        end:list = self.getEnd()
        start:list = self.getStart()
        self.currentCoords = start
        while not solved:
            nextCoordsFound:bool = False
            while not nextCoordsFound:
                if self.isStuck():
                    return "Impossible"

                checkCoords:tuple = self.getNextCoords()
                checkSpot:str = self.Maze[checkCoords[0]][checkCoords[1]]
                if checkSpot == self.END or checkSpot == self.PATH or (checkSpot == self.BEEN_ONCE and not self.isNewPath()):
                    nextCoordsFound = True
                    if checkSpot == self.END:
                        solved = True
                    self.Maze[self.currentCoords[0]][self.currentCoords[1]] = self.markSpot()
                    self.currentCoords = checkCoords
                else:
                    self.rotate()
        
        self.Maze[start[0]][start[1]] = self.START
        self.Maze[end[0]][end[1]] = self.END

        return self.validateMaze()
    
    def validateMaze(self)->str:
        solved:bool = False
        end:list = self.getEnd()
        start:list = self.getStart()
        self.currentCoords = start
        while not solved:
            nextCoordsFound:bool = False
            checkCoords:tuple = self.getNextCoords()
            checkSpot:str = self.Maze[checkCoords[0]][checkCoords[1]]
            while not nextCoordsFound:
                if checkSpot == self.BEEN_ONCE or checkSpot == self.END:
                    nextCoordsFound = True
                    if checkSpot == self.END:
                        solved = True
                    self.MazeStart[self.currentCoords[0]][self.currentCoords[1]] = self.VALID_PATH
                    self.currentCoords = checkCoords
                else:
                    self.rotate()
                checkCoords:tuple = self.getNextCoords()
                checkSpot = self.Maze[checkCoords[0]][checkCoords[1]]
        
        self.MazeStart[start[0]][start[1]] = self.START
        self.MazeStart[end[0]][end[1]] = self.END

        return self.printMaze(self.MazeStart).replace(self.PATH,self.WALL).replace(self.VALID_PATH,self.PATH)
    
    def markSpot(self)->str:
        return self.BEEN_ONCE if self.Maze[self.currentCoords[0]][self.currentCoords[1]] != self.BEEN_ONCE and not self.isIntersection() else self.BEEN_TWICE if not self.isIntersection() or (self.isIntersection and not self.isNewPath()) else self.BEEN_ONCE
    
    def isIntersection(self) -> bool:
        wallCount:int = 0
        checkCoords:list = self.getCheckCoords()
        for coord in checkCoords:
            wallCount += 1 if self.Maze[coord[0]][coord[1]] == self.WALL else 0
        return True if wallCount >= 2 else False
    
    def isDeadEnd(self) -> bool:
        wallCount:int = 0
        checkCoords:list = self.getCheckCoords()
        for coord in checkCoords:
            wallCount += 1 if self.Maze[coord[0]][coord[1]] == self.WALL else 0
        return True if wallCount >= 3 else False
    
    def isNewPath(self) -> bool:
        pathCount:int = 0
        checkCoords:list = self.getCheckCoords()
        for coord in checkCoords:
            mazeCheck = self.Maze[coord[0]][coord[1]]
            pathCount += 1 if mazeCheck == self.PATH or mazeCheck == self.END else 0
        
        return True if pathCount >= 1 else False
    
    def isStuck(self) -> bool:
        wallCount:int = 0
        checkCoords:list = self.getCheckCoords()
        for coord in checkCoords:
            wallCount += 1 if self.Maze[coord[0]][coord[1]] == self.WALL else 0
        return True if wallCount >= 4 else False
    
    def getCheckCoords(self):
        return [[self.currentCoords[0] ,self.currentCoords[1] + 1],[self.currentCoords[0] + 1,self.currentCoords[1]],[self.currentCoords[0],self.currentCoords[1] - 1],[self.currentCoords[0] - 1,self.currentCoords[1]]]

    def rotate(self) -> None:
        self.facing += 1
        if self.facing >= 5:
            self.facing = 1
    
    def getNextCoords(self) -> tuple:
        match (self.facing):
            case self.UP:
                return (self.currentCoords[0] + 1,self.currentCoords[1])
            case self.RIGHT:
                return (self.currentCoords[0],self.currentCoords[1] + 1)
            case self.DOWN:
                return (self.currentCoords[0]- 1,self.currentCoords[1] )
            case self.LEFT:
                return (self.currentCoords[0] ,self.currentCoords[1]- 1)

    def getStart(self):
        for index,maze in enumerate(self.Maze):
            if self.START in maze:
                return [index,maze.index(self.START) ]
        return 0
    
    def getEnd(self):
        for index,maze in enumerate(self.Maze):
            if self.END in maze:
                return [index,maze.index(self.END) ]
        return 0