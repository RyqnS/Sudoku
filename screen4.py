from cmu_cs3_graphics import *
import copy
import random
import math
import os
from screen1 import *
import itertools
from runAppWithScreens import *
from PIL import Image
import os

class boardState:
    def __init__(self,board,possibleValues,playerMoves,playerFlags,playerBans):
        self.board = board
        self.possibleValues = possibleValues
        self.playerMoves = playerMoves
        self.playerFlags = playerFlags
        self.playerBans = playerBans
    def __eq__(self,other):
        return isinstance(other,boardState) and self.board == other.board and self.playerFlags == other.playerFlags and self.playerBans == other.playerBans
    def __repr__(self):
        return str(self.playerMoves)

def screen4_onScreenStart(app):
    setUp(app)

def setUp(app):
    app.spriteone = loadAnimatedGif(app, 'wow.gif')
    app.spriteCounter = 0
    app.stepsPerSecond = 8
    app.spriteCounter = 0
    app.stepsPerSecond = 8
    app.rows = 9
    app.cols = 9
    app.boardWidth = app.boardHeight = 50+min(app.width- app.width//3,app.height - app.height//3)
    app.boardLeft = app.width//2 - app.boardWidth//2
    app.boardTop = app.height//6
    app.cellBorderWidth = 2
    app.board = []
    app.numpad = [[1,4,7],[2,5,8],[3,6,9]]
    #[([None] * app.cols) for row in range(app.rows)]
    app.playerHover = None 
    app.numHover = None
    app.playerSelect = None # one at a time, 'enter' to move this to playerMoves
    app.playerMoves = [] #list of (row,col) moves
    app.numpadStartLeft = app.boardLeft + app.boardWidth + 50
    app.numpadStartTop = app.boardTop
    app.setOfNumbers = {1,2,3,4,5,6,7,8,9}
    app.possibleValues = [[set() for i in range(app.cols)] for j in range(app.rows)]
    app.showPossibles=False
    app.listofActions = ["Hint","Current Mode: Input","Show Legals","Strong Hint","Autofill"]
    app.inputMode = 0 #for input mode, 1 for flag mode, 2 for ban mode
    app.playerFlags = [[set() for i in range(app.cols)] for j in range(app.rows)]
    app.playerBans = [[set() for i in range(app.cols)] for j in range(app.rows)]
    app.listOfStates = []
    app.listOfRedoStates = []
    # if app.selectedDiff != None:
    app.mouseUse = True
    app.keyboardUse = True
    app.competitionMode = False
    app.hintState = 0
    app.betterHintState = 0
    app.selectedCells = [] #reserved for hints
    app.currentHint = None
    app.stepsPerSecond = 8
    app.steps = 0
    app.gameLost = False
    app.killTimer = 0

def loadAnimatedGif(app, path):
    pilImages = Image.open(path)
    if pilImages.format != 'GIF':
        raise Exception(f'{path} is not an animated image!')
    if not pilImages.is_animated:
        raise Exception(f'{path} is not an animated image!')
    cmuImages = [ ]
    for frame in range(pilImages.n_frames):
        pilImages.seek(frame)
        pilImage = pilImages.copy()
        cmuImages.append(CMUImage(pilImage))
    return cmuImages

def makeRedImage(sourceImage):
    # First, get the RGB version of the image so getpixel returns r,g,b values:
    rgbImage = sourceImage.convert('RGB')

    # Now, a new image in the 'RGB' mode with same dimensions as app.image
    newImage = Image.new(mode='RGB', size=rgbImage.size)
    for x in range(newImage.width):
        for y in range(newImage.height):
            r,g,b = rgbImage.getpixel((x,y))
            newImage.putpixel((x,y),(r,0,0)) # ignore green and blue!

    return newImage

def screen4_redrawAll(app):
    if app.gameLost == True or app.steps >=1800:
        setActiveScreen('screen5')
    else:
        drawRect(0,0,app.width,app.height,fill = 'black')
        if random.randint(6,666) == 6: 
            spriteA = app.spriteone[app.spriteCounter]
            drawImage(spriteA, random.randint(60,app.width-60), random.randint(60,app.height-60), align='center')

        # drawRect(0,0,app.width,app.height)
        drawLabel(f'Sudoku', app.width//2, app.height//10, size=60,fill = 'Red', align = 'center',)

        drawBoard(app)
        drawBoardBorder(app)
        drawFlags(app)
        drawBans(app)
        drawReds(app)
        
        if (app.selectedMode!= None and (app.modes[app.selectedMode] == 'mouse-only' or app.modes[app.selectedMode] == 'standard')):
            drawNumbers(app)
            drawPossiblesControl(app)
            drawLabel("Back to Menu",200,60,size = 40,bold = True,align = 'center', fill = 'red')
        if app.showPossibles == True:
            drawPossibles(app)
        if sudokuSolved(app):
            drawRect(app.width//2,app.height-50,400,100,align = 'center',fill = 'black',border = 'white')
            drawLabel("You Completed the board!",app.width//2,app.height-50,align = 'center', size = 30)
        drawLabel(f'{str(60-app.steps//30)}',225,677, fill = 'white',size = 30)

        
def drawFlags(app):
    cellWidth,cellHeight = getCellSize(app)
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j]==0:
                cellLeft, cellTop = getCellLeftTop(app, i, j)
                for num in range(0,10):
                    if num in app.playerFlags[i][j]:
                        if num%3 == 0:
                            drawLabel(str(num),cellLeft + (3)*(cellWidth//4),cellTop+(cellHeight//4)*(math.ceil(num/3)),fill = 'blue')
                        else:
                            drawLabel(str(num),cellLeft + (num%3)*(cellWidth//4),cellTop+(cellHeight//4)*(math.ceil(num/3)),fill = 'blue')
def drawReds(app):
    cellWidth,cellHeight = getCellSize(app)
    for i in range(app.rows):
        for j in range(app.cols):
            cellLeft, cellTop = getCellLeftTop(app, i, j)
            if app.board[i][j]==0:
                for num in app.playerBans[i][j]:
                    if app.solvedBoard[i][j] == num:
                        drawCircle(cellLeft+10,cellTop+10,5,fill = 'red')
                        if app.competitionMode == True:
                            setActiveScreen('screen1')
            else:
                if app.board[i][j] != app.solvedBoard[i][j]:
                    drawCircle(cellLeft+10,cellTop+10,5,fill = 'red')
                    if app.competitionMode == True:
                        setActiveScreen('screen1')


    pass
def drawBans(app):
    cellWidth,cellHeight = getCellSize(app)
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j]==0:
                cellLeft, cellTop = getCellLeftTop(app, i, j)
                for num in range(0,10):
                    if num in app.playerBans[i][j]:
                        if num%3 == 0:
                            drawLabel(str(num),cellLeft + (3)*(cellWidth//4),cellTop+(cellHeight//4)*(math.ceil(num/3)),fill = 'red')
                        else:
                            drawLabel(str(num),cellLeft + (num%3)*(cellWidth//4),cellTop+(cellHeight//4)*(math.ceil(num/3)),fill = 'red')
    pass

def drawPossiblesControl(app):
    for i in range(5):
        drawRect(225,200+i*80,(app.width - app.numpadStartLeft-50)//1.5,40,align = 'center',fill= None,border = 'red')
        drawLabel(app.listofActions[i],225,200+i*80,size = 20,bold = True,fill = 'white')
def drawPossibles(app): #Modified from CS Academy
    cellWidth,cellHeight = getCellSize(app)
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j]==0:
                cellLeft, cellTop = getCellLeftTop(app, i, j)
                for num in range(0,10):
                    if num in app.possibleValues[i][j]:
                        if num%3 == 0:
                            drawLabel(str(num),cellLeft + (3)*(cellWidth//4),cellTop+(cellHeight//4)*(math.ceil(num/3)))
                        else:
                            drawLabel(str(num),cellLeft + (num%3)*(cellWidth//4),cellTop+(cellHeight//4)*(math.ceil(num/3)))

def drawNumbers(app): #Modified from CS Academy
    numpadWidth = app.width - app.numpadStartLeft - 50
    numpadHeight = app.boardHeight//4*3
    for i in range(3):
        for j in range(3):
            drawNumCell(app,i,j,app.numpad[i][j])
    drawRect(1151,500,80,40,fill = None,border = 'red')
    drawRect((1111+1462)//2,520,80,40,align = 'center',fill = None,border = 'red')
    drawRect(1340,500,80,40,fill = None, border = 'red')
    drawLabel("Undo",1191,520,size = 20, fill = 'white')
    drawLabel("Redo",(1111+1462)//2,520,size = 20, fill = 'white')
    drawLabel("Clear",1380,520,size = 20, fill = 'white')#numpadStartLeft+ (numpadWidth-200 - width)//2 + i*100, numpadStartTop+30 + j*100, width,height,fill = 'lightgrey',border = 'black')
def drawNumCell(app, row, col,number): #Modified from CS Academy
    cellLeft, cellTop = getNumCellLeftTop(app, row, col)
    cellWidth, cellHeight = getNumCellSize(app)
    # bW = app.cellBorderWidth if (row,col) == app.playerSelect else app.cellBorderWidth//2
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='white',
             borderWidth=2)
    drawLabel(app.numpad[row][col],cellLeft+cellWidth//2,cellTop+cellHeight//2, 
              align = 'center',size = 32,fill = 'red')
def getNumCellLeftTop(app, row, col): #Modified from CS Academy
    cellWidth, cellHeight = getCellSize(app)
    numpadWidth = app.width - app.numpadStartLeft-50
    numpadHeight = app.boardHeight//4*3
    cellLeft = app.numpadStartLeft + (numpadWidth-200 - cellWidth)//2 + row*100
    cellTop = app.numpadStartTop+ 30 + col*100
    return (cellLeft, cellTop)
def getNumCellSize(app): #Modified from CS Academy
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
def getNumCell(app, x, y): #Modified from CS Academy
    cellWidth, cellHeight = getCellSize(app)
    if 1152<x<1220:
        nrow = 0  
    elif 1252<x<1320:
        nrow = 1
    elif 1352<x<1420:
        nrow = 2
    else:
        nrow = 3
    if 170<y<238:
        ncol = 0 
    elif 270<y<338:
        ncol = 1
    elif 370<y<438:
        ncol = 2
    else:
        ncol = 3
    if (0 <= nrow < 3) and (0 <= ncol < 3):
        return (nrow, ncol)
    else:
        return None

def drawBoard(app): #From CS Academy
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col,app.board[row][col])
    for i in range(1,3):
        drawLine(app.boardLeft + i * app.boardWidth//3, app.boardTop,app.boardLeft + i * app.boardWidth//3, app.boardTop+app.boardHeight, lineWidth = app.cellBorderWidth*2,fill='white')
    for j in range(1,3):
        drawLine(app.boardLeft,app.boardTop + j*app.boardHeight//3,app.boardLeft+app.boardWidth,app.boardTop+j*app.boardHeight//3, lineWidth = app.cellBorderWidth*2,fill = 'white')
def drawBoardBorder(app): #From CS Academy
  # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, border='white',
           borderWidth=2*app.cellBorderWidth,fill = None)
def drawCell(app, row, col,number): #From CS Academy
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if(app.board[row][col]!= 0) and (row,col) not in app.playerMoves and (row,col) != app.playerSelect:
        color = 'red'
    elif (row, col) == app.playerHover:
        if app.inputMode == 0:
            color = 'lightblue'
        elif app.inputMode ==1:
            color = 'lightgreen'
        elif app.inputMode ==2:
            color = 'pink'
    elif (row,col) in app.selectedCells:
        color = 'lightblue'
    else:
        color = None

    bW = app.cellBorderWidth if (row,col) == app.playerSelect else app.cellBorderWidth//2

    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='white',
             borderWidth=bW)
    if app.board[row][col]!= 0:
        drawLabel(app.board[row][col],cellLeft+cellWidth//2,cellTop+cellHeight//2, 
              align = 'center',size = 32,fill = 'white')
def getCellLeftTop(app, row, col): #From CS Academy
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)
def getCellSize(app): #From CS Academy
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getCell(app, x, y): #From CS Academy
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None

def solveSudoku(app):
    unSolvedSet = set()
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j]==0:
                unSolvedSet.add((i,j))
    return solveSudokuHelp(app,unSolvedSet) 

def solveSudokuHelp(app,unSolvedSet):
    if sudokuSolved(app):
        return app.board
    else:
        updatePossibles(app)
        if hasSingletons(app):
            a,b = findSingleton(app)
            if (a,b) in unSolvedSet:
                app.board[a][b] = app.possibleValues[a][b].pop()
                unSolvedSet.remove((a,b))
                sol = solveSudokuHelp(app,unSolvedSet)
                if sol!=None:
                    return sol
                else:
                    app.board[a][b] = 0
                    unSolvedSet.add((a,b))
            else:
                return app.board
            
        else:
            for (x,y) in unSolvedSet:
                i,j = findSmallestPossible(app,unSolvedSet) #findthingwithsmalelst#ofpossiblevalues
                for value in app.possibleValues[i][j]:
                    app.board[i][j] = value
                    unSolvedSet.remove((i,j))
                    sol = solveSudokuHelp(app,unSolvedSet)
                    if sol!=None:
                        return sol
                    else:
                        app.board[i][j] = 0
                        unSolvedSet.add((i,j))
def findSmallestPossible(app,unSolvedSet):
    smallNum = None
    smallNumIndex = None
    for (i,j) in unSolvedSet:
        if smallNum == None or len(app.possibleValues[i][j]) < smallNum:
            smallNum = len(app.possibleValues[i][j])
            smallNumIndex = (i,j)
    return smallNumIndex
def sudokuSolved(app): #Taken from CS Academy 
    for row in range(app.rows):
        tempRows = getRowVals(app,row)
        if tempRows != app.setOfNumbers:
            return False
    for col in range(app.cols):
        tempCols = getRowVals(app,col)
        if tempCols != app.setOfNumbers:
            return False
    for i in [0,3,6]:
        for j in [0,3,6]:
            tempSquare = getSquareVals(app,i,j)
            if tempSquare != app.setOfNumbers:
                return False
    return True
def findSingleton(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if len(app.possibleValues[i][j])==1 and (i,j) not in app.playerMoves:
                return i,j
def clearSelection(app,row,col):
    app.board[row][col] = 0
def findNext(app,row,col,drow,dcol):
    if (row+drow not in range(0,app.rows)) or (col+dcol not in range(0,app.cols)):
        return None
    elif  app.board[row+drow][col+dcol]==0 or (row+drow,col+dcol) in app.playerMoves:
        return row+drow,col+dcol
    else:
        return findNext(app,row+drow,col+dcol,drow,dcol)

#Import doesn't get these functions, Idk why
def getRowVals(app,row):
    returnSet = set()
    for val in app.board[row]:
        returnSet.add(val)
    return returnSet
def getColVals(app,col):
    returnSet = set()
    for i in range(app.rows):
        returnSet.add(app.board[i][col])
    return returnSet
def getSquareVals(app,rownum,colnum):
    if rownum <=2:
        startrow = 0
    elif 3<=rownum<6:
        startrow = 3
    else:
        startrow = 6

    if colnum <=2:
        startcol = 0
    elif 3<=colnum<6:
        startcol = 3
    else:
        startcol = 6

    returnSet = set()

    for j in range(startrow,startrow+3):
        for k in range(startcol,startcol+3):
            returnSet.add(app.board[j][k])
    
    return returnSet
def hasSingletons(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if len(app.possibleValues[i][j])==1:
                return True
    return False
def updatePossibles(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j]==0:
                rowset = getRowVals(app,i)
                colset = getColVals(app,j)
                squareset = getSquareVals(app,i,j)
                app.possibleValues[i][j] = app.setOfNumbers-(rowset.union(colset).union(squareset))
            if app.playerBans[i][j]!=0:
                app.possibleValues[i][j] -= app.playerBans[i][j]
    if app.competitionMode:
        app.listofActions[0] = 'No Hints!'
        app.listofActions[3] = "Strong Hints off!"
        app.listofActions[4] = "Autofill off!"
    if sudokuSolved(app):
        with open('/Users/ryansong/Python/SudokuCode/submission.txt', "wt") as f:
            for row in range(len(app.board)):
                for col in range(len(app.board[0])):
                    f.write(str(app.board[row][col]))
                    f.write(" ")
                f.write('\n')
        f.close()
    if hasSingletons(app) and not sudokuSolved(app) and findSingleton(app)!=None:
        i,j = findSingleton(app)
        if app.playerSelect == (i,j) and app.hintState == 1:
            app.listofActions[0] = "Do hint"
        else:
            if app.competitionMode != True:
                app.listofActions[0] = "Hint"
            app.hintState = 0
    if app.currentHint != None:
        for (x,y) in app.currentHint:
            if app.board[x][y] == app.solvedBoard[x][y]:
                app.listofActions[3] = 'Strong Hint'
    if strongHintHelper(app)==None:
        app.listofActions[3] = 'No Strong Hints Left'
    if app.solvedBoard!= None:
        for xrow in range(app.rows):
            for xcol in range(app.cols):
                if app.board[xrow][xcol] != 0 and app.board[xrow][xcol]!=app.solvedBoard[xrow][xcol]:
                    app.gameLost = True

def updateStates(app):
    stateB = boardState(copy.deepcopy(app.board),copy.deepcopy(app.possibleValues),copy.deepcopy(app.playerMoves),copy.deepcopy(app.playerFlags),copy.deepcopy(app.playerBans))
    # # print(stateA == app.listOfStates[-1])
    if stateB != app.listOfStates[-1]:
        app.listOfStates.append(stateB)
# end of 'these functions'
def screen4_onMouseRelease(app,mouseX,mouseY):
    if app.maker or (app.selectedMode!= None and (app.modes[app.selectedMode] == 'mouse-only' or app.modes[app.selectedMode] == 'standard')):
        if not (420<=mouseY<=460 and 0<=mouseX<=401):
            app.betterHintState = 0
        if 30<=mouseY<=90:
            if 50<=mouseX<=350:
                if app.maker:
                    app.board = []
                    app.saveboard = None
                    app.maker = False
                setActiveScreen('screen1')
        elif 0<=mouseX<=401:
            if 180<=mouseY<=220:
                if app.competitionMode == False:
                    if app.hintState == 0:
                        if hasSingletons(app) and not sudokuSolved(app):
                            i,j = findSingleton(app)
                            app.playerSelect = i,j
                            app.playerHover = i,j
                        app.hintState =1

                    elif app.hintState ==1:
                        if hasSingletons(app) and not sudokuSolved(app):
                            i,j = findSingleton(app)
                            if app.playerSelect == app.playerHover == (i,j):
                                app.board[i][j] = app.possibleValues[i][j].pop()
                                app.playerMoves.append((i,j))
                                app.listOfRedoStates = []
                            else:
                                app.hintState = 0
                                i,j = findSingleton(app)
                                app.playerSelect = i,j
                                app.playerHover = i,j
                        app.hintState = 0
            elif 260<=mouseY<=300:
                #mode
                app.inputMode +=1
                app.inputMode%=3
                if app.inputMode==0:
                    app.listofActions[1] = "Current Mode: Input"
                elif app.inputMode ==1:
                    app.listofActions[1] = "Current Mode: Flag"
                elif app.inputMode ==2:
                    app.listofActions[1] = "Current Mode: Ban"
                # app.showPossibles = True
            elif 340<=mouseY<=380:
                #legals
                app.showPossibles = not app.showPossibles
                if app.showPossibles:
                    app.listofActions[2] = "Hide Legals"
                else:
                    app.listofActions[2] = "Show Legals"
            elif 420<=mouseY<=460:
                print(app.betterHintState)
                if app.competitionMode == False:
                    if strongHintHelper(app)==None:
                        app.listofActions[3] = 'No Strong Hints Left'
                        return
                    listOfTuples, overlappingElements = strongHintHelper(app)
                    if listOfTuples == app.currentHint:
                        if app.betterHintState ==0:
                            app.listofActions[3] = 'Solve This Hint First'
                        else:
                            app.listofActions[3] = 'Strong Hint'
                    app.currentHint = listOfTuples
                    if app.currentHint == None:
                        app.currentHint = listOfTuples
                    if app.betterHintState == 0:
                        for (x,y) in listOfTuples:
                            app.selectedCells.append((x,y))
                        print(app.selectedCells)
                        app.betterHintState =1
                    elif app.betterHintState ==1:
                        if app.selectedCells == list(listOfTuples):
                            doBans(app,listOfTuples, overlappingElements)
                            app.selectedCells = []
                            app.listOfRedoStates = []
                        else:
                            app.betterHintState = 0
                            for (x,y) in listOfTuples:
                                app.selectedCells.append((x,y))
                        app.selectedCells = []
                        app.betterHintState = 0            

            elif 500<=mouseY<=540:
                if app.competitionMode == False:
                    for i in range(app.rows):
                        for j in range(app.cols):
                            if app.board[i][j] == 0:
                                app.playerMoves.append((i,j))
                    app.board = app.solvedBoard

        elif 401<mouseX <=app.numpadStartLeft:
            selectedCell = getCell(app, mouseX, mouseY)
            if selectedCell!=None:
                row,col = selectedCell[0],selectedCell[1]
            if selectedCell!= None and app.board[row][col]!=0 and selectedCell not in app.playerMoves:
                if selectedCell == app.playerSelect:
                    if app.inputMode == 0:
                        app.playerMoves.append(app.playerSelect)
                        app.listOfRedoStates = []
                    elif app.inputMode == 1:
                        app.playerFlags[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                    elif app.inputMode ==2:
                        app.playerBans[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                app.playerSelect = None
                app.playerHover = None
                selectedCell = None
            else:
                if app.playerSelect== None:
                    app.playerSelect = selectedCell
                    app.playerHover = selectedCell
                else:
                    if selectedCell == app.playerSelect:
                        if app.board[row][col]!=0 and selectedCell not in app.playerMoves:
                            if app.inputMode==0:
                                app.playerMoves.append(app.playerSelect)
                                app.listOfRedoStates = []
                            elif app.inputMode ==1:
                                app.playerFlags[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                            elif app.inputMode ==2:
                                app.playerBans[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                        app.playerSelect = None
                        app.playerHover = None
                    else:
                        if app.board[app.playerSelect[0]][app.playerSelect[1]]!=0 and (app.playerSelect[0],app.playerSelect[1]) not in app.playerMoves:
                            if app.inputMode==0:
                                app.playerMoves.append(app.playerSelect)
                                app.listOfRedoStates = []
                            elif app.inputMode ==1:
                                app.playerFlags[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                            elif app.inputMode ==2:
                                app.playerBans[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                        app.playerSelect = selectedCell
                        app.playerHover = selectedCell
        elif mouseX >app.numpadStartLeft:
            selectedCell = getNumCell(app, mouseX, mouseY)
            if selectedCell!=None:
                row,col = selectedCell[0],selectedCell[1]
                num = app.numpad[row][col]
                app.listOfRedoStates = []
                if app.playerSelect!=None:
                    editrow,editcol = app.playerSelect[0],app.playerSelect[1]
                    if app.inputMode == 0:
                        app.board[editrow][editcol] = num
                        if (editrow,editcol) not in app.playerMoves:
                            app.playerMoves.append(app.playerSelect)
                    elif app.inputMode ==1:
                        app.playerFlags[editrow][editcol].add(num)
                        if num in app.playerBans[editrow][editcol]:
                            app.playerBans[editrow][editcol].remove(num)
                    elif app.inputMode ==2:
                        app.playerBans[editrow][editcol].add(num)
                        if num in app.playerFlags[editrow][editcol]:
                            app.playerFlags[editrow][editcol].remove(num)
            else:
                if 500<= mouseY<=540:
                    if 1151<=mouseX<=1231 and len(app.listOfStates) > 1:
                        #undo
                        if len(app.listOfStates) > 1:
                            app.listOfRedoStates.append(app.listOfStates.pop())
                            currentState = app.listOfStates[-1]
                            app.board = copy.deepcopy(currentState.board)
                            app.playerMoves = copy.deepcopy(currentState.playerMoves)
                            app.playerFlags = copy.deepcopy(currentState.playerFlags)
                            app.playerBans = copy.deepcopy(currentState.playerBans)
                            app.possibleValues = copy.deepcopy(currentState.possibleValues)
                    elif 1246<=mouseX<=1326:
                        #redo
                        if len(app.listOfRedoStates) > 0:
                            app.listOfStates.append(app.listOfRedoStates.pop())
                            currentState = app.listOfStates[-1]
                            app.board = copy.deepcopy(currentState.board)
                            app.playerMoves = copy.deepcopy(currentState.playerMoves)
                            app.possibleValues = copy.deepcopy(currentState.possibleValues)
                            app.playerFlags = copy.deepcopy(currentState.playerFlags)
                            app.playerBans = copy.deepcopy(currentState.playerBans)
                    elif 1340<=mouseX<=1420:
                        #clear
                        if app.playerSelect!=None:
                            app.board[app.playerSelect[0]][app.playerSelect[1]] = 0
                            if(app.playerSelect[0],app.playerSelect[1]) in app.playerMoves:
                                app.playerMoves.remove((app.playerSelect[0],app.playerSelect[1]))
                                app.listOfRedoStates = []
                            if app.playerFlags[app.playerSelect[0]][app.playerSelect[1]] != set():
                                app.playerFlags[app.playerSelect[0]][app.playerSelect[1]] = set()
                                app.listOfRedoStates = []
                            if app.playerBans[app.playerSelect[0]][app.playerSelect[1]] != set():
                                app.playerBans[app.playerSelect[0]][app.playerSelect[1]] = set()
                                app.listOfRedoStates = []

                elif 650<=mouseY<=750 and app.maker:
                    app.selectedDiff = 0
                    app.saveboard = app.board
                    app.maker = False
                    app.message = ''
                    setActiveScreen('screen1')
            app.steps = 0

        if app.board!= []:
            updatePossibles(app)
            updateStates(app)

def screen4_onMouseMove(app,mouseX,mouseY):
    if app.maker or (app.selectedMode!= None and (app.modes[app.selectedMode] == 'mouse-only' or app.modes[app.selectedMode] == 'standard')):
        if mouseX <=app.numpadStartLeft:
            selectedCell = getCell(app, mouseX, mouseY)
            if app.playerSelect == None:
                if selectedCell != app.playerSelect:
                    app.playerHover = selectedCell
                    app.numHover = None
        elif mouseX>app.numpadStartLeft:
            selectedCell = getNumCell(app,mouseX,mouseY)
            app.numHover = selectedCell
            if app.playerSelect == None:
                app.playerHover = None
   
def screen4_onKeyPress(app,key):
    if app.maker or (app.selectedMode!= None and (app.modes[app.selectedMode] == 'keyboard-only' or app.modes[app.selectedMode] == 'standard')):
        # keyboardUse == True:
        if key!= 'H':
            app.betterHintState = 0
        if app.playerSelect != None:
            row,col = app.playerSelect
            if key in ['up','left','right','down']:
                if app.board[row][col]!=0 and (row,col) not in app.playerMoves:
                    if app.inputMode==0:
                        app.playerMoves.append(app.playerSelect)
                    elif app.inputMode ==1:
                        app.playerFlags[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                    elif app.inputMode == 2:
                        app.playerBans[app.playerSelect[0]][app.playerSelect[1]].add(app.playerSelect)
                if key =='up':
                    if findNext(app,row,col,-1,0)!= None:
                        app.playerHover = app.playerSelect = findNext(app,row,col,-1,0)
                elif key =='left':
                    if findNext(app,row,col,0,-1)!= None:
                        app.playerHover = app.playerSelect = findNext(app,row,col,0,-1)
                elif key =='right':
                    if findNext(app,row,col,0,1)!= None:
                        app.playerHover = app.playerSelect = findNext(app,row,col,0,1)
                elif key =='down':
                    if findNext(app,row,col,1,0)!= None:
                        app.playerHover = app.playerSelect = findNext(app,row,col,1,0)

            if key.isdigit() and key != '0':
                app.listOfRedoStates = []
                if app.inputMode==0:
                    app.board[row][col] = int(key)
                    if (row,col) not in app.playerMoves:
                        app.playerMoves.append(app.playerSelect)     
                elif app.inputMode ==1:
                    app.playerFlags[row][col].add((int(key)))
                    if (int(key)) in app.playerBans[row][col]:
                        app.playerBans[row][col].remove((int(key)))
                elif app.inputMode ==2:
                    app.playerBans[row][col].add((int(key)))
                    if (int(key)) in app.playerFlags[row][col]:
                        app.playerFlags[row][col].remove((int(key)))
                app.steps = 0
            elif key =='backspace':
                app.board[row][col] = 0
                if(row,col) in app.playerMoves:
                    app.playerMoves.remove((row,col))
                    app.listOfRedoStates = []
                if app.playerFlags[row][col] != set():
                    app.playerFlags[row][col] = set()
                    app.listOfRedoStates = []
                if app.playerBans[row][col] != set():
                    app.playerBans[row][col] = set()
                    app.listOfRedoStates = []
        if key == 'z':
            if len(app.listOfStates) > 1:
                app.listOfRedoStates.append(app.listOfStates.pop())
                currentState = app.listOfStates[-1]
                app.board = copy.deepcopy(currentState.board)
                app.playerMoves = copy.deepcopy(currentState.playerMoves)
                app.playerFlags = copy.deepcopy(currentState.playerFlags)
                app.playerBans = copy.deepcopy(currentState.playerBans)
                app.possibleValues = copy.deepcopy(currentState.possibleValues)
        elif key =='Z':
            if len(app.listOfRedoStates) > 0:
                app.listOfStates.append(app.listOfRedoStates.pop())
                currentState = app.listOfStates[-1]
                app.board = copy.deepcopy(currentState.board)
                app.playerMoves = copy.deepcopy(currentState.playerMoves)
                app.playerFlags = copy.deepcopy(currentState.playerFlags)
                app.playerBans = copy.deepcopy(currentState.playerBans)
                app.possibleValues = copy.deepcopy(currentState.possibleValues)
        elif key == 'l':
            app.showPossibles = not app.showPossibles
            # solveSudoku(app.board)
            # print(app.listOfBoardNames)            
        elif key == 'h':
            if app.competitionMode == False:
                if app.hintState == 0:
                    if hasSingletons(app) and not sudokuSolved(app):
                        i,j = findSingleton(app)
                        app.playerSelect = i,j
                        app.playerHover = i,j
                    app.hintState =1
                elif app.hintState ==1:
                    if hasSingletons(app) and not sudokuSolved(app):
                        i,j = findSingleton(app)
                        if app.playerSelect == app.playerHover == (i,j):
                            app.board[i][j] = app.possibleValues[i][j].pop()
                            app.playerMoves.append((i,j))
                            app.listOfRedoStates = []
                        else:
                            app.hintState = 0
                            i,j = findSingleton(app)
                            app.playerSelect = i,j
                            app.playerHover = i,j
                    app.hintState = 0
        elif key =='f':
            app.inputMode +=1 
            app.inputMode %=3
            if app.inputMode==0:
                    app.listofActions[1] = "Current Mode: Input"
            elif app.inputMode ==1:
                app.listofActions[1] = "Current Mode: Flag"
            elif app.inputMode ==2:
                app.listofActions[1] = "Current Mode: Ban"
        elif key =='escape':
            if app.maker:
                app.board = []
                app.saveboard = None
                app.maker = False
            setActiveScreen('screen1')

            # for x,y in listOfTuples:
        elif key =='H':
            print(app.betterHintState)
            if app.competitionMode == False:
                if strongHintHelper(app)==None:
                    app.listofActions[3] = 'No Strong Hints Left'
                    return
                listOfTuples, overlappingElements = strongHintHelper(app)
                if listOfTuples == app.currentHint:
                    if app.betterHintState ==0:
                        app.listofActions[3] = 'Solve This Hint First'
                    else:
                        app.listofActions[3] = 'Strong Hint'
                app.currentHint = listOfTuples
                if app.currentHint == None:
                    app.currentHint = listOfTuples
                if app.betterHintState == 0:
                    for (x,y) in listOfTuples:
                        app.selectedCells.append((x,y))
                    print(app.selectedCells)
                    app.betterHintState =1
                elif app.betterHintState ==1:
                    if app.selectedCells == list(listOfTuples):
                        doBans(app,listOfTuples, overlappingElements)
                        app.selectedCells = []
                        app.listOfRedoStates = []
                    else:
                        app.betterHintState = 0
                        for (x,y) in listOfTuples:
                            app.selectedCells.append((x,y))
                    app.selectedCells = []
                    app.betterHintState = 0            

        if app.board!=[]:
            updatePossibles(app)
            updateStates(app)

def doBans(app,listofTuples,overlappingElements):
    if listofTuples[0][0] == listofTuples[1][0]:
        doRowBans(app,listofTuples,overlappingElements)
    elif listofTuples[0][1] == listofTuples[1][1]:
        doColBans(app,listofTuples,overlappingElements)
    row1 = listofTuples[0][0] 
    col1 = listofTuples[1][0]

    row2 = listofTuples[0][1] 
    col2 = listofTuples[1][1]

    if row1//3 == row2//3 and col1//3==col2//3:
        doSquareBans(app,listofTuples,overlappingElements)

def doRowBans(app,listofTuples,overlappingElements):
    for (i,j) in listofTuples:
        for col in range(app.cols):
            if app.board[i][col] == 0 and (i,col) not in listofTuples:
                app.possibleValues[i][col]-=overlappingElements
                app.playerBans[i][col]= app.playerBans[i][col].union(overlappingElements)

def doColBans(app,listofTuples,overlappingElements):
    for (i,j) in listofTuples:
        for row in range(app.rows):
            if app.board[row][j] == 0 and (row,j) not in listofTuples:
                app.possibleValues[row][j]-=overlappingElements
                app.playerBans[row][j]= app.playerBans[row][j].union(overlappingElements)

def doSquareBans(app,listofTuples,overlappingElements):
    for (i,j) in listofTuples:
        squareStartRow = 3*(i//3)
        squareStartCol = 3*(j//3)
        for row in range(squareStartRow,squareStartRow+3):
            for col in range(squareStartCol,squareStartCol+3):
                if app.board[row][col] == 0 and (row,col) not in listofTuples:
                    app.possibleValues[row][col]-=overlappingElements
                    app.playerBans[row][col]= app.playerBans[row][col].union(overlappingElements)

def strongHintHelper(app):
    regionList = makeRegionList(app)
    for N in range(2,6):
        for region in regionList:
            for M in itertools.combinations(region, N):
                if getOverlappingElements(app,M) != None:
                    return M, getOverlappingElements(app,M)
    app.listofActions[3] = 'No Strong Hints Left!'
    return None

def getOverlappingElements(app,M):
    for (i,j) in M:
        if app.board[i][j]!=0:
            return None
        else:
            theValues =  app.possibleValues[i][j]
            for (i2,j2) in M:
                if app.possibleValues[i2][j2]!=theValues:
                    return None
            
            if len(M) == len(theValues):
                return theValues
    return None

def makeRegionList(app):
    returnList = []
    for row in range(app.rows):
        tempList = []
        for col in range(app.cols):
            tempList.append((row,col))
        returnList.append(tempList)
    for col in range(app.rows):
        tempList = []
        for row in range(app.cols):
            tempList.append((row,col))
        returnList.append(tempList)
    for i in range(3):
        for j in range(3):
            tempList = []
            for row in range(3*i,3*i+3):
                for col in range(3*j,3*j+3):
                    tempList.append((row,col))
            returnList.append(tempList)
    return returnList
  
def screen4_onKeyHold(app,key):
    if 'space' in key and 'enter' in key and app.maker:
        app.selectedDiff = 0
        app.saveboard = app.board
        app.maker = False
        app.message = ''
        setActiveScreen('screen1')
    elif 'tab' in key and 'enter' in key:
        if app.competitionMode == False:
            for i in range(app.rows):
                for j in range(app.cols):
                    if app.board[i][j] == 0:
                        app.playerMoves.append((i,j))
            app.board = app.solvedBoard
    updatePossibles(app)

def screen4_onStep(app):
    if app.gameLost == True:
        app.killTimer +=1
        app.stepsPerSecond = 20
    else:
        app.spriteCounter = (1 + app.spriteCounter) % len(app.spriteone)
        app.steps+=1
    
    

