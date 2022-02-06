from cmu_112_graphics import *
import random
import math
import numpy as np 
from math import sqrt
import time
import pandas as pd
import alphaquery as aq
import yahoofinance as yf
import company

StartDate =''
Enddate = ''
Mode = ''

class MyApp(App):
    def appStarted(self):
        self.message = 'Click the mouse to enter The Tinker!'

    def mousePressed(self, event):
        global name
        name = self.getUserInput('The Tinker')
        if type(name) == str:
            self.showMessage('You entered: ' + name)
            if name.isalpha():
                name = name.upper()
                if (name in company.S) and (len(name) > 0):
                    print (name, aq.findSigma(name))
                    print (name, yf.findPrice(name))
                else: 
                    print ("incorrect company")
            else:
                print ("incorrect company")
        else:
            self.showMessage('You entered: (NONE)')    
        global Mode
        mode = "y"
        Mode = mode

    def redrawAll(self, canvas):
        font = 'Arial 24 bold'
        canvas.create_text(self.width/2,  self.height/2,
                            text=self.message, font=font)
MyApp(width = 1400, height = 700)

def tinkerstart():#get information for a stock from excel forms


    tinker = Tinker 
    dp = pd.read_excel(f'{tinker}.xlt',usecols=["Close"]) 
    dt = pd.read_excel (f'{tinker}.xlt',usecols=["Date"]) 

    l= dp.values.tolist()
    time = dt.values.tolist()




    pricelist = []
    for price in range(len(l)):
        num = l[price][0]
        pricelist.append(num)

    for date in range(len(time)):

        wp=l[date][0]

        time[date].append(wp)

    startweek = int(StartDate)
    endweek = int(Enddate)

    if endweek-startweek<=21:
        class MyApp(App):
            def appStarted(self):
                self.message = 'Time Interval Error: Too Close'
            def redrawAll(self, canvas):
                font = 'Arial 24 bold'
                canvas.create_text(self.width/2,  self.height/2,
                                    text=self.message, font=font)
        MyApp(width=600, height=300)
    elif startweek<time[0][0]-7:
        class MyApp(App):
            def appStarted(self):
                self.message = 'Start Time Error: Too Early'
            def redrawAll(self, canvas):
                font = 'Arial 24 bold'
                canvas.create_text(self.width/2,  self.height/2,
                                    text=self.message, font=font)
        MyApp(width=600, height=300)
    elif endweek>time[len(time)-1][0]-7:
        class MyApp(App):
            def appStarted(self):
                self.message = 'End Time Error: Not Updated Yet'
            def redrawAll(self, canvas):
                font = 'Arial 24 bold'
                canvas.create_text(self.width/2,  self.height/2,
                                    text=self.message, font=font)
        MyApp(width=600, height=300)
    elif startweek%100>31 or endweek%100>31 or startweek//100%100>12 or \
        endweek//100%100>12:
        class MyApp(App):
            def appStarted(self):
                self.message = 'Invalid Date'
            def redrawAll(self, canvas):
                font = 'Arial 24 bold'
                canvas.create_text(self.width/2,  self.height/2,
                                    text=self.message, font=font)
        MyApp(width=600, height=300)

    else:
        counter = 0 
        startmark = None
        endmark=None
        finallist = []  


        for vailddate in time:
        
            if vailddate[0] == startweek:
                startmark =  counter
            elif vailddate[0] == endweek:
                endmark =  counter
            counter += 1
        if startmark == None:
            counter=0
            for point in range(len(time)):
                if time[point][0]//100==startweek//100:
                    startmark = counter
                counter+=1
        elif endmark== None:
            counter=0
            for point in range(len(time)):
                if time[point][0]//100==endweek//100:
                    endmark = counter
                counter+=1
        templist = time[startmark:endmark]
            
        for info in range(len(templist)):
            num = templist[info][1]
            finallist.append(num)

        
    return finallist

def calcMean(a,b):#cited from wikipedia and sina blog
    #http://blog.sina.com.cn/s/blog_8bdd25f80101c5pq.html
    #https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    length =min(len(a),len(b))
    x=a[:length]
    y=b[:length]
    sum_x = sum(x)
    sum_y = sum(y)
    n = len(x)
    x_mean = float(sum_x+0.0)/n
    y_mean = float(sum_y+0.0)/n
    return x_mean,y_mean

