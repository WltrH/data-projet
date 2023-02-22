import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import api as api
import datetime
import warnings
warnings.filterwarnings('ignore')



#api.refresh('eur', 'bitcoin', 'ethereum', '01/01/2021', '01/02/2021')
'''api.top10('eur')
api.top5('eur')
api.allcoin('eur')
api.history('bitcoin', 'eur')
api.marketcap('bitcoin', 'eur', '01/01/2020', '01/01/2021')
api.history2('bitcoin', 'ethereum', 'eur', '01/01/2020', '01/01/2021')'''


#################### SIDEBAR ####################
# variable de date du jour
date_jour = datetime.date.today()
date_jour_ = date_jour - datetime.timedelta(days=30)

# mise en place d'une sidebar
st.sidebar.title("Crypto-Monnaies Data")
# placement d'une liste déroulante pour choisir la currency en passant par la fonction api.currencies
currency = st.sidebar.selectbox('Choisir la monnaie/fiat', ('eur','dollar'))

# placement d'une liste pour choisir l'id de la crypto monnaie
id1 = st.sidebar.selectbox('Choisir l\'id de la crypto monnaie', api.currencies())

# placement d'une case pour choisir le second id de la crypto monnaie
id2 = st.sidebar.selectbox('Choisir le second id de la crypto monnaie', api.currencies())

# placement d'une case pour choisir la date de début, avec date du jour par défaut
start_date = st.sidebar.date_input('Choisir la date de début', value=date_jour_)

# placement d'une case pour choisir la date de fin
end_date = st.sidebar.date_input('Choisir la date de fin', value=date_jour)

if st.sidebar.button('Mettre à jour les données'):
    # mise à jour des données
    api.refresh2(currency, id1, id2, start_date, end_date)
    # affichage d'un message de confirmation
    st.sidebar.success('Données mises à jour')

# placement d'un séparateur
st.sidebar.markdown('---')
# placement d'un sous titre au millieu de la sidebar
st.sidebar.subheader("Powered by :")
# insertion d'une image dans la sidebar
st.sidebar.image('img/logo.png', width=200)

# lancement de l'application web

#################### PAGE 1 ####################

# création du titre
st.title("Crypto-Monnaies Data")

# création du sous-titre
st.subheader("Top 10 des crypto-monnaies")

# création d'un tableau des 10 premières crypto monnaies, en partant du fichier json Top10
# avec les colonnes suivantes : nom, prix, volume, capitalisation, %1h, %24h, %7j
df = pd.read_json('json/top10.json')
df = df[['name', 'current_price', 'total_volume', 'market_cap', 'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency']]

# mise en forme des données en % pour les colonnes price_change_percentage_1h_in_currency, price_change_percentage_24h_in_currency, price_change_percentage_7d_in_currency
df['price_change_percentage_1h_in_currency'] = df['price_change_percentage_1h_in_currency'].apply(lambda x: str(round(x, 2)) + '%')
df['price_change_percentage_24h_in_currency'] = df['price_change_percentage_24h_in_currency'].apply(lambda x: str(round(x, 2)) + '%')
df['price_change_percentage_7d_in_currency'] = df['price_change_percentage_7d_in_currency'].apply(lambda x: str(round(x, 2)) + '%')

#mise en forme des données en € pour les colonnes current_price, total_volume, market_cap
df['current_price'] = df['current_price'].apply(lambda x: str(round(x, 6)) + ' €')
df['total_volume'] = df['total_volume'].apply(lambda x: str(round(x, 2)) + ' €')
df['market_cap'] = df['market_cap'].apply(lambda x: str(round(x, 2)) + ' €')
# renommage des colonnes
df = df.rename(columns={'name': 'Nom', 'current_price': 'Prix', 'total_volume': 'Volume', 'market_cap': 'Capitalisation', 'price_change_percentage_1h_in_currency': '%1h', 'price_change_percentage_24h_in_currency': '%24h', 'price_change_percentage_7d_in_currency': '%7j'})
st.table(df)

# separation des graphiques
st.markdown('---')

# titre du graphique
st.subheader("Capitalisation des 10 premières crypto-monnaies")

# graphique des capitalisations des 10 premières crypto monnaies
df = pd.read_json('json/top10.json')
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(df['name'], df['market_cap'])
ax1.set_xlabel('Nom')
ax1.set_ylabel('Capitalisation')
ax1.set_title('Capitalisation des 10 premières crypto monnaies')
plt.legend()
st.pyplot(fig1)

# intégration d'un séparateur
st.markdown('---')

# titre du graphique
st.subheader("Volume des 10 premières crypto monnaies")

# graphique des volumes des 10 premières crypto monnaies
df = pd.read_json('json/top10.json')
fig, ax = plt.subplots(figsize=(10, 5))
#ax = sns.pairplot(df, x_vars='name', y_vars='total_volume', height=5, aspect=2)
ax.bar(df['name'], df['total_volume'])
ax.set_xlabel('Nom')
ax.set_ylabel('Volume')
ax.set_title('Volume des 10 premières crypto monnaies')
plt.legend()
st.pyplot(fig)



st.markdown('---')


# création d'un graphique sur l'historique d'une crypto monnaie
st.subheader("Historique d'une crypto monnaie")
#df = pd.read_json('json/histo.json')

st.markdown('---')




