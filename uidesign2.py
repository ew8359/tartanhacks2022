from cmu_112_graphics import *
import math
import random
import time
import alphaquery as aq
import yahoofinance as yf
import company
import re
import MarketWatch_options as mo
import numpy as np 
import historical_data as l
import priceOption as po
import markov

Tinker = ''

# pages = ["homepage", "stock", "option", "detailed"]
# class MyApp(App):
def rgbString(color):
    r,g,b = color
    return f'#{r:02x}{g:02x}{b:02x}'

def appStarted(app):
    app.page = "homepage"
    if app.page == "homepage":
        app.homemessage = 'Click the mouse to enter the company name!'
    app.l = []
    app.diff = 0
    app.chartW = app.width*0.9
    app.chartH = app.height*0.8
    app.chart = False
    app.exit = [0, 0, app.width*0.05, app.height*0.05] # x1, y1, x2, y2
    app.next = [app.width, app.height, app.width-app.width*0.05, app.height-app.height*0.05] # x1, y1, x2, y2
    app.option = []
    app.optionP = 1
    app.reg = False
    app.estimation = ""
    app.markov = []

def keyPressed (app,event):
    if app.page == "stock":
        if event.key == 'k':
            app.chart = not app.chart
        elif event.key == 'r':
            app.reg = not app.reg
    elif app.page == "option":
        if (event.key == "Right" or event.key == "Down") and app.optionP <= 2:
            app.optionP += 1
        elif (event.key == "Left" or event.key == "Up") and app.optionP >= 2:
            app.optionP -= 1
        else:
            pass

def exit(app, x, y):
    if x <= app.exit[2] and x >= app.exit[0] and y <= app.exit[3] and y >= app.exit[1]:
        return True
    else:
        return False

def next(app, x, y):
    if x >= app.next[2] and x <= app.next[0] and y >= app.next[3] and y <= app.next[1]:
        return True
    else:
        return False

def convertIndex(app, x, y, p):
    option1 = app.option[0]
    option2 = app.option[1]
    option3 = app.option[2]
    rows1 = option1.shape[0]
    rows2 = option2.shape[0]
    rows3 = option3.shape[0]
    if p == 1:
        rows = rows1+2
        cols = 7 # callPrice, callBid, callAsk, Strike, putPrice, putBid, putAsk
        cellH = app.height*0.9/rows
        cellW = app.width*0.8/cols
        cellx = -1
        for j in range(0, 7):
            if app.width*0.1+cellW*j <= x and app.width*0.1+cellW*(j+1) >= x:
                cellx = j
        celly = -1
        for i in range (0, rows1+2):
            if app.height*0.05+cellH*i <= y and app.height*0.05+cellH*(i+1) >= y:
                celly = i
    elif p == 2:
        rows = rows2+2
        cols = 7 # callPrice, callBid, callAsk, Strike, putPrice, putBid, putAsk
        cellH = app.height*0.9/rows
        cellW = app.width*0.8/cols
        cellx = -1
        for j in range(0, 7):
            if app.width*0.1+cellW*j <= x and app.width*0.1+cellW*(j+1) <= x:
                cellx = j
        celly = -1
        for i in range (0, rows2+2):
            if app.height*0.05+cellH*i <= y and app.height*0.05+cellH*(i+1):
                celly = i
    else:
        rows = rows3+2
        cols = 7 # callPrice, callBid, callAsk, Strike, putPrice, putBid, putAsk
        cellH = app.height*0.9/rows
        cellW = app.width*0.8/cols
        cellx = -1
        for j in range(0, 7):
            if app.width*0.1+cellW*j <= x and app.width*0.1+cellW*(j+1) <= x:
                cellx = j
        celly = -1
        for i in range (0, rows3+2):
            if app.height*0.05+cellH*i <= y and app.height*0.05+cellH*(i+1):
                celly = i
    return [cellx, celly]

