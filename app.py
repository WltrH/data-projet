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
# présentation de l'application
st.write('L\'application récupère les données en direct depuis une API de marché de crypto-monnaies et permet de sélectionner différentes options telles que la monnaie et les crypto-monnaies à afficher.L\'application affiche également les graphiques et les tableaux pertinents pour aider à visualiser et analyser les données de marché des crypto-monnaies. Enfin, elle permet d\'afficher le Top10 des crypto-monnaies en termes de capitalisation boursière et d\'afficher les données de chaque crypto-monnaie individuellement.')


currency = 'usd'

# Récupération des données en passant par les fonctions de l'API
top10 = api.get_top10(currency)
exchange_simple = api.get_exchange_simple()

# transformation des données en dataframe
top10_brut = pd.DataFrame(top10)
exchange = pd.DataFrame(exchange_simple)


################### Données du TOP 10 ####################

with st.container():
    st.subheader(' Dataset du top 10 des Crypto monnaies par capitalisation mis en forme')
    
    #mise en forme du dataframe top10 pour ne récupérer que les colonnes qui nous intéressent
    top10 = top10_brut[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
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
    st.subheader("Analyses sur le top 10 des crypto-monnaies")

    #mise en forme du dataframe top10 pour ne récupérer que les colonnes qui nous intéressent
    top10 = top10_brut[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
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


################################################ Crypto ###############################################
with st.container():

    # titre figure sur les crypto monnaies
    st.subheader("Volumes du Market Cap des 10 premières crypto-monnaies sur 24h")

    # récupération des données dans un dataframe
    df = pd.DataFrame(top10_brut)

    # graphique nuage de point sur les prix des crypto monnaies
    fig = px.scatter(df, x='current_price', y='market_cap', color='id', size='market_cap', hover_name='id', log_x=True, size_max=60)
    st.plotly_chart(fig)

    st.subheader("Histoganme des variations des 10 premières crypto-monnaies sur 24h")

    fig = px.bar(df, x='id', y='price_change_percentage_24h', color='price_change_percentage_24h', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

   
################### EXCHANGES ####################
with st.container():
# Titre sur l'exchange Binance
    st.subheader("Dataset des Exchanges mis en forme")

    #mise en forme du dataframe
    # récupération des données dans un dataframe
    #Mise en forme du dataframe des exchanges pour ne récupérer que les colonnes qui nous intéressent
    df = pd.DataFrame(exchange)
    df = df[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]

   
    # mise en place d'une map avec la localisation des exchanges    
    # récupération des données dans un dataframe
    df = pd.DataFrame(exchange)
    #Mise en forme du dataframe des exchanges pour ne récupérer que les colonnes qui nous intéressent
    df = exchange[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]
    #mise en forme du dataframe
    df = exchange.rename(columns={'id': 'ID', 'name': 'Nom', 'year_established': 'Année de création', 'country': 'Pays', 'trust_score': 'Score de confiance', 'trade_volume_24h_btc': 'Volume 24h', 'trade_volume_24h_btc_normalized': 'Volume 24h normalisé'})
    #mise en forme des données
    df['Volume 24h'] = df['Volume 24h'].apply(lambda x: str(round(x, 2)) + ' BTC')
    df['Volume 24h normalisé'] = df['Volume 24h normalisé'].apply(lambda x: str(round(x, 2)) + ' BTC')
    
    st.write(df)


    st.markdown('---')

with st.container ():
    # création d'une map avec folium pour faire la localisation des exchanges

    # création d'un nouveau dataset regroupant les pays des exchanges et leur position géographique
    df = pd.DataFrame(df['Pays'].value_counts())
    df = df.reset_index()
    df = df.rename(columns={'index': 'Pays', 'Pays': 'Nombre d\'exchanges'})
    df = df.sort_values(by='Nombre d\'exchanges', ascending=False)
    df = df.head(100)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    df = df.rename(columns={'Pays': 'Country'})


    # nouveau dataframe avec les données du csv worldcities.csv
    df2 = pd.read_csv('worldcities.csv')
    #st.write(df2)

    # merge entre df et df2 pour récupérer que la colonne city si le pays est le même
    df = pd.merge(df, df2, how='left', left_on='Country', right_on='country')
    # garder que les lignes avec capital = primary
    df = df[df['capital'] == 'primary']
    # on garde que les colonnes qui nous intéressent
    df = df[['Country', 'Nombre d\'exchanges', 'city', 'lat', 'lng']]
    # on renomme les colonnes pour pouvoir matcher avec la fonction map de streamlit
    df = df.rename(columns={'city': 'City', 'lat': 'latitude', 'lng': 'longitude'})
    #st.write(df)

    st.subheader("Localisation des exchanges dans le monde")
    # placement des points sur la map
    st.map(df, zoom=1, use_container_width=True)

    st.markdown('---')

    st.subheader("Pourcentage des exchanges situé dans le monde par pays")
    # figure pie avec les pays et le nombre d'exchanges présent

    fig = px.pie(df, values='Nombre d\'exchanges', names='Country')
    st.plotly_chart(fig)

st.markdown('---')

with st.container():
    # volume de trade des exchanges sur map
    st.subheader("Volume de trade des exchanges dans le monde")

    # récupération des données dans un dataframe
    df_data = pd.DataFrame(exchange)
    #Mise en forme du dataframe des exchanges pour ne récupérer que les colonnes qui nous intéressent
    #df = exchange[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]
    df = df_data

    # création du nouveau dataset pour mettre les volumes de trade sur une map par pays
    df = pd.DataFrame(df['country'].value_counts())
    df = df.reset_index()
    df = df.rename(columns={'index': 'country', 'country': 'nombre_exchanges'})
    df = df.sort_values(by='nombre_exchanges', ascending=False)
    df = df.head(100)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    df = df.rename(columns={'country': 'Country'})

    # merge avec le dataframe df2 pour récupérer les coordonnées géographiques des exchanges
    df = pd.merge(df, df2, how='left', left_on='Country', right_on='country')
    # on ne garde que les exchanges avec une capital = primary
    df = df[df['capital'] == 'primary']

    # rajout des volumes de trade des exchanges
    df = pd.merge(df, df_data, how='left', left_on='Country', right_on='country')

    # on regroupe les volumes de trade par pays
    df = df.groupby(['Country', 'nombre_exchanges', 'city', 'lat', 'lng']).sum()
    df = df.reset_index()
    df = df.drop(columns=['year_established', 'trust_score'])
    df = df.rename(columns={'city': 'City', 'lat': 'latitude', 'lng': 'longitude'})
    df = df.sort_values(by='trade_volume_24h_btc', ascending=False)
    df = df.head(100)
    df = df.reset_index()
    df = df.drop(columns=['index'])


    # map en 3D avec les volumes de trade des exchanges par pays
    fig = px.scatter_3d(df, x='longitude', y='latitude', z='trade_volume_24h_btc', color='Country', size='trade_volume_24h_btc', hover_name='Country', size_max=20, opacity=0.7)
    st.plotly_chart(fig)

    st.markdown('---')

    # garder dans le dataset que certaines données
    df = df[['Country', 'longitude', 'latitude', 'trade_volume_24h_btc']]

    # figure avec bubble map sur les volumes de trade des exchanges
    st.subheader("Volumes de trade des exchanges par pays dans le monde")
    fig = px.scatter_geo(df, locations="Country", locationmode='country names', color="Country", hover_name="Country", size="trade_volume_24h_btc", projection="natural earth")
    st.plotly_chart(fig)

    st.markdown('---')

    # figure camembert sur les volumes de trade des exchanges par pays
    st.subheader("Volumes de trade des exchanges par pays")
    fig = px.pie(df, values='trade_volume_24h_btc', names='Country')
    st.plotly_chart(fig)

    st.markdown('---')


with st.container():
    # titre sur les scores de confiance des exchanges
    st.subheader("Volumes des trades des exchanges")

    df = pd.DataFrame(exchange)

    df = df.head(20)

    # figure en camembert sur les volumes d'échanges des exchanges
    st.subheader("Pourcentage des volumes de trade des exchanges sur 24h en BTC")
    fig = px.pie(df, values='trade_volume_24h_btc', names='name')
    st.plotly_chart(fig)
    st.markdown ('---')

    # figure de nuage de point sur les volumes d'échanges par exchanges
    st.subheader("Volumes de trade des exchanges en BTC sur 24h sans Binance")
    df = df[df['name'] != 'Binance']
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    st.markdown('---')

    # figure pairplot sur les volumes d'échanges par exchanges
    fig = px.scatter_matrix(df, dimensions=['name', 'trade_volume_24h_btc'], color='trade_volume_24h_btc')
    st.plotly_chart(fig)
    st.markdown('---')

    st.subheader(" Volumes de trade normalisés des exchanges sur 24h en BTC sans Binance")

    fig = px.scatter_3d(df, x='name', y='trade_volume_24h_btc_normalized', z='trade_volume_24h_btc', color='trade_volume_24h_btc', size='trade_volume_24h_btc', hover_name='name', size_max=20, opacity=0.7)
    st.plotly_chart(fig)
    st.markdown('---')

    #st.subheader(" Volumes de trade normalisés des exchanges sur 24h en BTC sans Binance")
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc_normalized', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    st.markdown('---')

# image de CoinGecko
st.header("Powerded by :")
st.image('img/logo.png', use_column_width=True)


