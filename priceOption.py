import alphaquery as aq
import yahoofinance as yf
import interestr as rate
import MarketWatch_options as mo
import re
import datetime
import math

# 390 minutes in a day, calculating every t mins
# company: a string of company name (e.g. AAPL, TSLA)
# K = float, strike price
# category = call/put/...
# N = maturity = number of date till maturity*390/t
# 
def priceOption(company, K, category, t, N, currPrice, currBid, currAsk):
    sigma = aq.findSigma(company)
    sigmat = sigma/((390/t)**2)
    # Instead of arbitrarily selecting the up (u) and down (d) jumps in the binomial, 
    # we can "match them to a volatility input assumption, σ. 
    # The correct values are given by u = exp[σ*sqrt(Δt)] and d = 1/u;
    u = (math.e)**sigmat
    d = 1/u
    period = 98670*2/t
    r = (1+rate.twoyrrate()/100)**(1/period)-1
    p = 1+r-d/(u-d)
    q = (u-(1+r))/(u-d)
    S0 = yf.findPrice(company)

    dom = [i for i in range(N+1)]
    dom[0] = set( [S0] )
    for n in range(N):
        try:
            if len(dom[n]) > 1e9: raise Exception('Out of memory')
        except:
            break # change the frequency of estimation?
        dom[n+1] = set( d*s for s in dom[n])
        dom[n+1].update( u*s for s in dom[n])
    f = [i for i in range(N+1)]

    if category == "put": # American put
        # Compute price. f[n](s, m) gives the price at time n when stock price is s and running max is m
        f[N] = { s:max(0, K-s) for s in dom[N] } # Option expires worthless
        def Rn(n, s):
            # Rollback operator
            En = max((f[n+1][u*s]*p + f[n+1][d*s]*q)/(1+r), max(0, K-s))
            return En
        for n in range(N-1, -1, -1):
            f[n] = { s:  Rn(n, s) for s in dom[n] }
        price = f[0]

    elif category == "call": # American call
        # Compute price. f[n](s, m) gives the price at time n when stock price is s and running max is m
        f[N] = { s:max(0, s-K) for s in dom[N] } # Option expires worthless
        def Rn(n, s):
            # Rollback operator
            En = max((f[n+1][u*s]*p + f[n+1][d*s]*q)/(1+r), max(0, s-K))
            return En
        for n in range(N-1, -1, -1):
            f[n] = { s:  Rn(n, s) for s in dom[n] }
        price = f[0]
    return f[0]


#option_index = 0 => option expires on 2/11
#option_index = 1 => option expires on 2/18
#option_index = 2 => option expires on 2/25

#row => the row index of option in the table 
def priceOption_wrapper(option_index, row, company, category, t):
    print(option_index, row, company, category, t)
    i = option_index
    today = datetime.datetime.now()
    today_date = today.year * 10000 + today.month * 100 + today.day
    maturity = 0
    if (i == 0):
        maturity = 20220211 - today_date
    elif (i == 1):
        maturity = 20220218 - today_date
    else:
        maturity = 20220225 - today_date
    option = mo.marketwatch_options(company.lower())[i]
    strike = 0.0
    strike_str = option['Strike'][row]
    if ',' in strike_str:
        strike = 1000 + float(re.findall("\d+\.\d+", strike_str)[0])
    else:
        strike = float(re.findall("\d+\.\d+", strike_str)[0])
    # strike = float(re.findall("\d+\.\d+", option['Strike'][row])[0])
    if category == 'call':
        currPrice = float(option['Call_Price'][row])
        currBid = float(option['Call_Bid'][row])
        currAsk = float(option['Call_Ask'][row])
    else:
        currPrice = float(option['Put_Price'][row])
        currBid = float(option['Put_Bid'][row])
        currAsk = float(option['Put_Ask'][row])
    price = priceOption(company, strike, category, t, maturity, currPrice, currBid, currAsk)
    return price    