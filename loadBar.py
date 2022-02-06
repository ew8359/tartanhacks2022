from cmu_112_graphics import *
import math
import random
import time

class loadBar(object):
    allBars = []

    # This function constructs a loading bar object
    def __init__(self, nCells, cx, cy, cellSize):
        self.nCells = nCells
        self.cx = 200
        self.cy = 200
        self.cellSize = cellSize
    
    # This function gets the canvas dimensions
    def getCanvasBounds(self):
        x0 = self.x - self.width / 2
        x1 = self.x + self.width / 2
        y0 = self.y - self.height / 2
        y1 = self.y + self.height / 2
        return x0, y0, x1, y1

    # This function draws the load bar object
    def drawLoadBar(self, canvas):
        # First calculate the sizes and positions
        # draw shape

        margin = self.cellSize / 8
        length = self.nCells * self.cellSize + (self.cellSize+1) * margin
        height = self.cellSize + 2 * margin

        # Draw the external bar boundary
        left = self.cx - length/2
        right = self.cx + length/2
        top = self.cy - height/2
        bottom = self.cy + height/2
        canvas.create_rectangle(left, top, right, bottom)

        # Load
        for t in range(1, self.nCells+1):
            time.sleep(1)
            for i in range(t):
                x = i * self.cellSize + (i+1) * margin
                y = top + margin
                canvas.create_rectangle(x, y, x+self.cellSize, y+self.cellSize)
