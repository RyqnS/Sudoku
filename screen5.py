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
from screen4 import *

def screen5_onScreenStart(app):
    app.image = Image.open('haha.jpeg') #https://chrome.google.com/webstore/detail/jumpscare-tab/lgffjphcglhjodndldapdedaemkkkcbo
    app.redImage = makeRedImage(app.image)

    # Convert each PIL image to a CMUImage for drawing
     # the following code was taken from demo code for animated gifs and pixel editting
    app.image = CMUImage(app.image)
    app.redImage = CMUImage(app.redImage)
    app.killTimer = 0
    app.stepsPerSecond = 20
    app.hindaduh = random.randint(0,2)
    app.spritetwo = loadAnimatedGif(app, 'aga.gif')# All gifs were taken from Tenor
    app.spriteCounter2 = 0
    app.spriteCounter3 = 0
    app.spritethree = loadAnimatedGif(app, 'fnaf.gif')# All gifs were taken from Tenor




def screen5_redrawAll(app):  # the following code was taken from demo code for animated gifs and pixel editting
    if app.hindaduh == 0:
        drawRect(0,0,app.width,app.height,fill = 'black')
        pilImage = app.redImage.image
        drawImage(app.redImage, 760, 400, align='center',
                width=pilImage.width//10 * abs((app.killTimer)**1.5),
                height=pilImage.height//10 * abs((app.killTimer)**1.5))
    elif app.hindaduh == 1:
        spriteB = app.spritetwo[app.spriteCounter2]
        drawImage(spriteB, app.width//2, app.height//2, align='center',width = 1512,height = 840)
        
    else:
        spriteB = app.spritethree[app.spriteCounter3]
        drawImage(spriteB, app.width//2, app.height//2, align='center',width = 1512,height = 840)
    

def screen5_onStep(app):  # the following code was taken from demo code for animated gifs and pixel editting
    app.killTimer +=1
    if app.hindaduh == 0:
        if app.killTimer>=20:
            os._exit(0)
    elif app.hindaduh ==1:
        if app.killTimer >=30:
            os._exit(0)
    elif app.hindaduh ==2:
        if app.killTimer >=5:
            os._exit(0)
    app.spriteCounter2 = (1 + app.spriteCounter2) % len(app.spritetwo)
    app.spriteCounter3 = (1 + app.spriteCounter3) % len(app.spritethree)

