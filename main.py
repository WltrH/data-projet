import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
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

#liste des crypto monnaies bitcoin, ethereum, tether, ripple

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=1095)

# mettre les données dans un dataframe en connectant directement à l'API
#btc = pd.Dataframe(cg.get_coin_market_chart_range_by_id(id=id1, vs_currency=currency, from_timestamp=start_date, to_timestamp=end_date))
# placement d'une liste déroulante pour choisir la currency en passant par la fonction api.currencies
currency = 'usd'

# placement d'une liste pour choisir l'id de la crypto monnaie
id1 = 'bitcoin'

# placement d'une case pour choisir le second id de la crypto monnaie, mise à eth en default
id2 =  'ethereum'

end_date_aff = end_date.strftime("%Y-%m-%d")
start_date_aff = start_date.strftime("%Y-%m-%d")

start_date = int(time.mktime(datetime.datetime.strptime(str(start_date), "%Y-%m-%d").timetuple()))
end_date = int(time.mktime(datetime.datetime.strptime(str(end_date), "%Y-%m-%d").timetuple()))


# récupération des crypto monnaies
bitcoin = api.get_btc(start_date, end_date)
ethereum = api.get_eth(start_date, end_date)

st.write(start_date, end_date)
st.write(start_date_aff, end_date_aff)