def mousePressed(app, event):
    if app.page == "homepage":
        info = "incorrect company"
        while info == "incorrect company":
            name = app.getUserInput('Please enter the stock ticker (e.g. AAPL, TSLA, ...)')
            if type(name) == str:
                app.showMessage('You entered: ' + name)
                global Tinker 
                Tinker = name
                if Tinker.isalpha():
                    Tinker = Tinker.upper()
                    if (Tinker in company.S) and (len(Tinker) > 0):
                        info = Tinker
                        app.l = l.historical_data(Tinker)
                        app.markov = markov.markov(app.l[-30: ], 1)
                        app.diff = max(app.l) - min(app.l)
                    else:
                        info = "incorrect company"
                        app.showMessage("The company you entered is incorrect, please reenter")
                else:
                    info = "incorrect company"
                    app.showMessage("The company you entered is incorrect, please reenter")
            else:
                info = "incorrect company"
                app.showMessage("You entered nothing, please reenter")
        app.page = "stock"
        app.stockmessage = "Current stock price of " + Tinker + " is " + str(yf.findPrice(Tinker))
    elif app.page == "stock":
        # goes from stock to option
        # goes from stock back to homepage
        if exit(app, event.x, event.y):
            app.page = "homepage"
        elif next(app, event.x, event.y):
            app.page = "option"
            app.option = mo.marketwatch_options(Tinker)
        pass
    elif app.page == "option":
        # goes from option to details
        # goes from option back to stock
        if exit(app, event.x, event.y):
            app.page = "stock"
            app.optionP = 1
        else:
            try:
                app.option = mo.marketwatch_options(Tinker)
                L = convertIndex(app, event.x, event.y, app.optionP)
                if L[0] >= 0 and L[0] != 3 and L[1] >= 2:
                    option1 = app.option[0]
                    option2 = app.option[1]
                    option3 = app.option[2]
                    rows1 = option1.shape[0]
                    rows2 = option2.shape[0]
                    rows3 = option3.shape[0]
                    if L[0] <= 2:
                        category = 'call'
                    else:
                        category = 'put'
                    price = str(po.priceOption_wrapper(app.optionP-1, L[1]-2, Tinker, category, 30))
                    newprice = ""
                    for i in range(len(price)):
                        if price[i] == ":":
                            newprice = price[i+2:]
                    newprice = round(float(newprice[:-1:]), 2)
                    if app.optionP == 1:
                        op = option1
                    elif app.optionP == 2:
                        op = option2
                    else:
                        op = option3
                    strike = 0.0
                    strike_str = op['Strike'][L[1]-2]
                    if ',' in strike_str:
                        strike = 1000 + float(re.findall("\d+\.\d+", strike_str)[0])
                    else:
                        strike = float(re.findall("\d+\.\d+", strike_str)[0])
                    currPutPrice = float(op['Put_Price'][L[1]-2])
                    currPutBid = float(op['Put_Bid'][L[1]-2])
                    currPutAsk = float(op['Put_Ask'][L[1]-2])
                    currCallPrice = float(op['Call_Price'][L[1]-2])
                    currCallBid = float(op['Call_Bid'][L[1]-2])
                    currCallAsk = float(op['Call_Ask'][L[1]-2])
                    Linfo = [currCallPrice, currCallBid, currCallAsk, strike, currPutPrice, currPutBid, currPutAsk]
                    if category == 'call':
                        app.optionmessage = f"The current price for this call option is {currCallPrice}. The current bid is {currCallBid}, and the current ask is {currCallAsk}."
                        app.strikemessage = f"The strike price is {strike}. Current stock price is {yf.findPrice(Tinker)}, so if the option expires today, the earning is {round(max(0, yf.findPrice(Tinker)-strike), 2)}." 
                        app.estimation = "Our estimation for the price is " + str(newprice) + "."
                    else:
                        app.optionmessage = f"The current price for this put option is {currPutPrice}. The current bid is {currPutBid}, and the current ask is {currPutAsk}."
                        app.strikemessage = f"The strike price is {strike}. Current stock price is {yf.findPrice(Tinker)}, so if the option expires today, the earning is {round(max(0, strike-yf.findPrice(Tinker)), 2)}."
                        app.estimation = "Our estimation for the price is " + str(newprice) + "."
                    app.page = "detailed"
            except:
                pass
        pass
    else: # app.page = detailed
        if exit(app, event.x, event.y):
            app.page = "option"
        pass

