try: from cmu_cs3_graphics import *
except: from cmu_graphics import *
import random

from runAppWithScreens import *

def screen3_onScreenStart(app):
    pass
def screen3_redrawAll(app):
    drawLabel("Sudoku Help Screen",app.width//2,3*app.height//24,size = 40)
    drawLabel("Sudoku is a logic-based, combinatorial number-placement puzzle.",app.width//2,4*app.height//24,size=20)
    drawLabel("The objective is to fill a 9 × 9 grid with digits",app.width//2,5*app.height//24,size = 20)
    drawLabel("so that each column, each row, and each of the nine 3 × 3 subgrids that",app.width//2,6*app.height//24,size = 20)
    drawLabel("compose the grid contain all of the digits from 1 to 9",app.width//2,7*app.height//24,size = 20)
 
    drawLabel("Keyboard-only mode:",app.width//2,8*app.height//24,size = 30,bold = True)
    drawLabel("Use up-left-right-down arrowkeys to move selection window",app.width//2,9*app.height//24,size = 20)
    drawLabel("'l (lowercase L)' to toggle legal vales",app.width//2,10*app.height//24,size = 20)
    drawLabel("'h' for a hint",app.width//2,11*app.height//24,size = 20)
    drawLabel("'z' to undo last placement",app.width//2,12*app.height//24,size = 20)
    drawLabel("'f' to toggle flag mode",app.width//2,13*app.height//24,size = 20)
    drawLabel("'s' to place a singleton",app.width//2,14*app.height//24,size = 20)
    drawLabel("'escape' to return to main menu",app.width//2,15*app.height//24,size = 20)
    drawLabel("space + enter to finish making a custom board",app.width//2,16*app.height//24,size = 20)


    drawLabel("Mouse-only mode:",app.width//2,19*app.height//24,size = 30,bold = True)
    drawLabel("Move mouse around to move selection window",app.width//2,20*app.height//24,size = 20)
    drawLabel("Use the numpad on the right to input values",app.width//2,21*app.height//24,size = 20)
    drawLabel("Use the buttons on the right to get hints,toggle legals, enter flag mode, & place singletons",app.width//2,22*app.height//24,size = 20)
    drawLabel("Red means flag mode, blue means input mode",app.width//2,23*app.height//24,size = 20)
    drawRect(50,50,300,100,fill = 'lightblue',border = 'black')
    drawLabel("Back to Menu",200,100,size = 40,bold = True,align = 'center')

def screen3_onMousePress(app,mouseX,mouseY):
    if 50<=mouseY<=150:
        if 50<=mouseX<=350:
            setActiveScreen('screen1')
def screen3_onKeyPress(app,key):
    if key == 'enter':
        setActiveScreen('screen1')