from cmu_112_graphics import *
import math
import random
import time

def appStarted(app):
    pass

def keyPressed(app, event):
    pass

def drawWelcomePage(app, canvas):
    pass

def mousePressed(app, event):
    company = app.getUserInput('What is the company code?')
    if (company == None):
        app.message = 'You canceled!'
    else:
        app.showMessage('You entered: ' + name)
        app.message = f'Hi, {name}!'

def redrawAll(app, canvas):
    canvas.create_text(app.width/2, 20,
                       text='FirecarPeaceElites')

runApp(width=400, height=400)