################################# Données du BTC ########################################
with st.container():

    st.write('DataFrame bictoin')
    # transformation des dates en timestamp


   #bitcoin = api.get_btc(start_date, end_date)
    #st.table(bitcoin)
    btc = pd.DataFrame(bitcoin)
    # mise en forme du dataframe pour faire une colonne date
    btc[['date', 'price']] = btc['prices'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('price_')
    btc[['date', 'market_cap']] = btc['market_caps'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('market_cap_')
    btc[['date', 'total_volume']] = btc['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('total_volume_')

    # mise en format de la date
    btc['date'] = btc['date'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S'))

    # enlever les heures et les minutes de la date
    btc['date'] = btc['date'].apply(lambda x: x.split(' ')[0])

    
    # garder uniquement les colonnes qui nous intéressent
    btc = btc[['date', 'price', 'market_cap', 'total_volume']]

    #changement des noms des colonnes
    btc = btc.rename(columns={'date': 'Date', 'price': 'Prix', 'market_cap': 'Capitalisation', 'total_volume': 'Volume total'})

    #mise en forme des données avec le symbol de la currency
    btc['Prix'] = btc['Prix'].apply(lambda x: str(round(x, 2)) + ' $')
    btc['Capitalisation'] = btc['Capitalisation'].apply(lambda x: str(round(x, 2)) + ' $')
    btc['Volume total'] = btc['Volume total'].apply(lambda x: str(round(x, 2)) + ' $')

    st.write(btc)



################################# Données de ETH ########################################
with st.container():

    st.write('DataFrame ethereum')
    
    #eth = api.get_eth(start_date, end_date)
    eth = pd.DataFrame(ethereum)

    # mise en forme du dataframe pour faire une colonne date
    eth[['date', 'price']] = eth['prices'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('price_')
    eth[['date', 'market_cap']] = eth['market_caps'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('market_cap_')
    eth[['date', 'total_volume']] = eth['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('total_volume_')

    # mise en format de la date
    eth['date'] = eth['date'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000).strftime('%Y-%m-%d %H:%M:%S'))

    # enlever les heures et les minutes de la date
    eth['date'] = eth['date'].apply(lambda x: x.split(' ')[0])

    # garder uniquement les colonnes qui nous intéressent
    eth = eth[['date', 'price', 'market_cap', 'total_volume']]

    #changement des noms des colonnes
    eth = eth.rename(columns={'date': 'Date', 'price': 'Prix', 'market_cap': 'Capitalisation', 'total_volume': 'Volume total'})

    #mise en forme des données avec le symbol de la currency
    eth['Prix'] = eth['Prix'].apply(lambda x: str(round(x, 2)) + ' $')
    eth['Capitalisation'] = eth['Capitalisation'].apply(lambda x: str(round(x, 2)) + ' $')
    eth['Volume total'] = eth['Volume total'].apply(lambda x: str(round(x, 2)) + ' $')


    st.write(eth)


################### Données du TOP 10 ####################

with st.container():
    st.write('TOP10 des Crypto monnaies par capitalisation')
    # récuéprer les données dans un dataframe le top10 du marché
    #top10 = pd.DataFrame(cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d'))
    top10 = api.get_top10(currency)
    top10 = pd.DataFrame(top10)
    #mise en forme du dataframe top10 pour ne récupérer que les colonnes qui nous intéressent
    top10 = top10[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
    # renommer les colonnes
    top10 = top10.rename(columns={'id': 'Nom', 'current_price': 'Prix', 'market_cap': 'Capitalisation', 'fully_diluted_valuation': 'Valeur totale', 'total_volume': 'Volume total', 'high_24h': 'Haut 24h', 'low_24h': 'Bas 24h', 'price_change_24h': 'Variation 24h', 'price_change_percentage_24h': 'Variation % 24h', 'market_cap_change_24h': 'Variation capitalisation 24h', 'market_cap_change_percentage_24h': 'Variation capitalisation % 24h', 'circulating_supply': 'Circulation', 'total_supply': 'Total'})
    # mettre en forme les données en avec le symbol de la currency
    top10['Prix'] = top10['Prix'].apply(lambda x: str(round(x, 6)) + ' $')
    top10['Capitalisation'] = top10['Capitalisation'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Valeur totale'] = top10['Valeur totale'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Volume total'] = top10['Volume total'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Haut 24h'] = top10['Haut 24h'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Bas 24h'] = top10['Bas 24h'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Variation 24h'] = top10['Variation 24h'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Variation capitalisation 24h'] = top10['Variation capitalisation 24h'].apply(lambda x: str(round(x, 2)) + ' $')


    # mettre en forme les données en pourcentage
    top10['Variation % 24h'] = top10['Variation % 24h'].map('{:,.2f}%'.format)
    top10['Variation capitalisation % 24h'] = top10['Variation capitalisation % 24h'].map('{:,.2f}%'.format)


    st.write(top10)

with st.container():
    # Titre
    st.subheader("Graphique sur le TOP 10 au dessus")

    # récuéprer les données dans un dataframe le top10 du marché
    top10 = api.get_top10(currency)
    top10 = pd.DataFrame(top10)
    #mise en forme du dataframe top10 pour ne récupérer que les colonnes qui nous intéressent
    top10 = top10[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
    # renommer les colonnes
    top10 = top10.rename(columns={'id': 'Nom', 'current_price': 'Prix', 'market_cap': 'Capitalisation', 'fully_diluted_valuation': 'Valeur totale', 'total_volume': 'Volume total', 'high_24h': 'Haut 24h', 'low_24h': 'Bas 24h', 'price_change_24h': 'Variation 24h', 'price_change_percentage_24h': 'Variation % 24h', 'market_cap_change_24h': 'Variation capitalisation 24h', 'market_cap_change_percentage_24h': 'Variation capitalisation % 24h', 'circulating_supply': 'Circulation', 'total_supply': 'Total'})

    st.subheader("Histogramme de la Capitalisation des 10 premières crypto-monnaies")
    # graphique en barre des capitalisations des 10 premières crypto monnaies
    fig = px.bar(top10, x='Nom', y='Capitalisation', color='Capitalisation', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

    st.subheader("Camembert du Volume des 10 premières crypto-monnaies")
    # graphique en camembert des volumes des 10 premières crypto monnaies
    fig = px.pie(top10, values='Volume total', names='Nom')
    st.plotly_chart(fig)

    st.markdown('---')

with st.container():
    # mise de start_date et end_date au format date sans l'heure
    #start_date = datetime.strptime(start_date, '%Y-%m-%d')
    #end_date = datetime.strptime(end_date, '%Y-%m-%d')
    # Titre
    st.subheader("Historique des prix du" + ' ' + id1 + ' ' + "en" + ' ' + currency + ' ' + "du" + ' ' + start_date_aff + ' ' + "au" + ' ' + end_date_aff)

    # récupération des données dans un dataframe
    btc = pd.DataFrame(bitcoin)

    # mise en forme du dataframe pour faire une colonne date
    btc[['date', 'price']] = btc['prices'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('price_')
    btc[['date', 'market_cap']] = btc['market_caps'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('market_cap_')
    btc[['date', 'total_volume']] = btc['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('total_volume_')

    # suppréssion des colonnes prices, market_caps et total_volumes
    btc = btc.drop(['prices', 'market_caps', 'total_volumes'], axis=1)

    #mise au format date sans mes minutes et secondes
    btc['date'] = pd.to_datetime(btc['date'], unit='ms')
    btc['date'] = btc['date'].dt.strftime('%Y-%m-%d')

    st.write(btc)

    # graphique en ligne du prix du bitcoin en fonction de la date
    fig = px.line(btc, x='date', y='price', title='Prix du Bitcoin en fonction de la date')
    fig.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig)

    st.markdown('---')
    st.subheader('Moyenne des prix du Bitcoin')
    st.write(btc)

    # prendre que la plus petite année
    start_date1 = start_date_aff[0:4]
    end_date1 = end_date_aff[0:4]

    st.write(start_date1, end_date1)

    # création d'un dataframe avec la date, la moyenne, l'écart type, le min et le max des prix du bitcoin
    btc1 = btc.loc[start_date1:end_date1,'price'].resample('W').agg(['mean', 'std', 'min', 'max'])
    st.write(btc1)

    #btc1 = btc.loc[start_date1:end_date1,'price'].resample('W').agg(['mean', 'std', 'min', 'max'])
    #st.write(btc1)

    # calcul de la moyenne des prix du bitcoin en fonction de la date
    #btc1 = btc.loc[start_date:end_date,'price'].resample('W').agg(['mean', 'std', 'min', 'max'])

    # mise de la date en index
    #btc1.reset_index('date')
    #btc1['date'] = btc1['date'].dt.strftime('%Y-%m-%d')

    #st.write(btc1)

    #figure de la moyenne, min et max des prix du bitcoin en fonction de la date
    #fig = px.line(btc1, x='date', y=(['mean', 'min', 'max']), title='Time Series with Rangeslider')
    #fig.update_xaxes(rangeslider_visible=True)
    #st.plotly_chart(fig)

    

    

    st.markdown('---')
################### HISTO ####################
# test des graphiques
st.subheader("Historique des prix du" + ' ' + id1 + ' ' + "en" + ' ' + currency)
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
df['price'] = df['price'].apply(lambda x: x + ' $')
df['market_cap'] = df['market_cap'].apply(lambda x: x + ' $')
df['total_volume'] = df['total_volume'].apply(lambda x: x + ' $')

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

########################################################################################
#mise de la date en index
st.write('LA ICI COUCOU')
df.set_index('date', inplace=True)
# mise du titre à cette place pour ne pas avoir les heures dans le titre
#titre du graphique
st.subheader("Prix du Bitcoin" + ' ' + str(df.index[0]) + ' ' + 'au' + ' ' + str(df.index[-1]))
# mise du dtype de l'index en datetime
df.index = pd.to_datetime(df.index)

st.write(df)
########################################################################################

#affichage du graphique des prix du bitcoin
fig = px.line(df, x=df.index, y='price',color_discrete_sequence=['#fe4a49'])
st.plotly_chart(fig)

########################################################################################
#mise de la date en index
#df.set_index('date', inplace=True)
# misedu titre du graphique
st.subheader("Prix du Bitcoin" + ' ' + str(df.index[0]) + ' ' + 'au' + ' ' + str(df.index[-1]))
# mise du dtype de l'index en datetime
#df.index = pd.to_datetime(df.index)

########################################################################################

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



#titre
st.title('Evolution du prix du bitcoin en 2020')

df1 = df.loc['2020','price'].resample('W').agg(['mean', 'std', 'min', 'max'])


#enlever l'index de la colonne date

st.write('ICI')
df1.reset_index(inplace=True)
df1['date'] = df1['date'].dt.strftime('%Y-%m-%d')

st.table(df1.iloc[0:10])

fig = px.line(df1, x='date', y=(['mean', 'min', 'max']), title='Time Series with Rangeslider')

fig.update_xaxes(rangeslider_visible=True)

st.plotly_chart(fig)


#titre du graphique
st.subheader("Capitalisation du marché")
