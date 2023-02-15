import requests #importation de la librairie requests   
import json #importation de la librairie json
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

#connexion à l'API de CoinGecko pour récupération du ping
def ping():
    try:
        r = requests.get('https://api.coingecko.com/api/v3/ping')
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

#print le retour de la fonction ping()
print(ping())

#récupération dans une liste des 10 premiers crypto-monnaies en USD
def top10():
    top10 = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top10.json', 'w') as f:
        json.dump(top10, f)
    return top10


'''#fonction Top10 avec le paramètre de la currency
def top10(currency):
    top10 = cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/top10.json', 'w') as f:
        json.dump(top10, f)
    return top10'''

#fonction de récupération de l'intégralité des crypto-monnaies
def all():
    all = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=100, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/all.json', 'w') as f:
        json.dump(all, f)
    return all


'''#fonction de récupération de l'intégralité des crypto-monnaies en choisissant la currency
def all(currency):
    all = cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=100, page=1, sparkline=False, price_change_percentage='1h,24h,7d')
    #mise des information dans un fichier json dans le dossier json du projet
    with open('json/all.json', 'w') as f:
        json.dump(all, f)
    return all'''



'''#fonction pour rafraichir les données 5 fois par minutes
def refresh():
    for i in range(5):
        top10()
        all()
        time.sleep(12)'''


#test des fonctions
print (top10())
print (all())