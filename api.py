import datetime
import requests #importation de la librairie requests   
import json #importation de la librairie json
import time #importation de la librairie time
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

'''#connexion à l'API de CoinGecko pour récupération du ping
def ping():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/ping')
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False'''


# fonction pour pinger l'API
def pinged():
    pinged =cg.ping()
    return pinged


#récupérer les 5 premières crypto-monnaies en USD
def top5usd():
    top5 = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=5, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top5.json', 'w') as f:
        json.dump(top5, f)
    return top5

#récupération dans une liste des 10 premiers crypto-monnaies en USD
def top10usd():
    top10 = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top10.json', 'w') as f:
        json.dump(top10, f)
    return top10


#fonction Top10 avec le paramètre de la currency
def top10cur(currency):
    top10 = cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top10.json', 'w') as f:
        json.dump(top10, f)
    return top10

#fonction de récupération de l'intégralité des crypto-monnaies
def allusd():
    all = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=100, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/all.json', 'w') as f:
        json.dump(all, f)
    return all


#fonction de récupération de l'intégralité des crypto-monnaies en choisissant la currency
def allcur(currency):
    all = cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=100, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/all.json', 'w') as f:
        json.dump(all, f)
    return all

#fonction de récupération de toutes l'historique d'une crypto-monnaie dans un fichier json avec la currency en paramètre
def historycur(currency, id):
    history = cg.get_coin_market_chart_by_id(id=id, vs_currency=currency, days=30)
    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-'+id+'.json', 'w') as f:
        json.dump(history, f)
    return history

#fonction de récupération de tout l'historique d'une crypto-monnaie
def historyall(id):
    history = cg.get_coin_market_chart_by_id(id=id, vs_currency='usd', days=1095)
    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-all-'+id+'.json', 'w') as f:
        json.dump(history, f)
    return history

#fonction pour rafraichir les données 5 fois par minutes
def refresh():
    for i in range(5):
        top10()
        all()
        time.sleep(12)

# fonction de récupérer l'historique d'une cryptomonnaie avec son id et la currency que l'on souhaite
def history(id, currency):
    history = cg.get_coin_market_chart_by_id(id=id, vs_currency=currency, days=30)
    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-'+id+'-'+currency+'.json', 'w') as f:
        json.dump(history, f)
    return history
###########################################################################
# restructuration du fichier api.py avec un choix de fonctions prédéfinies#
###########################################################################

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

# fonction pour récupérer l'historique d'une monnaie sur les 2 dernières années dans la currency choisie
def history(id, currency):
    history = cg.get_coin_market_chart_by_id(id=id, vs_currency=currency, days=730)
    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-'+id+'-'+currency+'.json', 'w') as f:
        json.dump(history, f)
    return history

# fonction pour récupérer le marketcap des 1O premières crypto-monnaies entre 2 dates dans la currency choisie
def marketcap(id, currency, date1, date2):
    # transformation des dates en timestamp
    date1 = int(time.mktime(datetime.datetime.strptime(date1, "%d/%m/%Y").timetuple()))
    date2 = int(time.mktime(datetime.datetime.strptime(date2, "%d/%m/%Y").timetuple()))


    marketcap = cg.get_coin_market_chart_range_by_id(id=id, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)
    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''marketcap-'+id+'-'+currency+'.json', 'w') as f:
       json.dump(marketcap, f)
    return marketcap

# fonction pour récupérer l'historique de deux crypto-monnaies entre 2 dates dans la currency choisie
def history2(id1, id2, currency, date1, date2):
    # transformation des dates en timestamp
    date1 = int(time.mktime(datetime.datetime.strptime(date1, "%d/%m/%Y").timetuple()))
    date2 = int(time.mktime(datetime.datetime.strptime(date2, "%d/%m/%Y").timetuple()))

    # récupération des données
    history1 = cg.get_coin_market_chart_range_by_id(id=id1, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)
    history2 = cg.get_coin_market_chart_range_by_id(id=id2, vs_currency=currency, from_timestamp=date1, to_timestamp=date2)


    #mise des information dans un fichier json du même nom que l'idi dans le dossier json du projet
    with open('json/''histo-'+id1+'-'+id2+'-'+currency+'.json', 'w') as f:
        json.dump(history1, f)
        json.dump(history2, f)
    return history1, history2

#test des fonctions
print (pinged())
#print (top10usd())
#print (top10cur('eur'))
#print (allusd())
#print (allcur('eur'))
#print(top5usd())
#print(historycur('eur', 'dogecoin'))
#historyall('bitcoin')
#allcoin('usd')
#history('bitcoin', 'eur')
#marketcap('bitcoin', 'eur', '01/01/2020', '01/01/2021')
history2('bitcoin', 'ethereum', 'eur', '01/01/2020', '01/01/2021')