def drawdetailed(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = rgbString((255, 228, 225)))
    canvas.create_text(app.width/2, app.height*0.3, text=app.optionmessage, font='Arial 24 bold')
    canvas.create_text(app.width/2, app.height*0.5, text=app.strikemessage, font='Arial 24 bold')
    canvas.create_text(app.width/2, app.height*0.7, text=app.estimation, font='Arial 24 bold')

def option(app, canvas):
    option1 = app.option[0]
    option2 = app.option[1]
    option3 = app.option[2]

    rows1 = option1.shape[0]
    rows2 = option2.shape[0]
    rows3 = option3.shape[0]

    if app.optionP == 1:
        rows = rows1+2
        cols = 7 # callPrice, callBid, callAsk, Strike, putPrice, putBid, putAsk
        cellH = app.height*0.9/rows
        cellW = app.width*0.8/cols
        for i in range (0, rows1+2):
            if i == 0:
                canvas.create_text(app.width/2, app.height*0.05, text="Expiration date: 20220211", font='Arial 16 bold')
            elif i == 1:
                L = ["Call Price", "Call Bid", "Call Ask", "Strike", "Put Price", "Put Bid", "Put Ask"]
                for j in range (0, 7):
                    canvas.create_text(app.width*0.1+cellW/2+cellW*j, app.height*0.05+(cellH/2)+cellH, text=L[j], font='Arial 16 bold')
            else:
                try:
                    strike = 0.0
                    strike_str = option1['Strike'][i-2]
                    if ',' in strike_str:
                        strike = 1000 + float(re.findall("\d+\.\d+", strike_str)[0])
                    else:
                        strike = float(re.findall("\d+\.\d+", strike_str)[0])
                    #strike = float(re.findall("\d+\.\d+", option1['Strike'][i-2])[0])
                    currPutPrice = float(option1['Put_Price'][i-2])
                    currPutBid = float(option1['Put_Bid'][i-2])
                    currPutAsk = float(option1['Put_Ask'][i-2])
                    currCallPrice = float(option1['Call_Price'][i-2])
                    currCallBid = float(option1['Call_Bid'][i-2])
                    currCallAsk = float(option1['Call_Ask'][i-2])
                    L = [currCallPrice, currCallBid, currCallAsk, strike, currPutPrice, currPutBid, currPutAsk]
                    for j in range (0, 7):
                        canvas.create_text(app.width*0.1+cellW/2+cellW*j, app.height*0.05+(cellH/2)+cellH*i, text=L[j], font='Arial 14 bold')
                except:
                    canvas.create_line(app.width*0.1, app.height*0.05+(cellH/2)+cellH*i, app.width*0.9, app.height*0.05+(cellH/2)+cellH*i)
    elif app.optionP == 2:
        rows = rows2+2
        cols = 7 # callPrice, callBid, callAsk, Strike, putPrice, putBid, putAsk
        cellH = app.height*0.9/rows
        cellW = app.width*0.8/cols
        for i in range (0, rows2+2):
            if i == 0:
                canvas.create_text(app.width/2, app.height*0.05, text="Expiration date: 20220218", font='Arial 16 bold')
            elif i == 1:
                L = ["Call Price", "Call Bid", "Call Ask", "Strike", "Put Price", "Put Bid", "Put Ask"]
                for j in range (0, 7):
                    canvas.create_text(app.width*0.1+cellW/2+cellW*j, app.height*0.05+(cellH/2)+cellH*i, text=L[j], font='Arial 16 bold')
            else:
                try:
                    strike = 0.0
                    strike_str = option2['Strike'][i-2]
                    if ',' in strike_str:
                        strike = 1000 + float(re.findall("\d+\.\d+", strike_str)[0])
                    else:
                        strike = float(re.findall("\d+\.\d+", strike_str)[0])
                    # strike = float(re.findall("\d+\.\d+", option2['Strike'][i-2])[0])
                    currPutPrice = float(option2['Put_Price'][i-2])
                    currPutBid = float(option2['Put_Bid'][i-2])
                    currPutAsk = float(option2['Put_Ask'][i-2])
                    currCallPrice = float(option2['Call_Price'][i-2])
                    currCallBid = float(option2['Call_Bid'][i-2])
                    currCallAsk = float(option2['Call_Ask'][i-2])
                    L = [currCallPrice, currCallBid, currCallAsk, strike, currPutPrice, currPutBid, currPutAsk]
                    for j in range (0, 7):
                        canvas.create_text(app.width*0.1+cellW/2+cellW*j, app.height*0.05+(cellH/2)+cellH*i, text=L[j], font='Arial 14 bold')
                except:
                    canvas.create_line(app.width*0.1, app.height*0.05+(cellH/2)+cellH*i, app.width*0.9, app.height*0.05+(cellH/2)+cellH*i)
    else:
        rows = rows3+2
        cols = 7 # callPrice, callBid, callAsk, Strike, putPrice, putBid, putAsk
        cellH = app.height*0.9/rows
        cellW = app.width*0.8/cols
        for i in range (0, rows3+2):
            if i == 0:
                canvas.create_text(app.width/2, app.height*0.05, text="Expiration date: 20220225", font='Arial 16 bold')
            elif i == 1:
                L = ["Call Price", "Call Bid", "Call Ask", "Strike", "Put Price", "Put Bid", "Put Ask"]
                for j in range (0, 7):
                    canvas.create_text(app.width*0.1+cellW/2+cellW*j, app.height*0.05+(cellH/2)+cellH*i, text=L[j], font='Arial 16 bold')
            else:
                try:
                    strike = 0.0
                    strike_str = option3['Strike'][i-2]
                    if ',' in strike_str:
                        strike = 1000 + float(re.findall("\d+\.\d+", strike_str)[0])
                    else:
                        strike = float(re.findall("\d+\.\d+", strike_str)[0])
                    # strike = float(re.findall("\d+\.\d+", option3['Strike'][i-2])[0])
                    currPutPrice = float(option3['Put_Price'][i-2])
                    currPutBid = float(option3['Put_Bid'][i-2])
                    currPutAsk = float(option3['Put_Ask'][i-2])
                    currCallPrice = float(option3['Call_Price'][i-2])
                    currCallBid = float(option3['Call_Bid'][i-2])
                    currCallAsk = float(option3['Call_Ask'][i-2])
                    L = [currCallPrice, currCallBid, currCallAsk, strike, currPutPrice, currPutBid, currPutAsk]
                    for j in range (0, 7):
                        canvas.create_text(app.width*0.1+cellW/2+cellW*j, app.height*0.05+(cellH/2)+cellH*i, text=L[j], font='Arial 14 bold')
                except:
                    canvas.create_line(app.width*0.1, app.height*0.05+(cellH/2)+cellH*i, app.width*0.9, app.height*0.05+(cellH/2)+cellH*i)

