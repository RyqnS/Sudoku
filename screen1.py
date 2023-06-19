try: from cmu_cs3_graphics import *
except: from cmu_graphics import *
import random
import os
from screen2 import *
from runAppWithScreens import *


##################################
# Screen1
##################################

def screen1_onScreenStart(app):
    app.starts = 7
    app.colors = ['green','yellow','red','lightblue']
    app.misc = ['help','makeNewBoard']
    app.difficulties = ['easy','medium','hard','competition','nightmare']
    app.modes = ['standard','keyboard-only','mouse-only']
    app.difficultyIndex = 0
    app.modeIndex = 0
    app.hoverStart = 0
    app.selectedDiff = None
    app.selectedMode = None
    app.keyboardRow = 0
    app.message = ''
    app.miscIndex = 0
    app.maker = False
    app.saveboard = None
    app.solvedBoard = None
    app.boardStates = []

def screen1_redrawAll(app):
    #background
    drawRect(0,0,app.width,app.height,fill = 'black') 
    drawRect(app.width/2,100,330,120,align = 'center',border = 'white')
    drawLabel("Sudoku",app.width/2,100,size = 80,fill='white',bold = True)
    drawLabel("Epilepsy Warning", app.width//2,180,fill = 'white',size = 20)

    #Other
    drawMisc(app)
    drawDifficulties(app)
    drawModes(app)
    drawStart(app)

def drawMisc(app):
    Mcolor = 'white' if app.miscIndex == 0 and app.keyboardRow ==0 else 'black'
    Ncolor = 'white' if app.miscIndex == 1 and app.keyboardRow == 0 else 'black'
    drawRect(200,50,300,100,fill = 'lightblue',border = 'black')
    drawLabel("Help",350,100,size = 30,bold = True,align = 'center',fill = Mcolor)
    drawLabel(app.message,app.width//2,235,size = 20, fill = 'white')
    drawRect(app.width-500,50,300,100,fill = 'lightblue',border = 'black')
    drawLabel("Make a New Board",app.width-350,100,size = 30,bold = True,fill = Ncolor,align = 'center')
def drawDifficulties(app):
    if app.saveboard == None:
        for i in range(3):
            Tsize = 80 if i == app.difficultyIndex else 60
            drawRect(207+i*400,320,300,100,border = 'white')
            if app.selectedDiff ==None:
                color = app.colors[i]
            else:
                color = app.colors[i] if i ==app.selectedDiff else 'grey'
            drawLabel(app.difficulties[i].upper(),207+i*400+150,370,align = 'center',
                    fill = color,size = Tsize,bold = True)
        if app.selectedDiff == None:
            scolor = app.colors[3]
        else:
            scolor = app.colors[3] if 3 ==app.selectedDiff else 'grey'         
        csize = 40 if app.difficultyIndex == 3 else 30
        drawRect(507,495,300,80, border = 'white',align = 'center')
        drawLabel("COMPETITION", 507,495,align = 'center',size = csize, fill = scolor,bold = True)
    else:
        drawLabel("'Enter' or click to reset Custom Board",207+1*400+150,370,align = 'center',
                    fill = 'grey',size = 40,bold = True)
def drawModes(app):
    for j in range(len(app.modes)):
        Msize = 70 if j == app.modeIndex else 50
        drawRect((app.width-(3*480))//2+j*480+240,600,300,50,align = 'center')
        if app.selectedMode ==None:
            color = 'white'
        else:
            color = 'white' if j ==app.selectedMode else 'grey'
        drawLabel(app.modes[j].upper(),(app.width-(3*480))//2+j*480+240,600,align = 'center',
                  fill = color,size = Msize,bold = True)
def drawStart(app):
    Ssize = 70 if app.hoverStart==1 else 50
    color = 'red' if app.selectedDiff == 4 else "lightgreen"
    drawLabel("START",app.width//2,app.height-80,align = 'center',size = Ssize,bold = True,fill = color)
    if app.keyboardRow == 0:
        drawRegularPolygon(100,100,30,3,fill = 'white',rotateAngle = 90)
    if app.keyboardRow == 1:
        drawRegularPolygon(140,370,30,3,fill = 'white',rotateAngle = 90)
    elif app.keyboardRow == 2:
        drawRegularPolygon(30,600,30,3,fill = 'white',rotateAngle = 90)
    elif app.keyboardRow ==3:
        drawRegularPolygon(550,760,30,3,fill = 'white',rotateAngle = 90)

def getDifficulty(x):
    if 207<=x<=507:
        return 0
    elif 607<=x<=907:
        return 1
    elif 1007<=x<=1307:
        return 2
def getMode(x):
    if 100<=x<=450:
        return 0
    elif 550<=x<=950:
        return 1
    elif 1050<=x<=1400:
        return 2

def goScreen2(app):
    print(app.selectedDiff)
    setUp(app)
    app.listOfBoardNames = []
    if app.selectedDiff < 3 or app.selectedDiff ==4:
        if app.selectedDiff == 4:
            for filename in os.listdir('/Users/ryansong/Python/SudokuCode/tp-starter-files/boards/'):
                if filename.endswith('.txt') and str(app.difficulties[2]) in filename:
                    pathToFile = f'tp-starter-files/boards/{filename}'
                    # app.fileContents = readFile(pathToFile)
                    # print(app.fileContents)
                    app.listOfBoardNames.append(pathToFile)
        else:
            for filename in os.listdir('/Users/ryansong/Python/SudokuCode/tp-starter-files/boards/'):
                if filename.endswith('.txt') and str(app.difficulties[app.selectedDiff]) in filename:
                    pathToFile = f'tp-starter-files/boards/{filename}'
                    # app.fileContents = readFile(pathToFile)
                    # print(app.fileContents)
                    app.listOfBoardNames.append(pathToFile)
    elif app.selectedDiff == 3:
        app.competitionMode = True
        pathToFile = f'contest0-starter-file.txt'
        app.listOfBoardNames = [pathToFile]
        app.listofActions[0] = 'No Hints!'
        app.listofActions[3] = "Singletons off!"
        app.listofActions[4] = "Autofill off!"
    app.boardPath = f'{random.choice(app.listOfBoardNames)}'
    loadBoardFromFile(app,app.boardPath)
    if app.modes[app.selectedMode] == 'keyboard-only':
        if findEmpty(app)!=None:
            app.playerSelect = findEmpty(app)
            app.playerHover = findEmpty(app)
        else:
            print("what?")
    if app.selectedDiff == 4:
        setActiveScreen('screen4')
    else:
        setActiveScreen('screen2')



def findEmpty(app):
    for i in range(app.rows):
        for j in range(app.cols):
            if app.board[i][j]==0 or (i,j) in app.playerMoves:
                return (i,j)
    return None
def readFile(path): #From https://www.cs.cmu.edu/~112-3/notes/term-project.html 
    with open(path, "rt") as f:
        return f.read()

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
    
def loadBoardFromFile(app,path): #From https://www.cs.cmu.edu/~112-3/notes/term-project.html
    fileContents = readFile(path)
    for line in fileContents.splitlines():
        tempList = line.split(" ")
        appendList = [int(j) for j in tempList]
        app.board.append(appendList)
    updatePossibles(app)
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
    app.listofActions[3] = "Strong Hint"

    # updateStates(app)
# end of 'these functions'
def enterMakerMode(app):
    app.maker = True
    setUp(app)
    app.board = [[0 for i in range(app.rows)]for j in range(app.cols)]
    app.keyboardUse = True
    app.mouseUse = True
    app.playerSelect = 0,0
    app.playerHover = 0,0
    setActiveScreen("screen2")

class boardState:
    def __init__(self,board,possibleValues,playerMoves,playerFlags,playerBans,listofActions):
        self.board = board
        self.possibleValues = possibleValues
        self.playerMoves = playerMoves
        self.playerFlags = playerFlags
        self.playerBans = playerBans
        self.listofActions = listofActions
    def __eq__(self,other):
        return isinstance(other,boardState) and self.board == other.board
    def __repr__(self):
        return str(self.playerMoves)
    
def startGame(app):
    goScreen2(app)
    if app.saveboard!=None:
        app.board = app.saveboard 
    stateA = boardState(copy.deepcopy(app.board),copy.deepcopy(app.possibleValues),copy.deepcopy(app.playerMoves),copy.deepcopy(app.playerFlags),copy.deepcopy(app.playerBans),copy.deepcopy(app.listofActions))
    app.listOfStates.append(stateA)
    temp = copy.deepcopy(app.board)
    solveSudoku(app)
    app.solvedBoard = copy.deepcopy(app.board) 
    app.board = copy.deepcopy(temp)
    updatePossibles(app)

def screen1_onMouseMove(app,mouseX,mouseY):
    if 320<=mouseY<=420:
        if app.selectedDiff == None:
            app.difficultyIndex = getDifficulty(mouseX)

    elif 455<=mouseY<=535:
        if 357<=mouseX<=657:
            app.difficultyIndex = 3

    if 575<=mouseY<=625:
        if app.selectedMode ==None:
            app.modeIndex = getMode(mouseX)
    if 735<=mouseY<=785 and 650<mouseX<850:
        app.hoverStart = 1
    else:
        app.hoverStart = 0

def screen1_onMousePress(app,mouseX,mouseY):
    if 320<=mouseY<=420:
        app.difficultyIndex = getDifficulty(mouseX)
        app.selectedDiff = app.difficultyIndex
        if app.saveboard!=None:
            app.saveboard=None
        app.keyboardRow = 1
    
    elif 455<=mouseY<=535:
        if 357<=mouseX<=657:
            app.difficultyIndex = 3
            app.selectedDiff = app.difficultyIndex
            if app.saveboard!=None:
                app.saveboard=None
            app.keyboardRow = 1

    elif 575<=mouseY<=625:
        app.modeIndex = getMode(mouseX)
        app.selectedMode = app.modeIndex
        app.keyboardRow = 2

    elif 735<=mouseY<=785 and 650<mouseX<850:
        app.keyboardRow = 3
        app.hoverStart = True
        if app.selectedDiff==None:
            app.message = "Select a Difficulty!"
        elif app.selectedMode==None:
            app.message = "Select a Mode!"
        else:
            startGame(app)
    elif 50<=mouseY<=150:
        if 200<=mouseX<=500:
            setActiveScreen('screen3')
        elif 1012<=mouseX<=1312:
            enterMakerMode(app)

def screen1_onKeyPress(app, key):
    if key == 'up' and app.keyboardRow>0:
        app.keyboardRow -=1
        if app.keyboardRow ==3:
            app.hoverStart = 1
        else:
            app.hoverStart = 0
    elif key =='down' and app.keyboardRow<3:
        app.keyboardRow +=1
        if app.keyboardRow ==3:
            app.hoverStart = 1
        else:
            app.hoverStart = 0
    elif key =='right':
        if app.keyboardRow ==0:
            if app.miscIndex < 1:app.miscIndex +=1
        elif app.keyboardRow == 1:
            if app.difficultyIndex == None:
                app.difficultyIndex = 0
            if app.difficultyIndex < 4: app.difficultyIndex +=1 
        elif app.keyboardRow ==2:
            if app.modeIndex < 2: app.modeIndex +=1 
    elif key =='left':
        if app.keyboardRow ==0:
            if app.miscIndex > 0:app.miscIndex -=1
        elif app.keyboardRow == 1:
            if app.difficultyIndex > 0: app.difficultyIndex -=1 
        elif app.keyboardRow ==2:
            if app.modeIndex >0: app.modeIndex -=1 
    elif key =='enter':
        if app.keyboardRow ==0:
            if app.miscIndex == 0:
                setActiveScreen("screen3")
            elif app.miscIndex ==1:
                enterMakerMode(app)
        elif app.keyboardRow == 1:
            app.selectedDiff = app.difficultyIndex
            if app.saveboard!=None:
                app.saveboard=None
        elif app.keyboardRow ==2:
            app.selectedMode = app.modeIndex
        elif app.keyboardRow ==3:
            if app.selectedDiff==None:
                app.message = "Select a Difficulty!"
            elif app.selectedMode==None:
                app.message = "Select a Mode!"
            else:
                startGame(app)
                if app.competitionMode:
                    if app.competitionMode:
                        app.listofActions[0] = 'No Hints!'
                        app.listofActions[3] = "Singletons off!"
                        app.listofActions[4] = "Autofill off!"


