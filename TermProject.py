# Project:
# Ghostly Gummy Grove (GGG)
# Name: Jessica Li
#ID: jli8

#################################################
# Helper functions... from 15-112 hw files
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


#################################################
# source citations
#################################################
'''
https://www.anycodings.com/1questions/5726842/how-to-move-objects-diagonally-in-tkinters-canvas
https://www.w3schools.com/python/ref_random_randint.asp 
https://christianjmills.com/Notes-on-Procedural-Map-Generation-Techniques/#binary-space-partition-rooms
https://doodle-halloween-2018.fandom.com/wiki/The_Great_Ghoul_Duel_Wiki
https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#exampleSnake
https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#nQueens
https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#usingModes 
https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf
'''

import math, copy, random

from cmu_112_graphics import *

def appStarted(app):
    app.player = [(app.width//2, app.height//2)]
    app.playerSize = 10
    app.map = [
    [0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,1,0,0,0,0,0],
    [0,0,0,0,1,0,0,0,1,0],
    [1,0,0,0,1,0,0,0,1,0],
    [2,2,0,0,0,0,0,1,0,0],
    [2,2,0,0,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,1,0,0,0,0,0,0,0],
    [0,0,1,0,0,1,1,1,1,0],
    [0,0,1,0,0,0,0,0,1,0]]
    app.cols = len(app.map[0])
    app.rows = len(app.map)
    app.cW = app.width//app.cols
    app.cH = app.height//app.cols
    app.gameOver = False
    app.timer = 60
    app.timerDelay = 1000
    app.score = 0
    app.ogSpirits = [[0]*10 for x in range(10)]
    app.spiritColor = "dodgerBlue2"
    app.blah = createRandomSpiritsMap(app)
    app.enterBase = False
    app.score = 0
    app.curScore = 0
    #enemy stuffs
    app.enemy = [spawnEnemy(app)]
    app.eScore = 0
    app.eCurScore = 0
    app.eDirections = [(0,-1), (0, 1), (1, 0), (-1,0)]
    app.spiritFound = True
    app.eEnterBase = False

def timerFired(app):
    if(app.gameOver == False):
        if app.timer == 0:
            app.gameOver = True
        if app.gameOver == False:
            if app.timer % 15 == 0:
                app.blah = createRandomSpiritsMap(app)
            if(app.timer % 0.5 == 0):
                moveEnemy(app)
                scoreEnemy(app)
            app.timer -= 1

def keyPressed(app, event):
    if(app.gameOver == False):
        if(event.key == 'Up'):
            app.direction = (0, -1)
            #movePlayer(app)
            pickUpnMove(app)
            scoring(app)
        elif (event.key == 'Down'):
            app.direction = (0, 1)
            #movePlayer(app)
            pickUpnMove(app)
            scoring(app)
        elif (event.key == 'Left'):
            app.direction = (-1, 0)
            #movePlayer(app)
            pickUpnMove(app)
            scoring(app)
        elif (event.key == 'Right'):
            app.direction = (1, 0)
            #movePlayer(app)
            pickUpnMove(app)
            scoring(app)

def getCellBounds(app, row, col):
    mapW  = app.width
    mapH = app.height
    x0 = mapW * col / app.cols 
    x1 = mapW * (col+1) / app.cols
    y0 = mapH * row / app.rows
    y1 = mapH * (row+1) / app.rows
    return (x0, y0, x1, y1)

def isMoveLegal(app):
    # check if its at the borders of it the corners of the character(square)
    # belongs in any cell whose value is 1 or has block
    # if next move one of the corners will be within range of block then backtrack
    (ox, oy) = app.player[0]
    (dx, dy) = app.direction
    (nx, ny) = (ox + dx, oy + dy)
    temp = (nx, ny)
    temp2=getCell(app, temp[0]-app.playerSize, temp[1]-app.playerSize)
    temp3=getCell(app, temp[0]+app.playerSize, temp[1]+app.playerSize)
    temp4=getCell(app, temp[0]+app.playerSize, temp[1]-app.playerSize)
    temp5=getCell(app, temp[0]-app.playerSize, temp[1]+app.playerSize)
    # print(app.map[temp2[0]][temp2[1]], end = " ")
    # print(temp3, end = " ")
    # print(temp4, end = " ")
    # print(temp5)
    if(temp[0]<app.playerSize or temp[0]>app.width-app.playerSize):
        return False
    if(temp[1]<app.playerSize or temp[1]>app.height-app.playerSize):
        return False
    else:
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
    return (int(y),int(x))
    
# def movePlayer(app):
#     (ox, oy) = app.player[0]
#     (dx, dy) = app.direction
#     (nx, ny) = (ox + dx, oy + dy)
#     if(isMoveLegal(app)):
#         app.player[0] = (nx, ny)
    #adds spirit to player 2d list when touched
    # save the head player location
    # insert another spirit in place of it if spirit collected and add on head to new position
    # else pop the last element of player

def createRandomSpiritsMap(app):
    temp = [[0]*10 for x in range(10)]
    for r in range (10):
        for c in range(10):
            if(app.map[r][c] == 0):
                temp[r][c] = random.randint(0,4)
    return temp

def distance(app, x1, x2, y1, y2):
    return math.sqrt(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))

def pickUpnMove(app):
    (x, y) = app.player[0]
    (dx, dy) = app.direction
    (nx, ny) = (x + dx, y + dy)

    if(isMoveLegal(app)):
        #app.player[0] = (nx, ny)
        # print("called")
        (c1x, c1y)=(x-app.playerSize, y-app.playerSize)
        (c2x, c2y)=(x+app.playerSize, y-app.playerSize)
        (c3x, c3y)=(x-app.playerSize, y+app.playerSize)
        (c4x, c4y)=(x+app.playerSize, y+app.playerSize)
        tempCell = getCell(app, x, y)
        # print(tempCell)
        for r in range(len(app.blah)):
            for c in range(len(app.blah[r])):
                if(app.blah[r][c] == 1):
                    if(tempCell[0] == r and tempCell[1]==c):
                        # print("hehe")
                        if(distance(app, c1x, c*app.cW, c1y, r*app.cH) <= app.cW/2 or 
                        distance(app, c2x, c*app.cW, c2y, r*app.cH) <= app.cW/2 or
                        distance(app, c3x, c*app.cW, c3y, r*app.cH) <= app.cW/2 or 
                        distance(app, c4x, c*app.cW, c4y, r*app.cH) <= app.cW/2 ):
                            app.blah[r][c]=0
                            app.player[0] = (x,y)
                            app.player.insert(0,(nx,ny))
                            app.curScore += 1
                            print(app.player)
                else:
                    app.player[0] = (nx, ny)
                    # for i in range(len(app.player)):
                    #     (tx, ty) = app.player[i]
                    #     (dx2, dy2) = app.direction
                    #     (nx2, ny2) = (tx + dx2, ty + dy2)
                    #     print((nx2, ny2))
                    #     app.player[i] = (nx2, ny2)

def spawnEnemy(app):
    r = random.randint(0, len(app.map)-1)
    c = random.randint(0, len(app.map)-1)
    while(app.map[r][c] != 0 or app.blah[r][c]==1):
        r = random.randint(0, len(app.map)-1)
        c = random.randint(0, len(app.map)-1)
    x = app.cH//2 + c*app.cH
    y = app.cW//2 + r*app.cW
    return (x,y)

def eIsValid(app, dx, dy):
    (ox, oy) = app.enemy[0]
    (nx, ny) = (ox + dx*app.cH, oy + dy * app.cW)
    temp = (nx, ny)
    temp2=getCell(app, temp[0]-app.playerSize, temp[1]-app.playerSize)
    temp3=getCell(app, temp[0]+app.playerSize, temp[1]+app.playerSize)
    temp4=getCell(app, temp[0]+app.playerSize, temp[1]-app.playerSize)
    temp5=getCell(app, temp[0]-app.playerSize, temp[1]+app.playerSize)
    if(temp[0]<app.playerSize or temp[0]>app.width-app.playerSize):
        return False
    if(temp[1]<app.playerSize or temp[1]>app.height-app.playerSize):
        return False
    if(app.blah[temp2[0]][temp2[1]] == 1):
        app.spiritFound = True
        return True
    elif(app.blah[temp3[0]][temp3[1]] == 1):
        app.spiritFound = True
        return True
    elif(app.blah[temp4[0]][temp4[1]] == 1):
        app.spiritFound = True
        return True
    elif(app.blah[temp5[0]][temp5[1]] == 1):
        app.spiritFound = True
        return True
    else:
        app.spiritFound = False
        if(app.map[temp2[0]][temp2[1]] != 1 and app.map[temp2[0]][temp2[1]]!=2):
            return True
        elif(app.map[temp3[0]][temp3[1]] != 1 and app.map[temp3[0]][temp3[1]]!=2):
            return True
        elif(app.map[temp4[0]][temp4[1]] != 1 and app.map[temp4[0]][temp4[1]]!=2):
            return True
        elif(app.map[temp5[0]][temp5[1]] != 1 and app.map[temp5[0]][temp5[1]]!=2):
            return True
    return False

def moveEnemy(app):
    if(app.timer>20):
        moved = False
        canMove = []
        for i in range(len(app.eDirections)):
            boop = app.eDirections[i]
            if(eIsValid(app, boop[0], boop[1])):
                if app.spiritFound:
                    (x, y) = app.enemy[0]
                    (dx, dy) = boop
                    (nx, ny) = (x + dx*app.cH, y + dy*app.cH)
                    app.enemy[0] = (nx, ny)
                    # app.eCurScore += 1
                    app.eScore += 1
                    print(app.eCurScore)
                    heh = getCell(app, nx, ny)
                    app.blah[heh[0]][heh[1]] = 0
                    moved = True
                else:
                    canMove.append((boop))
        hehe = random.randint(0,len(canMove)-1)
        rando = canMove[hehe]
        if(moved == False):
            if(eIsValid(app, rando[0], rando[1])):
                (tx, ty) = app.enemy[0]
                app.enemy[0] = (tx + rando[0]*app.cH, ty + rando[1]*app.cW)
    # else:
    #     (ex, ey)= app.enemy[0]
    #     if(y)
    #     if(eIsValid(app,-1,0)):




def scoreEnemy(app):
    temp = app.enemy[0]
    temp2=getCell(app, temp[0]-app.playerSize, temp[1]-app.playerSize)
    temp3=getCell(app, temp[0]+app.playerSize, temp[1]+app.playerSize)
    temp4=getCell(app, temp[0]+app.playerSize, temp[1]-app.playerSize)
    temp5=getCell(app, temp[0]-app.playerSize, temp[1]+app.playerSize)
    if(app.map[temp2[0]][temp2[1]] == 2 or
        app.map[temp3[0]][temp3[1]] == 2 or
        app.map[temp4[0]][temp4[1]] == 2 or
        app.map[temp5[0]][temp5[1]] == 2):
        app.eEnterBase = not app.eEnterBase
        # app.eScore+= app.eCurScore
        # app.eCurScore = 0
    else:
        app.eEnterBase = not app.eEnterBase

def scoring(app):
    (ox, oy) = app.player[0]
    (dx, dy) = app.direction
    (nx, ny) = (ox + dx, oy + dy)
    temp = (nx, ny)
    temp2=getCell(app, temp[0]-app.playerSize, temp[1]-app.playerSize)
    temp3=getCell(app, temp[0]+app.playerSize, temp[1]+app.playerSize)
    temp4=getCell(app, temp[0]+app.playerSize, temp[1]-app.playerSize)
    temp5=getCell(app, temp[0]-app.playerSize, temp[1]+app.playerSize)
    # print(app.map[temp2[0]][temp2[1]], end = " ")
    # print(temp3, end = " ")
    # print(temp4, end = " ")
    # print(temp5)
    if(app.map[temp2[0]][temp2[1]] == 2 or
        app.map[temp3[0]][temp3[1]] == 2 or
        app.map[temp4[0]][temp4[1]] == 2 or
        app.map[temp5[0]][temp5[1]] == 2):
        app.enterBase = not app.enterBase
        app.score+= app.curScore
        app.curScore = 0
        # app.player = app.player[0]
    else:
        app.enterBase = not app.enterBase

def drawPlayer(app, canvas):
    temp = app.player[0]
    canvas.create_rectangle(temp[0]-app.playerSize, temp[1]-app.playerSize,
                            temp[0]+app.playerSize, temp[1]+app.playerSize, fill = "springGreen4")
def drawEnemy(app, canvas):
    temp = app.enemy[0]
    canvas.create_rectangle(temp[0]-app.playerSize, temp[1]-app.playerSize,
                            temp[0]+app.playerSize, temp[1]+app.playerSize, fill = "blue violet")
    # if(len(app.player)>1):
    #     # print("hehe")
    #     for i in range(1,len(app.player)):
    #         # print("boo")
    #         (c, r) = app.player[i]
    #         print(app.player[i])
    #         canvas.create_oval(c+app.cW/4, r+app.cH/4,
    #                                 c-app.cW/4, r-app.cH/4, fill = "black", outline = app.spiritColor)
def drawMap(app, canvas):
    for r in range (len(app.map)):
        for c in range(len(app.map[r])):
            block = "white"
            if(app.map[r][c]):
                block = "grey"
            if(app.map[r][c] == 2):
                block = "light goldenrod"
            canvas.create_rectangle(getCellBounds(app, r, c), fill = block, outline = block)

def drawOgSpiritsMap(app, canvas):
    for r in range(len(app.blah)):
        for c in range(len(app.blah)):
            if(app.blah[r][c] == 1):
                canvas.create_oval(c*app.cW +app.cW/4, r*app.cH +app.cH/4,
                                    (c+1)*app.cW-app.cW/4, (r+1)*app.cH-app.cH/4, fill = app.spiritColor, outline = app.spiritColor)

def drawScore(app, canvas):
    canvas.create_text(0, 0, text=f'  score: {app.score}', anchor = "nw")

def drawEScore(app, canvas):
    canvas.create_text(app.width, 0, text=f'Enemy score: {app.eScore}    ', anchor = "ne")

def drawTimer(app, canvas):
    canvas.create_text(app.width//2, 0, text=f'time: {int(app.timer)}', anchor = "n")

def drawGameOver(app, canvas):
    if(app.gameOver):
        canvas.create_text(app.width//2, app.height//2, text = "Game Over!", font = "arial 30")

# def drawViewWindow(app, canvas):
#     (x,y) = app.player[0]
#     c1x = x - 3*app.cW
#     c1y = y - 3*app.cW
#     c2x = x + 3*app.cW
#     c2y = y + 3*app.cW
#     for r in range (c1x, c2x,app.cW):
#         block = "white"
#         if(app.map[r][c]):
#             block = "black"
#         if(app.map[r][c] == 2):
#             block = "purple"
#         canvas.create_rectangle(getCellBounds(app, r, c), fill = block, outline = block)

def redrawAll(app, canvas):
    drawMap(app, canvas)
    #drawViewWindow(app, canvas)
    drawOgSpiritsMap(app, canvas)
    drawTimer(app, canvas)
    drawPlayer(app, canvas)
    drawScore(app, canvas)
    drawEScore(app, canvas)
    drawGameOver(app, canvas)
    drawEnemy(app, canvas)
    pass


#################################################
# main
#################################################

def main():
    # playGGG()
    runApp(width=500, height=500)

if __name__ == '__main__':
    main()