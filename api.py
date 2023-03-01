import datetime
import requests #importation de la librairie requests   
import json #importation de la librairie json
import time #importation de la librairie time
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()


# fonction pour pinger l'API
def pinged():
    pinged =cg.ping()
    return pinged

# fonction pour appeler l'API pour faire un ping
def ping():
    ping = requests.get('https://api.coingecko.com/api/v3/ping')
    if ping.status_code == 200:
        ping = True
    else:
        ping = False
    return ping

def get_btc(date1, date2):
        
    btc = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from='+str(date1)+'&to='+str(date2))
    return btc.json()

def get_eth(date1, date2):
    eth = requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=eur&from='+str(date1)+'&to='+str(date2))
    return eth.json()

def get_top10(currency):
    top10 = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency='+currency+'&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d')
    return top10.json()