def drawk(app,canvas): # fancy
    for i in range (len(app.l)-1):
        x1 = (app.chartW/len(app.l))*i+(app.width*0.05)
        x2 = (app.chartW/len(app.l))*(i+1)+(app.width*0.05)
        y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH*0.8)
        y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH*0.8)
        if y2>y1:
            color="red"
        else:
            color="green"
        x = (x2-x1)/3
        canvas.create_rectangle(x1+x,y1,x2-x,y2,fill=color)

def singlelinreg(x,y): # the dimension of x and y should be the same. Get the inspiration (not direct code) from Wikipedia and real python website:
    n = x.shape[0] # https://en.wikipedia.org/wiki/Coefficient_of_determination
    xypara = np.dot(x,y)/n # https://realpython.com/numpy-scipy-pandas-correlation-python/
    xpara = x.sum()/n
    ypara = y.sum()/n
    x2para = (x**2).sum()/n
    k = (xypara - xpara * ypara)/(x2para - xpara**2)
    b = ypara - k*xpara
    return k,b

def drawregression(app,canvas):
    x = []
    y = []
    targetline = []
    for i in range (len(app.l)):
        xele = i
        yele = app.l[i]
        x.append(xele)
        y.append(yele)
    m = np.array(x)
    n = np.array(y)
    k,b = singlelinreg(m,n)
    for i in range (len(app.l)*2):
        targetline.append(k*i+b)
    for i in range (len(targetline)-1):
        if targetline[i]>=max(app.l):
            break
        x1 = (app.chartW*2/len(targetline))*i+(app.width*0.05)
        x2 = (app.chartW*2/len(targetline))*(i+1)+(app.width*0.05)
        y1 = abs(app.chartH-((targetline[i]-min(app.l))/app.diff)*app.chartH*0.8)
        y2 = abs(app.chartH-((targetline[i+1]-min(app.l))/app.diff)*app.chartH*0.8)
        canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.001,fill=rgbString((0, 255, 0)))
        canvas.create_text(app.width*0.9, app.height*0.1, text = f"y = {round(k, 2)}x+{round(b, 2)}")

