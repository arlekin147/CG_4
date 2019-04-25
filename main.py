import numpy as np
import matplotlib.pyplot as plt
import pylab
import random
import copy
from matplotlib.widgets import Button



def addButtonClicked(event = 0):
        ax.clear()
        PlotWindow(window)
        snips = list()
        for i in range(0, 10):
            snips.insert(i, Snip(GetRandomCoord(), GetRandomCoord(),
                             GetRandomCoord(), GetRandomCoord()))
   

        showSnips(snips, window)
        plt.show()

class Window():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2


class Snip():
    def __init__(self, x1, y1, x2, y2):
        if(x2 < x1):
            temp = x1
            x1 = x2
            x2 = temp
            temp = y1
            y1 = y2
            y2 = temp
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.IsDot1Moved = False
        self.IsDot2Moved = False


def getCode(x, y, window):
    code = 0
    if(y > window.y1):
        code += 8
    elif(y < window.y2):
        code += 4
    if(x > window.x2):
        code += 2
    elif(x < window.x1):
        code += 1
    return code


def bytePrint(code):
    i = 8
    answer = ""
    while(i > 0):
        if(code & i != 0):
            answer += str(1)
        else:
            answer += str(0)
        i >>= 1
    print(answer)


def PlotSnip(snip, color="blue"):
    ax.plot([snip.x1, snip.x2], [snip.y1, snip.y2], label="ogo", color=color)


def PlotWindow(window):
    ax.plot([window.x1, window.x1], [window.y1, window.y2],
            label="ogo", color="red")  # left
    ax.plot([window.x1, window.x2], [window.y1, window.y1],
            label="ogo", color="red")  # up
    ax.plot([window.x2, window.x2], [window.y1, window.y2],
            label="ogo", color="red")  # right
    ax.plot([window.x1, window.x2], [window.y2, window.y2],
            label="ogo", color="red")  # down

def getNearestDot(x, y, window):
    if x == window.x1: return window.x2
    if x == window.x2: return window.x1
    if abs(x - window.x1) < abs(x - window.x2): return window.x1
    else: return window.x2



def GetRandomCoord():
    return random.randint(0, 10)


def Trunc(snip, window):

    if snip.x1 < window.x1 or snip.x2 > window.x2:
        if getCode(snip.x1, snip.y1, window) != 0 and not snip.IsDot1Moved:
            if snip.x1 < window.x1:
                nextX = window.x1
            else:
                nextX = window.x2
            snip.y1 = np.polyval(np.polyfit([snip.x1, snip.x2], [
                                snip.y1, snip.y2], deg=1),
                                nextX)
            snip.x1 = nextX
            snip.IsDot1Moved = True
        else:
            if snip.x2 > window.x2:
                nextX = window.x2
            else:
                nextX = window.x1
            snip.y2 = np.polyval(np.polyfit([snip.x1, snip.x2], [
                                snip.y1, snip.y2], deg=1),
                                nextX)
            snip.x2 = nextX
            snip.IsDot2Moved = True
    else:
        if getCode(snip.x1, snip.y1, window) != 0 and not snip.IsDot1Moved:
            if snip.y1 > window.y1:
                nextY = window.y1
            else:
                nextY = window.y2
            snip.y1 = nextY
            snip.x1 = SolveOnY(np.polyfit([snip.x1, snip.x2],
             [snip.y1, snip.y2], deg = 1), nextY)
            snip.IsDot1Moved = True
        else:
            if snip.y2 > window.y1:
                nextY = window.y1
            else:
                nextY = window.y2
            snip.y2 = nextY
            snip.x2 = SolveOnY(np.polyfit([snip.x1, snip.x2],
             [snip.y1, snip.y2], deg = 1), nextY)
            snip.IsDot1Moved = True


def IsInWindow(snip, window):
    dot1 = getCode(snip.x1, snip.y1, window)
    dot2 = getCode(snip.x2, snip.y2, window)

    if((dot1 & dot2) != 0):
        return False
    elif (dot1 == 0 or dot2 == 0) or (snip.IsDot1Moved and snip.IsDot2Moved):
        return True
    else:
        Trunc(snip, window)
        return IsInWindow(snip, window)

def OnTheBorder(x, y, window):
    if (x == window.x1 or x == window.x2 ) and y < window.y1 and y > window.y2: return True
    return False


def showSnips(snips, window):
    for snip in snips:
            PlotSnip(snip)
    for snip in snips:
            snipCopy = copy.copy(snip)
            if IsInWindow(snipCopy, window): PlotSnip(snip, "green")

def SolveOnY(line, y):
    return (float)(y - line[1]) / line[0]

def main():
    
    a = [2.0, 2.0]
    b = 3.0
    global window
    window = Window(1, 5, 5, 1)
    global fig
    global ax
    fig, ax = pylab.subplots()
    axes_button_add = pylab.axes([0.7, 0.05, 0.25, 0.075])
    button_add = Button(axes_button_add, 'Перегенерировать!')
    button_add.on_clicked(addButtonClicked)
    addButtonClicked()
    


if __name__ == "__main__":
    main()
