import requests
from bs4 import BeautifulSoup

def findPrice(company):
    url = "https://finance.yahoo.com/quote/"+company
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    price = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
    return float(price)