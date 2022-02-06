from bs4 import BeautifulSoup
import requests

def twoyrrate():
    url = 'https://www.annuity.org/annuities/rates/'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    L = []
    for num in soup.find_all('div', class_='c-rates-bar__rate'):
        L.append(num.text)
    strlen = len(L[0])
    return float(L[0][0:strlen-2])