def pearson(a,b):#cited from wikipedia and CSDN blog:#http://blog.sina.com.cn/s/blog_8bdd25f80101c5pq.html
    length =min(len(a),len(b))#https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    x=a[:length]
    y=b[:length]
    x_mean,y_mean = calcMean(x,y)	
    n = len(x)
    sumTop = 0.0
    sumBottom = 0.0
    x_pow = 0.0
    y_pow = 0.0
    for i in range(n):
        sumTop += (x[i]-x_mean)*(y[i]-y_mean)
    for i in range(n):
        x_pow += math.pow(x[i]-x_mean,2)
    for i in range(n):
        y_pow += math.pow(y[i]-y_mean,2)
    sumBottom = math.sqrt(x_pow*y_pow)
    p = sumTop/sumBottom
    return p

def std(n):# given a list of numbers, calculate the standard deviation
    sumtotal = sum(n)
    average = sumtotal/len(n)
    stdsq = 0
    for i in n:
        stdsq+= (i-average)**2
    std = (stdsq/(len(n)))**0.5
    return round(std,2)

def singlelinreg(x,y): #the demonsion of x and y should be the same. Get the inspiration (not direct code) from Wikipedia and real python website:
    n = x.shape[0]#https://en.wikipedia.org/wiki/Coefficient_of_determination
    xypara = np.dot(x,y)/n #https://realpython.com/numpy-scipy-pandas-correlation-python/
    xpara = x.sum()/n
    ypara = y.sum()/n
    x2para = (x**2).sum()/n
    
    k = (xypara - xpara * ypara)/(x2para - xpara**2)
    b = ypara - k*xpara
    return k,b

drawlist = tinkerstart()

index = 0
altstart = 0
altend = 0
val=0
while (index < len(drawlist)):
    if (str(drawlist[index]) =='nan' ):
        altstart = index

        for k in range(index,len(drawlist)):
            if str(drawlist[k])!='nan':
                altend = k
                val=round((drawlist[altend]-\
                    drawlist[altstart-1])/(altend-altstart+2),3)
                drawlist.pop(index)
                drawlist.insert(altstart, drawlist[altstart-1]+val)
    else:
        index += 1

mode = Mode

if mode =='y':# comparision mode
    class MyApp(App):
        def appStarted(self):
            self.message = 'Click the mouse to enter the company code!'

        def mousePressed(self, event):
            name = self.getUserInput('The Second Tinker')
            self.showMessage('You entered: ' + name)
            global Tinker 
            Tinker = name
            startdate = self.getUserInput('Start Date')
            self.showMessage('You entered: ' + startdate)
            global StartDate
            StartDate=startdate
            enddate = self.getUserInput('End Date')
            self.showMessage('You entered: ' + enddate)
            global Enddate
            Enddate = enddate

        def redrawAll(self, canvas):
            font = 'Arial 24 bold'
            canvas.create_text(self.width/2,  self.height/2,
                                text=self.message, font=font)
    MyApp(width=600, height=300)
    class ProApp(App):
        def appStarted(self):
            self.message1 = 'Pearson Value: the similarity shared'
            self.message2 = 'Pearson Value range from -1 to 1, 1 means 100% positively correlated and -1 means 100% negatively correlated'
            self.message3 = 'A Pearson Value graeter than 0.8 or less than -0.8 means very strong relationship '
            self.message4 = 'A Pearson Value graeter than 0.6 or less than -0.6 means relatively strong relationship '
            self.message5 = 'A Pearson Value equals 0 means no relationship '
            self.message6 = 'You can click on the stock to get the Press but you need to press 1 to switch. Press K to make it fancy'


        def redrawAll(self, canvas):
            font = 'Arial 10 bold'
            canvas.create_text(self.width/2,  self.height/7*1,
                                text=self.message1, font=font)
            canvas.create_text(self.width/2,  self.height/7*2,
                                text=self.message2, font=font)
            canvas.create_text(self.width/2,  self.height/7*3,
                                text=self.message3, font=font)
            canvas.create_text(self.width/2,  self.height/7*4,
                                text=self.message4, font=font)  
            canvas.create_text(self.width/2,  self.height/7*5,
                                text=self.message5, font=font)
            canvas.create_text(self.width/2,  self.height/7*6,
                                text=self.message6, font=font)                                       
    ProApp(width=900, height=400)
    twostock = [drawlist]
    twostock.append(tinkerstart())
    index = 0
    while (index < len(twostock[1])):
        if (str(twostock[1][index]) =='nan' ):
            twostock[1].pop(index)
        else:
            index += 1
    
    def appStarted(app):

        app.rows = 40
        app.cols = 40
        app.click1=[]
        app.l = twostock
        numberofweeks1 = len(app.l[0])
        app.chartH1 = max(app.l[0])-min(app.l[0])

        while app.chartH1<400:
            app.chartH1*=1.1
        while app.chartH1>500:
            app.chartH1 = app.chartH1//2
        app.color = False
        app.chartW1 = app.chartH1 * 1.2
        app.diff1 = max(app.l[0])-min(app.l[0])
        app.intv1 = app.chartW1//(len(app.l[0]))
        app.weekprice1 = 0
        app.drawSpecificweekPrice1 =False
        app.checkspecific1price=True
        app.similaritylist1 =[]
