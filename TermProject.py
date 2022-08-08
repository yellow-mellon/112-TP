# Project:
# Ghostly Gummy Grove (GGG)

import math, copy, random

from cmu_112_graphics import *

def appStarted(app):
    app.player = [[app.width//2, app.height//2]]
    app.map = [
    [0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,0],
    [1,0,0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,1,0],
    [0,0,1,0,0,0,0,0,1,0]]
    app.cols = len(app.map[0])
    app.rows = len(app.map)
    app.cW = app.width/app.cols
    app.cH = app.height/app.cols

def keyPressed(app, event):
    if(event.key == 'Up'):
        app.direction = (0, -10)
        movePlayer(app)
    elif (event.key == 'Down'):
        app.direction = (0, 10)
        movePlayer(app)
    elif (event.key == 'Left'):
        app.direction = (-10, 0)
        movePlayer(app)
    elif (event.key == 'Right'):
        app.direction = (10, 0)
        movePlayer(app)

def getCellBounds(app, row, col):
    mapW  = app.width
    mapH = app.height
    x0 = mapW * col / app.cols 
    x1 = mapW * (col+1) / app.cols
    y0 = mapH * row / app.rows
    y1 = mapH * (row+1) / app.rows
    return (x0, y0, x1, y1)

def isMoveLegal(app):
    temp = copy.deepcopy(app.player[0])
    temp[0] += app.direction[0]
    temp[1] += app.direction[1]

    temp2=getCell(app, temp[0]-10, temp[1]-10)
    temp3=getCell(app, temp[0]+10, temp[1]+10)
    temp4=getCell(app, temp[0]+10, temp[1]-10)
    temp5=getCell(app, temp[0]-10, temp[1]+10)
    print(app.map[temp2[0]][temp2[1]], end = " ")
    print(temp3, end = " ")
    print(temp4, end = " ")
    print(temp5)
    if(temp[0]<10 or temp[0]>app.width-10):
        return False
    elif(temp[1]<10 or temp[1]>app.height-10):
        return False
    if(app.map[temp2[0]][temp2[1]] == 1):
        print("j")
        return False
    if(app.map[temp3[0]][temp3[1]] == 1):
        print("j")
        return False
    if(app.map[temp4[0]][temp4[1]] == 1):
        print("j")
        return False
    if(app.map[temp5[0]][temp5[1]] == 1):
        print("j")
        return False
    return True

def getCell(app,x,y):
    x //= app.cW
    y //= app.cH
    return (int(x),int(y))
    
def movePlayer(app):
    if(isMoveLegal(app)):
        app.player[0][0] += app.direction[0]
        app.player[0][1] += app.direction[1]

def drawPlayer(app, canvas):
    canvas.create_rectangle(app.player[0][0]-10, app.player[0][1]-10,
                            app.player[0][0]+10, app.player[0][1]+10, fill = "red")
def drawMap(app, canvas):
    
    for r in range (len(app.map)):
        for c in range(len(app.map[r])):
            block = "white"
            if(app.map[r][c]):
                block = "black"
            canvas.create_rectangle(getCellBounds(app, c, r), fill = block, outline=block)

def drawSpirit(app, canvas):
    pass

def redrawAll(app, canvas):
    drawMap(app, canvas)
    drawPlayer(app, canvas)
    drawSpirit(app, canvas)
    pass


#################################################
# main
#################################################

def main():
    # playGGG()
    runApp(width=500, height=500)

if __name__ == '__main__':
    main()