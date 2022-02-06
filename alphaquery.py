import requests
from bs4 import BeautifulSoup

def findSigma(company):
    url = "https://www.alphaquery.com/stock/"+company+"/volatility-option-statistics/30-day/iv-mean"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    sigma = soup.find('div', {'class': 'indicator-figure-inner'}).text
    return float(sigma)