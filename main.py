import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import api as api
import datetime
import warnings
warnings.filterwarnings('ignore')

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from streamlit_extras import dataframe_explorer
from streamlit_extras.chart_container import chart_container



####################Setting######################
page_title = "Crypto-Monnaies Data"
page_icon = ":bar_chart:"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

################### SIDEBAR ####################
# variable de date du jour
date_jour = datetime.date.today()
date_jour_ = date_jour - datetime.timedelta(days=30)

#liste des crypto monnaies bitcoin, ethereum, tether, ripple

currencies = []
currencies = [('bitcoin', 'ethereum', 'tether', 'ripple')]

# placement d'une liste déroulante pour choisir la currency en passant par la fonction api.currencies
currency = st.sidebar.selectbox('Choisir la monnaie/fiat', ('eur','dollar'))

# placement d'une liste pour choisir l'id de la crypto monnaie
id1 = st.sidebar.selectbox('Choisir l\'id de la crypto monnaie', ('bitcoin', 'ethereum', 'tether', 'ripple'))

# placement d'une case pour choisir le second id de la crypto monnaie, mise à eth en default
id2 = st.sidebar.selectbox('Choisir l\'id de la crypto monnaie', ('bitcoin', 'ethereum', 'tether', 'ripple'), index=1)

# placement d'une case pour choisir la date de début, avec date du jour par défaut
start_date = st.sidebar.date_input('Choisir la date de début', value=date_jour_)

# placement d'une case pour choisir la date de fin
end_date = st.sidebar.date_input('Choisir la date de fin', value=date_jour)

# si les dates start_date et end_date ont un différenciel de plus de 30 jours alors on ajuste les dates
if (end_date - start_date).days > 30:
    # on ajuste la date de début à la date de fin - 30 jours
    start_date = end_date - datetime.timedelta(days=30)

if st.sidebar.button('Mettre à jour les données'):
    # mise à jour des données
    #api.refresh2(currency, id1, id2, start_date, end_date)
    api.top10(currency)
    api.allcoin(currency)
    #api.history(id1, currency, start_date, end_date)
    ##api.marketcap(id1, currency, start_date, end_date)
    api.history2(id1, id2, currency, start_date, end_date)
    ## affichage d'un message de confirmation
    st.sidebar.success('Données mises à jour')

# placement d'un séparateur
st.sidebar.markdown('---')
# placement d'un sous titre au millieu de la sidebar
st.sidebar.subheader("Powered by :")
# insertion d'une image dans la sidebar
st.sidebar.image('img/logo.png', width=200)


################### MAIN ####################


################### TOP 10 ####################
st.subheader("Top 10 des crypto-monnaies")

# création d'un tableau des 10 premières crypto monnaies, en partant du fichier json Top10
# avec les colonnes suivantes : nom, prix, volume, capitalisation, %1h, %24h, %7j
df = pd.read_json('json/top10.json')
df = df[['name', 'current_price', 'total_volume', 'market_cap', 'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency']]

# renommer les colonnes
#df = df.rename(columns={'name': 'Nom', 'current_price': 'Prix', 'total_volume': 'Volume', 'market_cap': 'Capitalisation', 'price_change_percentage_1h_in_currency': '%1h', 'price_change_percentage_24h_in_currency': '%24h', 'price_change_percentage_7d_in_currency': '%7j'})

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
# graphique en barre des capitalisations des 10 premières crypto monnaies
fig = px.bar(df, x='name', y='market_cap')
st.plotly_chart(fig)

# intégration d'un séparateur
st.markdown('---')

# titre du graphique
st.subheader("Volume des 10 premières crypto monnaies")

# graphique des volumes des 10 premières crypto monnaies
fig = px.pie(df, values='total_volume', names='name')
st.plotly_chart(fig)

st.markdown('---')
################### HISTO ####################
# test des graphiques
st.subheader("Historique des prix")
# exploration des dataframes avec streamlit_extras
#récupération des données dans un dataframe
df = pd.read_json('json/histo-bitcoin-eur.json')

