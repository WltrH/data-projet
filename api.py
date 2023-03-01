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



###########################################################################
# restructuration du fichier api.py avec un choix de fonctions prédéfinies#
###########################################################################

# fonction pour récupérer la date du jour
def date_jour():
    date_jour = datetime.date.today()
    return date_jour



# fonction pour récupérer la liste de tous les coins
def allcoin(currency):
    all = cg.get_coins_list()
    with open('json/allcoin.json', 'w') as f:
        json.dump(all, f)
    return all

# fontion pour récupérer les 10 premières crypto-monnaies dans la currency choisie
def top10(currency):
    top10 = cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top10.json', 'w') as f:
        json.dump(top10, f)
    return top10

# fonction pour récupérer les 5 premières crypto-monnaies dans la currency choisie
def top5(currency):
    top5 = cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=5, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top5.json', 'w') as f:
        json.dump(top5, f)
    return top5

# fonction pour récupérer l'historique d'une monnaie entre deux dates dans la currency choisie
def history(id, currency, date1, date2):

    # transformation des dates en timestamp
    date1 = int(time.mktime(datetime.datetime.strptime(date1, "%Y/%m/%d").timetuple()))
    date2 = int(time.mktime(datetime.datetime.strptime(date2, "%Y/%m/%d").timetuple()))
    print(date1)
    print(date2)
    # récupération des données
    history = cg.get_coin_market_chart_range_by_id(id=id, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)

    # mise en forme des données de history
    history = history['prices']
    history = [list(i) for i in history]
    for i in history:
        i[0] = datetime.datetime.fromtimestamp(i[0]/1000).strftime('%Y-%m-%d %H:%M:%S')
    history = [tuple(i) for i in history]


    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-'+id+'-'+currency+'.json', 'w') as f:
        json.dump(history, f)
    return history

# fonction pour récupérer le marketcap des 1O premières crypto-monnaies entre 2 dates dans la currency choisie
def marketcap(id, currency, date1, date2):
    # transformation des dates en timestamp
    date1 = int(time.mktime(datetime.datetime.strptime(date1, "%Y/%m/%d").timetuple()))
    date2 = int(time.mktime(datetime.datetime.strptime(date2, "%Y/%m/%d").timetuple()))


    marketcap = cg.get_coin_market_chart_range_by_id(id=id, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)
    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''marketcap-'+id+'-'+currency+'.json', 'w') as f:
       json.dump(marketcap, f)
    return marketcap

# fonction pour récupérer l'historique de deux crypto-monnaies entre 2 dates dans la currency choisie
def history2(id1, id2, currency, date1, date2):

    # contrôle sur les dates
    if date1 > date2 or date1 == date2:
        date2  = date1 + 1

    # transformation des dates en timestamp
    date1 = int(time.mktime(datetime.datetime.strptime(date1, "%Y/%m/%d").timetuple()))
    date2 = int(time.mktime(datetime.datetime.strptime(date2, "%Y/%m/%d").timetuple()))

    # récupération des données
    history1 = cg.get_coin_market_chart_range_by_id(id=id1, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)
    history2 = cg.get_coin_market_chart_range_by_id(id=id2, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)

    # mise des données de history1 dans un fichier json
    with open('json/''histo-'+id1+'-'+currency+'.json', 'w') as f:
        json.dump(history1, f)
    
    with open('json/''histo-'+id2+'-'+currency+'.json', 'w') as f:
        json.dump(history2, f)

    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-'+id1+'-'+id2+'-'+currency+'.json', 'w') as f:
        json.dump(history1, f)
        json.dump(history2, f)
    return history1, history2

# fonction pour récupérer les fiats disponibles
def fiats():
    fiats = cg.get_supported_vs_currencies()
    return fiats



def currencies():
    currencies = cg.get_supported_vs_currencies()

    return currencies

#fonction pour rafraichir les données 5 fois par minutes
def refresh(currency, id1, id2, start_date, end_date):
    currency = currency
    id1 = id1
    id2 = id2
    start_date = start_date
    end_date = end_date

    for i in range(5):
        allcoin(currency)
        top10(currency)
        top5(currency)
        history(id1, currency)
        marketcap(id1, currency, start_date, end_date)
        history2(id1, id2, currency, start_date, end_date)
        time.sleep(12)
# fonction pour rafraichir les données
def refresh2(currency, id1, id2, start_date, end_date):
    currency = currency
    id1 = id1
    id2 = id2
    start_date = start_date
    end_date = end_date

    allcoin(currency)
    top10(currency)
    top5(currency)
    history(id1, currency)
    marketcap(id1, currency, start_date, end_date)
    history2(id1, id2, currency, start_date, end_date)

#test des fonctions
print (pinged())
#print (get_btc())
#print (top10usd())
#print (top10cur('eur'))
#print (allusd())
#print (allcur('eur'))
#print(top5usd())
#print(historycur('eur', 'dogecoin'))
#historyall('bitcoin')
#allcoin('usd')
#top10('eur')
#top5('eur')
#history('poly', 'eur', '2020/01/01', '2020/12/31')
#marketcap('bitcoin', 'eur', '01/01/2020', '01/01/2021')bitcoin, ethereum, ripple, tether, 
#history2('bitcoin', 'ethereum', 'eur', '01/01/2020', '01/01/2021')
#print(currencies())