#####################################################
        app.click2=[]
        numberofweeks2 = len(app.l[1])
        app.weekprice2 = 0
        app.chartH2 = max(app.l[1])-min(app.l[1])
        app.drawSpecificweekPrice2 = False

        while app.chartH2<400:
            app.chartH2*=1.1
        while app.chartH2>500:
            app.chartH2 = app.chartH2//1.1
        app.chartW2 = app.chartH2 * 1.2
        app.diff2 = max(app.l[1])-min(app.l[1])
        app.intv2 = app.chartW2//(len(app.l[1]))
        app.weekprice2 = 0
        app.checkspecific2price=False
        app.similaritylist2 =[]
        app.pearson=0
        app.chartH= max(app.chartH1,app.chartH2)
        app.chartW= max(app.chartW1,app.chartW2)
    def createFluctuation(app,canvas):
        FluctuationIndex = round(std(app.l[0])/std(app.l[1]),3)
        canvas.create_text(450,650,text=f'FluctuationIndex (Quotient of two standard deviations)={FluctuationIndex}'\
                                ,fill='black',font=\
                                    "Helvetica 15 bold underline")
    def getCellBounds(app, row, col):#cited from 112 webpage https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        gridWidth  = app.width 
        gridHeight = app.height 
        x0 = gridWidth * col / app.cols
        x1 = gridWidth * (col+1) / app.cols
        y0 = gridHeight * row / app.rows
        y1 = gridHeight * (row+1) / app.rows
        return (x0, y0, x1, y1)
    def drawBoard(app, canvas):#background
        for row in range(app.rows):
            for col in range(app.cols):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill='light grey')
    def keyPressed(app,event):
        if event.key=='k':
            app.color= not app.color
        elif event.key =='1':
            app.checkspecific1price= not app.checkspecific1price
            app.checkspecific2price= not app.checkspecific2price
    def drawtwo(app,canvas):  # 2 k charts
            for i in range (len(app.l[0])-1):
                x1 = (app.chartW1/len(app.l[0]))*i
                x2 = (app.chartW1/len(app.l[0]))*(i+1)
                y1 = abs(app.chartH1-((app.l[0][i]-\
                    min(app.l[0]))/app.diff1)*app.chartH1)
                y2 = abs(app.chartH1-((app.l[0][i+1]-\
                    min(app.l[0]))/app.diff1)*app.chartH1)
                r = app.chartH1*0.01*(1/(len(app.l[0])))
                
                if app.color == False:
                    color = 'blue'
                else:
                    color = random.choice(['lightGreen','gold','black'])
                
                canvas.create_text(650,200, text="stock1",
                       fill=color, font="Helvetica 20 bold underline")
                canvas.create_oval(x1-r,y1-r,x1+r,y1+r)
                canvas.create_oval(x2-r,y2-r,x2+r,y2+r)
                canvas.create_line(x1,y1,x2,y2,width=app.chartW1*0.005,fill=color)
            for i in range (len(app.l[1])-1):
                x1 = (app.chartW2/len(app.l[1]))*i
                x2 = (app.chartW2/len(app.l[1]))*(i+1)
                y1 = abs(app.chartH2-((app.l[1][i]-\
                    min(app.l[1]))/app.diff2)*app.chartH2)
                y2 = abs(app.chartH2-((app.l[1][i+1]-\
                    min(app.l[1]))/app.diff2)*app.chartH2)
                r = app.chartH2*0.01*(1/(len(app.l[1])))
                
                if app.color == False:
                    color = 'red'
                else:
                    color = random.choice(['blue','purple','pink'])
                canvas.create_text(650,300, text="stock2",
                       fill=color, font="Helvetica 20 bold underline")
                canvas.create_oval(x1-r,y1-r,x1+r,y1+r)
                canvas.create_oval(x2-r,y2-r,x2+r,y2+r)
                canvas.create_line(x1,y1,x2,y2,width=app.chartW2*0.005,\
                    fill=color)

    def mousePressed(app,event):
        x=event.x
        y=event.y
        if app.checkspecific2price== True:
            app.drawSpecificweekPrice1=False
            for i in range (len(app.l[1])-1):
                    x1 = (app.chartW2/len(app.l[1]))*i
                    x2 = (app.chartW2/len(app.l[1]))*(i+1)
                    y1 = abs(app.chartH2-((app.l[1][i]-\
                        min(app.l[1]))/app.diff2)*app.chartH2)
                    y2 = abs(app.chartH2-((app.l[1][i+1]-\
                        min(app.l[1]))/app.diff2)*app.chartH2)
                    
                    if x1<=x<=x2 and y1*0.85<=y<=y2*1.25:
                        if app.click2==[]:
                            
                            app.click2.append(x1+x2)
                            app.click2.append(y1+y2)
                            app.weekprice2 = round((app.l[1][i+1]+\
                                app.l[1][i])/2,3)
                            app.drawSpecificweekPrice2  = True
                            
                        else:
                            app.click2.pop(0)
                            app.click2.pop(0)
                            app.click2.append(x1+x2)
                            app.click2.append(y1+y2)
                            app.weekprice2 = round((app.l[1][i+1]+\
                                app.l[1][i])/2,3)
                            app.drawSpecificweekPrice2  = True         

        elif app.checkspecific1price== True:
            app.drawSpecificweekPrice2=False    
            for i in range (len(app.l[0])-1):
                    x1 = (app.chartW1/len(app.l[0]))*i
                    x2 = (app.chartW1/len(app.l[0]))*(i+1)
                    y1 = abs(app.chartH1-((app.l[0][i]-\
                        min(app.l[0]))/app.diff1)*app.chartH1)
                    y2 = abs(app.chartH1-((app.l[0][i+1]-\
                        min(app.l[0]))/app.diff1)*app.chartH1)
                    
                    if x1<=x<=x2 and y1*0.85<=y<=y2*1.25:
                        if app.click1==[]:
                            
                            app.click1.append(x1+x2)
                            app.click1.append(y1+y2)
                            app.weekprice1 = round((app.l[0][i+1]+\
                                app.l[0][i])/2,3)
                            app.drawSpecificweekPrice1  = True
                            
                        else:
                            app.click1.pop(0)
                            app.click1.pop(0)
                            app.click1.append(x1+x2)
                            app.click1.append(y1+y2)
                            app.weekprice1 = round((app.l[0][i+1]+\
                                app.l[0][i])/2,3)
                            app.drawSpecificweekPrice1  = True
    def getPearson(app): # Pearson value
        similaritylist1=[]
        similaritylist2=[]
        pearsonNum=0
        for i in range (len(app.l[0])-1):
                    x1 = (app.chartW1/len(app.l[0]))*i
                    x2 = (app.chartW1/len(app.l[0]))*(i+1)
                    y1 = abs(app.chartH1-((app.l[0][i]-\
                        min(app.l[0]))/app.diff1)*app.chartH1)
                    y2 = abs(app.chartH1-((app.l[0][i+1]-\
                        min(app.l[0]))/app.diff1)*app.chartH1)
                    similaritylist1.append(y1)
        for i in range (len(app.l[1])-1):
                    x1 = (app.chartW2/len(app.l[1]))*i
                    x2 = (app.chartW2/len(app.l[1]))*(i+1)
                    y1 = abs(app.chartH2-((app.l[1][i]-\
                        min(app.l[1]))/app.diff2)*app.chartH2)
                    y2 = abs(app.chartH2-((app.l[1][i+1]-\
                        min(app.l[1]))/app.diff2)*app.chartH2)
                    similaritylist2.append(y1)
        pearsonNum = pearson(similaritylist1,similaritylist2)
        return pearsonNum
        
    def drawPearson(app,canvas):

        if len(app.l[0])/len(app.l[1])>1.05 or len(app.l[0])/len(app.l[1])<0.95:
            canvas.create_text(400,500,text=\
                'WARNING: THE TIME INTVERTAL IS DIFFERENT THE PEARSON IS INACCURATE'\
                 ,fill='orange',font="Helvetica 15 bold underline") 
                 
        p = round(getPearson(app),4)
        canvas.create_text(500,600,text=f'Pearson correlation={p}'\
                                ,fill='black',font=\
                                    "Helvetica 20 bold underline")

    def axis(app,canvas): # x and y axis
        canvas.create_line(0,0,0,app.chartH,width=3,fill='brown')
        canvas.create_line(0,app.chartH,app.chartW,app.chartH,width=3,fill='brown')
        canvas.create_line(0,0,10,10,width=3,fill='brown')
        canvas.create_line(app.chartW,app.chartH,app.chartW-10,app.chartH-12,width=3,fill='brown')
        for i in range(9):
            canvas.create_line(0,app.chartH/10*i,10,app.chartH/10*i,width=3,fill='brown')
        for i in range(10):
            canvas.create_line(app.chartW/10*i,app.chartH,app.chartW/10*i,app.chartH-10,width=3,fill='brown')
    
    def redrawAll(app, canvas):
        drawBoard(app, canvas)
        axis(app,canvas)
        drawtwo(app,canvas)
        drawPearson(app,canvas)
        createFluctuation(app,canvas)

        if app.drawSpecificweekPrice1 == True:

            canvas.create_text((app.click1[0])/2,(app.click1[1])/2*0.9,\
                text=f'{app.weekprice1}'\
                            ,fill='black',font="Helvetica 10 bold underline")
        elif app.drawSpecificweekPrice2 == True:
            canvas.create_text((app.click2[0])/2,(app.click2[1])/2*0.9,\
                text=f'{app.weekprice2}'\
                            ,fill='black',font="Helvetica 10 bold underline")
        



    runApp(width=800, height=1000)

