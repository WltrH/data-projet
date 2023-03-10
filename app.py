import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import api as api
import warnings

from streamlit_extras import dataframe_explorer
from streamlit_extras.chart_container import chart_container

warnings.filterwarnings('ignore')


####################Setting######################
page_title = "Analyses Crypto-Monnaies"
page_icon = ":bar_chart:"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

#################################################
# presentation of the application
st.write('L\'application récupère les données en direct depuis une API de marché de crypto-monnaies et permet de sélectionner différentes options telles que la monnaie et les crypto-monnaies à afficher.L\'application affiche également les graphiques et les tableaux pertinents pour aider à visualiser et analyser les données de marché des crypto-monnaies. Enfin, elle permet d\'afficher le Top10 des crypto-monnaies en termes de capitalisation boursière et d\'afficher les données de chaque crypto-monnaie individuellement.')


currency = 'usd'

# Data retrieval through API functions
top10 = api.get_top10(currency)
exchange_simple = api.get_exchange_simple()

# transformation des données en dataframe
top10_brut = pd.DataFrame(top10)
exchange = pd.DataFrame(exchange_simple)


################### TOP 10 Data ####################

with st.container():
    st.subheader(' Dataset du top 10 des Crypto monnaies par capitalisation mis en forme')
    
    # formatting of the top10 dataframe to retrieve only the columns of interest
    top10 = top10_brut[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
    # rename the columns
    top10 = top10.rename(columns={'id': 'Nom', 'current_price': 'Prix', 'market_cap': 'Capitalisation', 'fully_diluted_valuation': 'Valeur totale', 'total_volume': 'Volume total', 'high_24h': 'Haut 24h', 'low_24h': 'Bas 24h', 'price_change_24h': 'Variation 24h', 'price_change_percentage_24h': 'Variation % 24h', 'market_cap_change_24h': 'Variation capitalisation 24h', 'market_cap_change_percentage_24h': 'Variation capitalisation % 24h', 'circulating_supply': 'Circulation', 'total_supply': 'Total'})
    # format the data with the currency symbol
    top10['Prix'] = top10['Prix'].apply(lambda x: str(round(x, 6)) + ' $')
    top10['Capitalisation'] = top10['Capitalisation'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Valeur totale'] = top10['Valeur totale'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Volume total'] = top10['Volume total'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Haut 24h'] = top10['Haut 24h'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Bas 24h'] = top10['Bas 24h'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Variation 24h'] = top10['Variation 24h'].apply(lambda x: str(round(x, 2)) + ' $')
    top10['Variation capitalisation 24h'] = top10['Variation capitalisation 24h'].apply(lambda x: str(round(x, 2)) + ' $')


    # format the data in percentages
    top10['Variation % 24h'] = top10['Variation % 24h'].map('{:,.2f}%'.format)
    top10['Variation capitalisation % 24h'] = top10['Variation capitalisation % 24h'].map('{:,.2f}%'.format)


    st.write(top10)

with st.container():
    # Tittle
    st.subheader("Analyses sur le top 10 des crypto-monnaies")

    # formatting of the top10 dataframe to retrieve only the columns of interest
    top10 = top10_brut[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
    # rename the columns
    top10 = top10.rename(columns={'id': 'Nom', 'current_price': 'Prix', 'market_cap': 'Capitalisation', 'fully_diluted_valuation': 'Valeur totale', 'total_volume': 'Volume total', 'high_24h': 'Haut 24h', 'low_24h': 'Bas 24h', 'price_change_24h': 'Variation 24h', 'price_change_percentage_24h': 'Variation % 24h', 'market_cap_change_24h': 'Variation capitalisation 24h', 'market_cap_change_percentage_24h': 'Variation capitalisation % 24h', 'circulating_supply': 'Circulation', 'total_supply': 'Total'})

    st.subheader("Histogramme de la Capitalisation des 10 premières crypto-monnaies")
    # bar chart of the capitalizations of the top 10 crypto currencies
    fig = px.bar(top10, x='Nom', y='Capitalisation', color='Capitalisation', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

    st.subheader("Camembert du Volume des 10 premières crypto-monnaies")
    # pie chart of the volumes of the top 10 crypto currencies
    fig = px.pie(top10, values='Volume total', names='Nom')
    st.plotly_chart(fig)

    st.markdown('---')


################################################ Crypto ###############################################
with st.container():

    # Tittle
    st.subheader("Volumes du Market Cap des 10 premières crypto-monnaies sur 24h")

    # data recovery in a dataframe
    df = pd.DataFrame(top10_brut)

    # dot plot on crypto currencies prices
    fig = px.scatter(df, x='current_price', y='market_cap', color='id', size='market_cap', hover_name='id', log_x=True, size_max=60)
    st.plotly_chart(fig)

    st.subheader("Histoganme des variations des 10 premières crypto-monnaies sur 24h")

    fig = px.bar(df, x='id', y='price_change_percentage_24h', color='price_change_percentage_24h', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

   
################### EXCHANGES ####################
with st.container():
    # Tittle
    st.subheader("Dataset des Exchanges mis en forme")

    # retrieve data from a dataframe
    # Formatting of the exchanges dataframe to retrieve only the columns of interest
    df = pd.DataFrame(exchange)
    df = df[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]


    # recovery of data in a dataframet
    df = pd.DataFrame(exchange)
    # Formatting of the exchanges dataframe to retrieve only the columns that interest us
    df = exchange[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]
    # dataframe formatting
    df = exchange.rename(columns={'id': 'ID', 'name': 'Nom', 'year_established': 'Année de création', 'country': 'Pays', 'trust_score': 'Score de confiance', 'trade_volume_24h_btc': 'Volume 24h', 'trade_volume_24h_btc_normalized': 'Volume 24h normalisé'})
    # data formatting
    df['Volume 24h'] = df['Volume 24h'].apply(lambda x: str(round(x, 2)) + ' BTC')
    df['Volume 24h normalisé'] = df['Volume 24h normalisé'].apply(lambda x: str(round(x, 2)) + ' BTC')
    
    st.write(df)


    st.markdown('---')

with st.container ():

    # creation of a new dataset regrouping the countries of the exchanges and their geographical position
    df = pd.DataFrame(df['Pays'].value_counts())
    df = df.reset_index()
    df = df.rename(columns={'index': 'Pays', 'Pays': 'Nombre d\'exchanges'})
    df = df.sort_values(by='Nombre d\'exchanges', ascending=False)
    df = df.head(100)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    df = df.rename(columns={'Pays': 'Country'})


    # new dataframe with worldcities.csv data
    df2 = pd.read_csv('worldcities.csv')

    # merge between df and df2 to recover only the city column if the country is the same
    df = pd.merge(df, df2, how='left', left_on='Country', right_on='country')
    # keep only the lines with capital = primary
    df = df[df['capital'] == 'primary']
    # we keep only the columns that interest us
    df = df[['Country', 'Nombre d\'exchanges', 'city', 'lat', 'lng']]
    # we rename the columns to match the streamlit map function
    df = df.rename(columns={'city': 'City', 'lat': 'latitude', 'lng': 'longitude'})
    #st.write(df)

    st.subheader("Localisation des exchanges dans le monde")
    # placement of points on the map
    st.map(df, zoom=1, use_container_width=True)

    st.markdown('---')

    st.subheader("Pourcentage des exchanges situé dans le monde par pays")

    # figure with the countries and the number of exchanges present
    fig = px.pie(df, values='Nombre d\'exchanges', names='Country')
    st.plotly_chart(fig)

st.markdown('---')

with st.container():
    # trade volume of exchanges on map
    st.subheader("Volume de trade des exchanges dans le monde")

    # data recovery in a dataframe
    df_data = pd.DataFrame(exchange)
    # Shaping of the exchanges dataframe to retrieve only the columns of interest
    df = df_data

    # creation of a new dataset to put trade volumes on a map by country
    df = pd.DataFrame(df['country'].value_counts())
    df = df.reset_index()
    df = df.rename(columns={'index': 'country', 'country': 'nombre_exchanges'})
    df = df.sort_values(by='nombre_exchanges', ascending=False)
    df = df.head(100)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    df = df.rename(columns={'country': 'Country'})

    # merge with the df2 dataframe to get the geographic coordinates of the exchanges
    df = pd.merge(df, df2, how='left', left_on='Country', right_on='country')
    # we keep only the exchanges with a capital = primary
    df = df[df['capital'] == 'primary']

    # addition of the trade volumes of the exchanges
    df = pd.merge(df, df_data, how='left', left_on='Country', right_on='country')

    # group trade volumes by country
    df = df.groupby(['Country', 'nombre_exchanges', 'city', 'lat', 'lng']).sum()
    df = df.reset_index()
    df = df.drop(columns=['year_established', 'trust_score'])
    df = df.rename(columns={'city': 'City', 'lat': 'latitude', 'lng': 'longitude'})
    df = df.sort_values(by='trade_volume_24h_btc', ascending=False)
    df = df.head(100)
    df = df.reset_index()
    df = df.drop(columns=['index'])


    # 3D map with trade volumes of exchanges by country
    fig = px.scatter_3d(df, x='longitude', y='latitude', z='trade_volume_24h_btc', color='Country', size='trade_volume_24h_btc', hover_name='Country', size_max=20, opacity=0.7)
    st.plotly_chart(fig)

    st.markdown('---')

    # garder dans le dataset que certaines données
    df = df[['Country', 'longitude', 'latitude', 'trade_volume_24h_btc']]

    # figure with bubble map on trade volumes of exchanges
    st.subheader("Volumes de trade des exchanges par pays dans le monde")
    fig = px.scatter_geo(df, locations="Country", locationmode='country names', color="Country", hover_name="Country", size="trade_volume_24h_btc", projection="natural earth")
    st.plotly_chart(fig)

    st.markdown('---')

    # pie chart on trade volumes of exchanges by country
    st.subheader("Volumes de trade des exchanges par pays")
    fig = px.pie(df, values='trade_volume_24h_btc', names='Country')
    st.plotly_chart(fig)

    st.markdown('---')


with st.container():
    # Tittle
    st.subheader("Volumes des trades des exchanges")

    df = pd.DataFrame(exchange)

    df = df.head(20)

    # is a pie chart of the trading volumes of the exchanges
    st.subheader("Pourcentage des volumes de trade des exchanges sur 24h en BTC")
    fig = px.pie(df, values='trade_volume_24h_btc', names='name')
    st.plotly_chart(fig)
    st.markdown ('---')

    # Scatter plot of trade volumes by trade
    st.subheader("Volumes de trade des exchanges en BTC sur 24h sans Binance")
    df = df[df['name'] != 'Binance']
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    st.markdown('---')

    # pairplot figure on trade volumes by exchange
    fig = px.scatter_matrix(df, dimensions=['name', 'trade_volume_24h_btc'], color='trade_volume_24h_btc')
    st.plotly_chart(fig)
    st.markdown('---')

    st.subheader(" Volumes de trade normalisés des exchanges sur 24h en BTC sans Binance")

    fig = px.scatter_3d(df, x='name', y='trade_volume_24h_btc_normalized', z='trade_volume_24h_btc', color='trade_volume_24h_btc', size='trade_volume_24h_btc', hover_name='name', size_max=20, opacity=0.7)
    st.plotly_chart(fig)
    st.markdown('---')

 
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc_normalized', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    st.markdown('---')

# CoinGecko
st.header("Powerded by :")
st.image('img/logo.png', use_column_width=True)


