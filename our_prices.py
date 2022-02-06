from subprocess import call
import MarketWatch_options as mo
import priceOption as po
import pandas as pd
import re
import datetime

df = pd.DataFrame()
tinker = 'AAPL'
call1 = []
put1 = []
call2 = []
put2 = []
call3 = []
put3 = []


option1 = mo.marketwatch_options(tinker.lower())[0]
option2 = mo.marketwatch_options(tinker.lower())[1]
option3 = mo.marketwatch_options(tinker.lower())[2]

rows1 = option1.shape[0]
rows2 = option2.shape[0]
rows3 = option3.shape[0]


today = datetime.datetime.now()
today_date = today.year * 10000 + today.month * 100 + today.day
exp_date1 = 20220211
exp_date2 = 20220218
exp_date3 = 20220225
maturity1 = exp_date1 - today_date
maturity2 = exp_date2 - today_date
maturity3 = exp_date3 - today_date

ex = 0

#construct call1
for i in range (0, rows1):
    try:
        strike = float(re.findall("\d+\.\d+", option1['Strike'][i])[0])
        currPrice = float(option1['Call_Price'][i])
        currBid = float(option1['Call_Bid'][i])
        currAsk = float(option1['Call_Ask'][i])
        price = po.priceOption(tinker, strike, "call", 30, maturity1, currPrice, currBid, currAsk)
        call1.append([strike, price])
    except:
        ex = 1




#construct call2
for i in range (0, rows2):
    try:
        strike = float(re.findall("\d+\.\d+", option2['Strike'][i])[0])
        currPrice = float(option2['Call_Price'][i])
        currBid = float(option2['Call_Bid'][i])
        currAsk = float(option2['Call_Ask'][i])
        price = po.priceOption(tinker, strike, "call", 30, maturity2, currPrice, currBid, currAsk)
        call2.append([strike, price])
    except:
        ex = 1

#construct call3
for i in range (0, rows3):
    try:
        strike = float(re.findall("\d+\.\d+", option3['Strike'][i])[0])
        currPrice = float(option3['Call_Price'][i])
        currBid = float(option3['Call_Bid'][i])
        currAsk = float(option3['Call_Ask'][i])
        price = po.priceOption(tinker, strike, "call", 30, maturity3, currPrice, currBid, currAsk)
        call3.append([strike, price])
    except:
        call3.append(0)

# #construct put1
for i in range (0, rows1):
    try:
        strike = float(re.findall("\d+\.\d+", option1['Strike'][i])[0])
        currPrice = float(option1['Put_Price'][i])
        currBid = float(option1['Put_Bid'][i])
        currAsk = float(option1['Put_Ask'][i])
        price = po.priceOption(tinker, strike, "put", 30, maturity1, currPrice, currBid, currAsk)
        put1.append([strike, price])
    except:
        ex = 1

#construct put2
for i in range (0, rows2):
    try:
        strike = float(re.findall("\d+\.\d+", option2['Strike'][i])[0])
        currPrice = float(option2['Put_Price'][i])
        currBid = float(option2['Put_Bid'][i])
        currAsk = float(option2['Put_Ask'][i])
        price = po.priceOption(tinker, strike, "put", 30, maturity2, currPrice, currBid, currAsk)
        put2.append([strike, price])
    except:
        ex = 1


#construct put3
for i in range (0, rows3):
    try:
        strike = float(re.findall("\d+\.\d+", option3['Strike'][i])[0])
        currPrice = float(option3['Put_Price'][i])
        currBid = float(option3['Put_Bid'][i])
        currAsk = float(option3['Put_Ask'][i])
        price = po.priceOption(tinker, strike, "put", 30, maturity3, currPrice, currBid, currAsk)
        put2.append([strike, price])
    except:
        ex = 1