else:
    class MyApp(App):
        def appStarted(self):
            self.message1 = 'PRESS P TO GET REGRESSIONAL PREDICTION AND CONFIDENCE INTERVAL!'
            self.message2 = 'PRESS Q TO GET PEARSON PREDICTION!(SIMILAR PATTERNS IN THE PAST)'
            self.message3 = 'PRESS A TO GET ITS AVERAGE PRICE IN THE PAST 3 MONTHS, PAST YEAR, AND PAST 2 YEARS!'
            self.message4 = 'PRESS K TO MAKE IT FANCY! BUT SOME INDEX WILL DISAPPEAR!'
            self.message5 = 'PRESS UP AND DOWN TO CHANGE THE BASE INTEVAL!'
            self.message6 = 'BOLL: THE LINE IN THE MIDDLE IS THE AVERAGE PRICE.UPPER AND LOWER BOUNDS ARE EACH 2 STD AWAY '

        def redrawAll(self, canvas):
            font = 'Arial 12 bold'
            canvas.create_text(self.width/2,  self.height/7,
                                text=self.message1, font=font)
            canvas.create_text(self.width/2,  self.height/7*2,
                                text=self.message2, font=font)
            canvas.create_text(self.width/2,  self.height/7*3,
                                text=self.message3, font=font)
            canvas.create_text(self.width/2,  self.height/7*4,
                                text=self.message4, font=font)
            canvas.create_text(self.width/2,  self.height/7*5,
                                text=self.message5, font=font)
            canvas.create_text(self.width/2,  self.height/7*6,
                                text=self.message6, font=font)
    MyApp(width=900, height=400)

    def appStarted(app):
        app.rows = 40
        app.cols = 40

        app.l = drawlist
        app.predictIntv = 0.8
 
                    
        app.upcount = 0
        app.pearsonPre = False
        numberofweeks = len(app.l)
        app.weekprice=0
        app.chartH = max(app.l)-min(app.l)
        app.drawSpecificweekPrice=False
        app.click=[]
        app.showA = False

        
        while app.chartH<400:
            app.chartH*=1.1
        while app.chartH>500:
            app.chartH = app.chartH//1.1
        app.isk=False
        app.predict=False
        


        app.chartW = app.chartH * 1.2
        app.diff = max(app.l)-min(app.l)
        app.intv = app.chartW//(len(app.l))
    
    
    def averages(app,canvas): # average lines
        if len(app.l)>26:
            hyearAverage = round(sum(app.l[len(app.l)-26:])/26,3)
            xp=(1-26/len(app.l))*app.chartW
            yp = abs(app.chartH-((hyearAverage-min(app.l))/app.diff)*app.chartH)
            canvas.create_line(xp,yp,800,yp,width=5,fill='light blue')
            canvas.create_text(700,yp-10,text='Average Price: Last Half Year',font="Helvetica 10 bold underline",fill='light blue')
            if hyearAverage>app.l[-1]:
                canvas.create_text(250,540,text='Current Price is Lower than the Average Price of the Past 26 weeks',font="Helvetica 10 bold underline",fill='light blue')
            else:
                canvas.create_text(250,540,text='Current Price is Higher than the Average Price of the Past 26 weeks',font="Helvetica 10 bold underline",fill='light blue')
        if len(app.l)>53:
            yearAverage = round(sum(app.l[len(app.l)-52:])/52,3)
            xp=(1-52/len(app.l))*app.chartW
            yp = abs(app.chartH-((yearAverage-min(app.l))/app.diff)*app.chartH)
            canvas.create_line(xp,yp,800,yp,width=5,fill='light blue')
            canvas.create_text(700,yp-10,text='Average Price: Last Year',font="Helvetica 10 bold underline",fill='light blue')
            if hyearAverage>app.l[-1]:
                canvas.create_text(250,560,text='Current Price is Lower than the Average Price of the Past Year',font="Helvetica 10 bold underline",fill='light blue')
            else:
                canvas.create_text(250,560,text='Current Price is Higher than the Average Price of the Past Year',font="Helvetica 10 bold underline",fill='light blue')
        if len(app.l)>106:
            tyearAverage = round(sum(app.l[len(app.l)-106:])/106,3)
            xp=(1-106/len(app.l))*app.chartW
            yp = abs(app.chartH-((tyearAverage-min(app.l))/app.diff)*app.chartH)
            canvas.create_line(xp,yp,800,yp,width=5,fill='light blue')
            canvas.create_text(700,yp-10,text='Average Price: Last 2 Years',font="Helvetica 10 bold underline",fill='light blue')    
            if hyearAverage>app.l[-1]:
                canvas.create_text(250,580,text='Current Price is Lower than the Average Price of the Past 2 Years',font="Helvetica 10 bold underline",fill='light blue')
            else:
                canvas.create_text(250,580,text='Current Price is Higher than the Average Price of the Past 2 Years',font="Helvetica 10 bold underline",fill='light blue')
    
    def getCellBounds(app, row, col):#cited from 112 webpage #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
        gridWidth  = app.width 
        gridHeight = app.height 
        x0 = gridWidth * col / app.cols
        x1 = gridWidth * (col+1) / app.cols
        y0 = gridHeight * row / app.rows
        y1 = gridHeight * (row+1) / app.rows
        return (x0, y0, x1, y1)
    
    def drawBoard(app, canvas):
        for row in range(app.rows):
            for col in range(app.cols):
                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
    
    def findPearson(app,canvas): # short term slice
        baseline = app.l[round(len(app.l)*app.predictIntv):]
        stl = len(baseline)
        bestPearson = -2
        bestList = None
        Pins = 0
        Pine = 0
        for startp in range (len(app.l[:round(len(app.l)*app.predictIntv-stl)])):
            if pearson(app.l[startp:startp+stl],baseline)>bestPearson:
                bestPearson = pearson(app.l[startp:startp+stl],baseline)
                bestList = app.l[startp:startp+stl]
                Pins = startp
                Pine = startp+stl-1
        for k in range(len(app.l)-1):
            if k>= round(len(app.l)*app.predictIntv) and k<=len(app.l):
                x1 = (app.chartW/len(app.l))*k
                x2 = (app.chartW/len(app.l))*(k+1)
                y1 = abs(app.chartH-((app.l[k]-min(app.l))/app.diff)*app.chartH)
                y2 = abs(app.chartH-((app.l[k+1]-min(app.l))/app.diff)*app.chartH)

                canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005,fill='orange')
        for i in range (len(app.l)-1):
            
            if i>= Pins and i<=Pine:
                x1 = (app.chartW/len(app.l))*i
                x2 = (app.chartW/len(app.l))*(i+1)
                y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH)
                y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH)

                canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005,fill='orange')
        
        canvas.create_text(600,600,text='Similarity Shared: '+f'{round(bestPearson,3)}',font="Helvetica 15 bold underline",fill='orange')
    
    def draw(app,canvas):  
        for i in range (len(app.l)-1):
            x1 = (app.chartW/len(app.l))*i
            x2 = (app.chartW/len(app.l))*(i+1)
            y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH)
    
            r = app.chartH*0.01*(1/(len(app.l)))
            
                    
            canvas.create_oval(x1-r,y1-r,x1+r,y1+r)
            canvas.create_oval(x2-r,y2-r,x2+r,y2+r)
            canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005)

            
            
    def findendp(app): # find the start point of prediction line
        for i in range (len(app.l)-1):
            x1 = (app.chartW/len(app.l))*i
            x2 = (app.chartW/len(app.l))*(i+1)
            y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH)
            if i == len(app.l)-2:
                return y2
            
    def keyPressed(app,event):
        if event.key=='k':
            app.isk= not app.isk
        elif event.key=='p':
            app.predict= not app.predict
        elif event.key=='q':
            app.pearsonPre = not app.pearsonPre
        elif event.key=='Up':
            if app.upcount<3:
                app.upcount+=1
        elif event.key=='Down':
            if app.upcount>0:
                app.upcount-=1
        elif event.key=='a':
            app.showA = not app.showA
        if app.upcount == 0:
            app.predictIntv=0.8
        if app.upcount ==1:
            app.predictIntv=0.85
        if app.upcount == 2:
            app.predictIntv = 0.9
        if app.upcount == 3:
            app.predictIntv = 0.95
            
    def axis(app,canvas):
        canvas.create_line(0,0,0,app.chartH,width=3,fill='brown')
        canvas.create_line(0,app.chartH,app.chartW,app.chartH,width=3,fill='brown')
        canvas.create_line(0,0,10,10,width=3,fill='brown')
        canvas.create_line(app.chartW,app.chartH,app.chartW-10,app.chartH-12,width=3,fill='brown')
        for i in range(9):
            canvas.create_line(0,app.chartH/10*i,10,app.chartH/10*i,width=3,fill='brown')
        for i in range(10):
            canvas.create_line(app.chartW/10*i,app.chartH,app.chartW/10*i,app.chartH-10,width=3,fill='brown')

    def mousePressed(app,event):
        x=event.x
        y=event.y

        for i in range (len(app.l)-1):
            x1 = (app.chartW/len(app.l))*i
            x2 = (app.chartW/len(app.l))*(i+1)
            y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH)

            if x1<=x<=x2 and y1*0.85<=y<=y2*1.25:
                if app.click==[]:
                            
                    app.click.append(x1+x2)
                    app.click.append(y1+y2)
                    app.weekprice = round((app.l[i+1]+app.l[i])/2,3)
                    app.drawSpecificweekPrice  = True
                            
                else:
                    app.click.pop(0)
                    app.click.pop(0)
                    app.click.append(x1+x2)
                    app.click.append(y1+y2)
                    app.weekprice = round((app.l[i+1]+app.l[i])/2,3)
                    app.drawSpecificweekPrice  = True    
    def drawk(app,canvas): # fancy
        for i in range (len(app.l)-1):
            x1 = (app.chartW/len(app.l))*i
            x2 = (app.chartW/len(app.l))*(i+1)
            y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH)
            if y2>y1:
                color="red"
                linelen=random.randint(20,50)*(abs(y1-y2))*0.05
            else:
                color="green"
                linelen=random.randint(20,50)*(abs(y1-y2))*0.05
            
            canvas.create_rectangle(x1,y1,x2,y2,fill=color)
            canvas.create_line((x1+x2)*0.5,y2,(x1+x2)*0.5,linelen+y2,fill=color\
                ,width=2)
            canvas.create_line((x1+x2)*0.5,y1,(x1+x2)*0.5,y1-linelen,fill=color\
                ,width=2)
                
    def drawBollingLine(app,canvas):
        bollUpperLine = app.chartH
        bolllowerBound= 700
        bollAverage = 0.5*(bolllowerBound+bollUpperLine)
        averagePrice = sum(app.l)/(len(app.l)-1)
        stdv = std(app.l)
        for i in range (len(app.l)-1):
            x1 = (app.chartW/len(app.l))*i
            x2 = (app.chartW/len(app.l))*(i+1)
            y1 = abs(app.chartH-((app.l[i]-min(app.l))/app.diff)*app.chartH)*0.2+bollUpperLine
            y2 = abs(app.chartH-((app.l[i+1]-min(app.l))/app.diff)*app.chartH)*0.2+bollUpperLine
            canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005,fill='yellow')
        averagePrice = sum(app.l)/(len(app.l)-1)
        graphPricebollUp=  abs(app.chartH-((averagePrice+2*stdv-min(app.l))/app.diff)*app.chartH)*0.2+bollUpperLine
        graphPricebollDw=  abs(app.chartH-((averagePrice-2*stdv-min(app.l))/app.diff)*app.chartH)*0.2+bollUpperLine
        graphPrice=(graphPricebollUp+graphPricebollDw)*0.5
        canvas.create_line(0,graphPricebollUp,1000,graphPricebollUp,width=app.chartW*0.005,fill='blue')
        canvas.create_line(0,graphPrice,1000,graphPrice,width=app.chartW*0.005,fill='blue')
        canvas.create_line(0,graphPricebollDw,1000,graphPricebollDw,width=app.chartW*0.005,fill='blue')
        canvas.create_text(700,(bollUpperLine+bollAverage)*0.5,text='BOLL',fill='blue')
        if app.l[-1]>averagePrice+2*stdv:
            canvas.create_text(600,650,text='Boll indicates that the price may fall',font="Helvetica 15 bold underline")
        elif averagePrice+2*stdv>app.l[-1]>averagePrice:
            canvas.create_text(600,650,text='Boll indicates that the price is higher than usual',font="Helvetica 12 bold underline")
        elif averagePrice>app.l[-1]>averagePrice-2*stdv:
            canvas.create_text(600,650,text='Boll indicates that the price is lower than usual',font="Helvetica 12 bold underline")
        elif app.l[-1]<averagePrice-2*stdv:
            canvas.create_text(600,650,text='Boll indicates that the price may raise',font="Helvetica 15 bold underline")
    def drawregression(app,canvas):
        x=[]
        y=[]
        targetline=[]
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
            x1 = (app.chartW*2/len(targetline))*i
            x2 = (app.chartW*2/len(targetline))*(i+1)
            y1 = abs(app.chartH-((targetline[i]-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((targetline[i+1]-min(app.l))/app.diff)*app.chartH)
            canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005,fill='white')
    def drawr(app,canvas):

        p=[]
        q=[]
        targetlineshort=[]
        baseline = app.l[round(len(app.l)*app.predictIntv):]
        for i in range (len(baseline)):
            xele = i
            yele = baseline[i]
            p.append(xele)
            q.append(yele)
        a = np.array(p)
        b = np.array(q)
        c,d = singlelinreg(a,b)
        for i in range (len(baseline)*4):
            targetlineshort.append(c*i+d)
        for i in range (len(targetlineshort)-1):

            if targetlineshort[i]>=max(app.l):
                break
            x1 = (app.chartW*1/len(targetlineshort))*i+app.predictIntv*app.chartW
            x2 = (app.chartW*1/len(targetlineshort))*(i+1)+app.predictIntv*app.chartW
            y1 = abs(app.chartH-((targetlineshort[i]-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((targetlineshort[i+1]-min(app.l))/app.diff)*app.chartH)
            
            canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005,fill='purple')
      
        x=[]
        y=[]
        targetline=[]
        for i in range (len(app.l)):
            xele = i
            yele = app.l[i]
            x.append(xele)
            y.append(yele)
        m = np.array(x)
        n = np.array(y)
        k,b = singlelinreg(m,n)
        predictslope = (k+c)/2
        startp=findendp(app)
        for i in range(0,len(baseline)-3,2):
            if baseline[-1]+i*predictslope>=max(app.l):
                break
            x1 = (app.chartW*0.5/len(baseline))*i+app.chartW
            x2 = (app.chartW*0.5/len(baseline))*(i+1)+app.chartW
            y1 = abs(app.chartH-((baseline[-1]+i*predictslope-min(app.l))/app.diff)*app.chartH)
            y2 = abs(app.chartH-((baseline[-1]+(i+1)*predictslope-min(app.l))/app.diff)*app.chartH)
            canvas.create_line(x1,y1,x2,y2,width=app.chartW*0.005,fill='red')
 
    def drawPredictionArea(app,canvas):# confidence interval


        baseline = app.l[round(len(app.l)*app.predictIntv):]

        ltvar = std(app.l)
        stvar = std(baseline)
        startp=findendp(app)
        trianglelowerbound= baseline[-1]+(ltvar+stvar)
        triangleupperbound= baseline[-1]-(ltvar+stvar)
        


        canvas.create_polygon(app.chartW,abs(app.chartH-((baseline[-1]-min(app.l))/app.diff)*app.chartH),\
                 app.chartW*(2-app.predictIntv),abs(app.chartH-((trianglelowerbound-min(app.l))/app.diff)*app.chartH),\
                 app.chartW*(2-app.predictIntv),abs(app.chartH-((triangleupperbound-min(app.l))/app.diff)*app.chartH),fill='pink')
    def showBoard(app,canvas):
        canvas.create_rectangle(0,600,300,800,fill='white')
        canvas.create_text(150,620,text='white line: Long Term Regression',font="Helvetica 10 bold underline")
        canvas.create_text(150,640,text='purple line: Short Term Regression',font="Helvetica 10 bold underline")
        canvas.create_text(150,660,text='pink area: 95 percent confidence interval',font="Helvetica 10 bold underline")
        canvas.create_text(150,680,text='red dashed: regressional prediction',font="Helvetica 10 bold underline")

    def redrawAll(app, canvas):
    
        drawBoard(app, canvas)
        axis(app,canvas)
        if app.isk==False:
            draw(app,canvas)
            drawBollingLine(app,canvas)
            canvas.create_text(750,50,text=Tinker,fill='yellow',font="Helvetica 20 bold underline")
            
            
            
            if app.predict==True:
                showBoard(app,canvas)
                drawPredictionArea(app,canvas)
                drawregression(app,canvas)
                drawr(app,canvas)
            if app.pearsonPre== True:
                findPearson(app,canvas)
            if app.drawSpecificweekPrice == True:
                canvas.create_text((app.click[0])/2,(app.click[1])/2*0.9,text=f'{app.weekprice}'\
                            ,fill='yellow',font="Helvetica 10 bold underline")
            
            if app.showA== True:
                averages(app,canvas)
        else:
            drawk(app,canvas)
            drawBollingLine(app,canvas)
            if app.predict==True:
                showBoard(app,canvas)
                drawPredictionArea(app,canvas)
                drawregression(app,canvas) 
                drawr(app,canvas)
        


    runApp(width=800, height=1000)
