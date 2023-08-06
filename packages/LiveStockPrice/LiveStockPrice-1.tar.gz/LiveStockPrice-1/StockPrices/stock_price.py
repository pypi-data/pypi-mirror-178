import bs4
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import html5lib
def stock_price(ticker):
    while True:
        try:
            url = 'https://finance.yahoo.com/quote/'+ ticker + "?p=" + ticker +"&.tsrc=fin-srch"
            page = requests.get(url)
            soup = bs4.BeautifulSoup(page.content,'html5lib')
            break
        except TypeError:
            print("Incorrect Symbol: Please Retry.")


    price1 = soup.find('fin-streamer',{'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'})
    current_price = list(price1)
    current_price = current_price[0]
    return current_price