#création d'un dataframe avec les données de la colonne prices, market_caps et total_volumes avec séparation de la date
df[['date', 'price']] = df['prices'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('price_')
df[['date', 'market_cap']] = df['market_caps'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('market_cap_')
df[['date', 'total_volume']] = df['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('total_volume_')

#suppression des colonnes inutiles
df.drop(['prices', 'market_caps', 'total_volumes'], axis=1, inplace=True)

#mise aua format datetime de la colonne date
df['date'] = pd.to_datetime(df['date'], unit='ms')

#retirer les heures de la date
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

#mise de la date en index
#df.set_index('date', inplace=True)


#mise au format monnaie de la colonne price
df['price'] = df['price'].apply(lambda x: '{:,.2f}'.format(x))
#mise au format monnaie de la colonne market_cap
df['market_cap'] = df['market_cap'].apply(lambda x: '{:,.2f}'.format(x))
#mise au format monnaie de la colonne total_volume
df['total_volume'] = df['total_volume'].apply(lambda x: '{:,.2f}'.format(x))

# mise du dataframe au format euro
df['price'] = df['price'].apply(lambda x: x + ' €')
df['market_cap'] = df['market_cap'].apply(lambda x: x + ' €')
df['total_volume'] = df['total_volume'].apply(lambda x: x + ' €')

st.table(df.iloc[0:10])
# separation des graphiques
st.markdown('---')

df = pd.read_json('json/histo-bitcoin-eur.json')

#création d'un dataframe avec les données de la colonne prices, market_caps et total_volumes avec séparation de la date
df[['date', 'price']] = df['prices'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('price_')
df[['date', 'market_cap']] = df['market_caps'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('market_cap_')
df[['date', 'total_volume']] = df['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('total_volume_')

#suppression des colonnes inutiles
df.drop(['prices', 'market_caps', 'total_volumes'], axis=1, inplace=True)

#mise aua format datetime de la colonne date
df['date'] = pd.to_datetime(df['date'], unit='ms')

#retirer les heures de la date
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

#mise de la date en index
df.set_index('date', inplace=True)

# mettre le dtype de l'index en datetime
df.index = pd.to_datetime(df.index)

fig = px.line(df, x=df.index, y='price',color_discrete_sequence=['#f4d03f'])
st.plotly_chart(fig)

# slider pour choisir la période
st.slider('Période', 1, 10, 5)
#affichage du graphique en relation avec le slider
fig = px.line(df, x=df.index, y='price',color_discrete_sequence=['#f4d03f'])
st.plotly_chart(fig)

plt.figure(figsize=(15, 5))
fig, ax = plt.subplots(figsize=(15, 5))
ax = df.loc['2020','price'].plot(label='prix 2020')
ax = df.loc['2020','price'].resample('M').mean().plot(label='prix moyen par mois 2020', ls='--', lw=3, alpha=0.5)
ax = df.loc['2020','price'].resample('W').mean().plot(label='prix moyen par semaine 2020', ls=':', lw=3, alpha=0.5)
st.pyplot(fig)

st.markdown('---')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['2020'], y=df['price'], name='prix 2020', line=dict(color='#f4d03f', width=2)))
fig.add_trace(go.Scatter(x=df['2020'], y=df['price'].resample('M').mean(), name='prix moyen par mois 2020', line=dict(color='royalblue', width=2)))
fig.add_trace(go.Scatter(x=df['2020'], y=df['price'].resample('W').mean(), name='prix moyen par semaine 2020', line=dict(color='green', width=2)))

#edition de la figure
fig.update_layout(title = 'Evolution du prix du bitcoin en 2020',
                    xaxis_title = 'Date',
                    yaxis_title = 'Prix')
st.plotly_chart(fig)
#separation des graphiques
st.markdown('---')

#titre du graphique
st.subheader("Capitalisation du marché")

