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




'''#ping de l'API CoinGecko
bping =cg.ping()
print(bping)

#récupérer le btc vs usd
btc = cg.get_price(ids='bitcoin', vs_currencies='usd')
print(btc)
'''
#print le retour de la fonction ping()
print(ping())