def drawline(app,canvas): # fancy
    for i in range (len(app.l)-1):
        x1 = (app.chartW/len(app.l))*i+(app.width*0.05)
        x2 = (app.chartW/len(app.l))*(i+1)+(app.width*0.05)
        y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH*0.8)
        y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH*0.8)
        if y2>y1:
            color="red"
        else:
            color="green"
        x = (x2-x1)/3
        canvas.create_line(x1,y1,x2,y2,width=app.chartW/len(app.l)*0.2,fill="black")

def drawExit(app, canvas):
    canvas.create_rectangle(app.exit[0],app.exit[1],app.exit[2],app.exit[3],fill="white")
    canvas.create_text(app.exit[2]/2,  app.exit[3]/2,
                        text="Exit", font='Arial 16 bold')

def drawNext(app, canvas):
    canvas.create_rectangle(app.next[0],app.next[1],app.next[2],app.next[3],fill="white")
    canvas.create_text((app.next[0]+app.next[2])/2, (app.next[1]+app.next[3])/2,
                        text="Next", font='Arial 16 bold')

def axis(app,canvas): # x and y axis, +app.chartH*0.1
    canvas.create_line((app.width*0.05),app.chartH*0.1,(app.width*0.05),app.chartH,width=3,fill='black')
    canvas.create_line((app.width*0.05),app.chartH,app.chartW+(app.width*0.05),app.chartH,width=3,fill='black')
    canvas.create_line((app.width*0.05),app.chartH*0.1,10+(app.width*0.05),10+app.chartH*0.1,width=3,fill='black')
    canvas.create_line((app.width*0.05)+app.chartW,app.chartH,app.chartW-10+(app.width*0.05),app.chartH-12,width=3,fill='black')
    for i in range(9):
        canvas.create_line((app.width*0.05),app.chartH/10*(i+1)+app.chartH*0.1,10+(app.width*0.05),app.chartH/10*(i+1)+app.chartH*0.1,width=3,fill='black')
    for i in range(10):
        canvas.create_line(app.chartW/10*i+(app.width*0.05),app.chartH,app.chartW/10*i+(app.width*0.05),app.chartH-10,width=3,fill='black')

def redrawAll(app, canvas):
    if app.page == "homepage":
        canvas.create_text(app.width/2,  app.height/2,
                        text=app.homemessage, font='Arial 24 bold')
    elif app.page == "stock":
        drawExit(app, canvas)
        drawNext(app, canvas)
        drawline(app,canvas)
        axis(app,canvas)
        if app.chart == False:
            drawk(app,canvas)
        else:
            drawline(app,canvas)
        canvas.create_text(app.width/2,  app.height*0.87, text=app.stockmessage, font='Arial 20 bold')
        markovmg = f'The probability that the stock goes up tomorrow = {app.markov[0]}, and goes down = {app.markov[1]}.'
        canvas.create_text(app.width/2,  app.height*0.95, text=markovmg, font='Arial 20 bold')
        if app.reg == True:
            drawregression(app,canvas)
    elif app.page == "option":
        drawExit(app, canvas)
        option(app, canvas)
        pass
    else:
        drawdetailed(app, canvas)
        drawExit(app, canvas)
        pass
    
runApp(width = 1400, height = 700)