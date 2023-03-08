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

from streamlit_extras import dataframe_explorer
from streamlit_extras.chart_container import chart_container

warnings.filterwarnings('ignore')


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


# Récupération des données en passant par les fonctions de l'API
bitcoin = api.get_btc(start_date, end_date)
ethereum = api.get_eth(start_date, end_date)
top10 = api.get_top10(currency)
exchange_bin = api.get_bin_exchange()
exchange_coin = api.get_bit_exchange()
exchange_simple = api.get_exchange_simple()


# transformation des données en dataframe
btc = pd.DataFrame(bitcoin)
eth = pd.DataFrame(ethereum)
top10 = pd.DataFrame(top10)
binance = pd.DataFrame(exchange_bin)
coinbase = pd.DataFrame(exchange_coin)
exchange = pd.DataFrame(exchange_simple)



################### Données du TOP 10 ####################

with st.container():
    st.write('TOP10 des Crypto monnaies par capitalisation')
    # récuéprer les données dans un dataframe le top10 du marché
    #top10 = pd.DataFrame(cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d'))

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
   
################### EXCHANGES ####################
with st.container():
# Titre sur l'exchange Binance
    st.subheader("Exchanges")

    #mise en forme du dataframe

    # récupération des données dans un dataframe
    #Mise en forme du dataframe des exchanges pour ne récupérer que les colonnes qui nous intéressent
    exchange = pd.DataFrame(exchange)
    exchange = exchange[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]

    st.write(exchange)
    # mise en place d'une map avec la localisation des exchanges
    st.subheader("Localisation des exchanges")
    # récupération des données dans un dataframe
    exchange = pd.DataFrame(exchange)
    #Mise en forme du dataframe des exchanges pour ne récupérer que les colonnes qui nous intéressent
    exchange = exchange[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]
    #mise en forme du dataframe
    exchange = exchange.rename(columns={'id': 'ID', 'name': 'Nom', 'year_established': 'Année de création', 'country': 'Pays', 'trust_score': 'Score de confiance', 'trade_volume_24h_btc': 'Volume 24h', 'trade_volume_24h_btc_normalized': 'Volume 24h normalisé'})
    #mise en forme des données
    exchange['Volume 24h'] = exchange['Volume 24h'].apply(lambda x: str(round(x, 2)) + ' BTC')
    exchange['Volume 24h normalisé'] = exchange['Volume 24h normalisé'].apply(lambda x: str(round(x, 2)) + ' BTC')
    #mise en forme des données en pourcentage
    exchange['Score de confiance'] = exchange['Score de confiance'].map('{:,.2f}%'.format)
    #mise en forme des données en pourcentage
    exchange['Année de création'] = exchange['Année de création'].map('{:,.0f}'.format)




  
    


    

    st.markdown('---')
################### HISTO ####################
# test des graphiques
st.subheader("Historique des prix du" + ' ' + id1 + ' ' + "en" + ' ' + currency)
# exploration des dataframes avec streamlit_extras
#récupération des données dans un dataframewx
# separation des graphiques
st.markdown('---')

df = pd.read_json('json/histo-bitcoin-eur.json')
st.header('BTC')
st.write(btc)
st.header('DF')
st.write(df)


#création d'un dataframe avec les données de la colonne prices, market_caps et total_volumes avec séparation de la date
df[['date', 'price']] = df['prices'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('price_')
df[['date', 'market_cap']] = df['market_caps'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('market_cap_')
df[['date', 'total_volume']] = df['total_volumes'].apply(lambda x: pd.Series([x[0], x[1]])).add_prefix('total_volume_')

#suppression des colonnes inutiles
df.drop(['prices', 'market_caps', 'total_volumes'], axis=1, inplace=True)

st.header('DF APRES TRAITEMENT')
st.write(df)

#mise aua format datetime de la colonne date
df['date'] = pd.to_datetime(df['date'], unit='ms')

#retirer les heures de la date
df['date'] = df['date'].dt.strftime('%Y-%m-%d')

st.header('DF APRES TRAITEMENT DE LA DATE')
st.write(df)

st.header('BTC APRES TRAITEMENT DE LA DATE en index')
#mise de la date en index
btc.set_index('date', inplace=True)
st.write(btc)

###############################ICI#########################################################
#mise de la date en index
st.write('LA ICI COUCOU')
df.set_index('date', inplace=True)
# mise du titre à cette place pour ne pas avoir les heures dans le titre
#titre du graphique
st.subheader("Prix du Bitcoin" + ' ' + str(df.index[0]) + ' ' + 'au' + ' ' + str(df.index[-1]))
# mise du dtype de l'index en datetime
df.index = pd.to_datetime(df.index)

st.header('DF APRES TRAITEMENT DE LA DATE TO DATETIME')

st.write(df)

st.header('BTC APRES TRAITEMENT DE LA DATE TO DATETIME')
btc.index = pd.to_datetime(btc.index)
st.write(btc)
########################################################################################
st.header('FIGURE AVEC DF')
#affichage du graphique des prix du bitcoin
fig = px.line(df, x=df.index, y='price',color_discrete_sequence=['#fe4a49'])
st.plotly_chart(fig)

st.header('FIGURE AVEC BTC')
#affichage du graphique des prix du bitcoin
fig = px.line(btc, x=btc.index, y='price',color_discrete_sequence=['#fe4a49'])
fig.update_xaxes(rangeslider_visible=True)
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
# checkbox pour afficher les années

# mise en place d'un slider pour choisir l'année venant de la colonne date du dataframe
year = st.slider('Choisir une année', min_value=df.index.year.min(), max_value=df.index.year.max(), value=df.index.year.min())

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
