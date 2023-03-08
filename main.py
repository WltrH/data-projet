import streamlit as st
import time
import pandas as pd
import numpy as np
import seaborn as sns
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

#end_date = datetime.date.today()
#start_date = end_date - datetime.timedelta(days=1095)

# mettre les données dans un dataframe en connectant directement à l'API
#btc = pd.Dataframe(cg.get_coin_market_chart_range_by_id(id=id1, vs_currency=currency, from_timestamp=start_date, to_timestamp=end_date))
# placement d'une liste déroulante pour choisir la currency en passant par la fonction api.currencies
currency = 'usd'

# placement d'une liste pour choisir l'id de la crypto monnaie
id1 = 'bitcoin'

# placement d'une case pour choisir le second id de la crypto monnaie, mise à eth en default
id2 =  'ethereum'

#end_date_aff = end_date.strftime("%Y-%m-%d")
#start_date_aff = start_date.strftime("%Y-%m-%d")

#start_date = int(time.mktime(datetime.datetime.strptime(str(start_date), "%Y-%m-%d").timetuple()))
#end_date = int(time.mktime(datetime.datetime.strptime(str(end_date), "%Y-%m-%d").timetuple()))


# Récupération des données en passant par les fonctions de l'API
top10 = api.get_top10(currency)
exchange_simple = api.get_exchange_simple()


# transformation des données en dataframe
top10_brut = pd.DataFrame(top10)
exchange = pd.DataFrame(exchange_simple)


################### Données du TOP 10 ####################

with st.container():
    st.write('TOP10 des Crypto monnaies par capitalisation')
    # récuéprer les données dans un dataframe le top10 du marché
    #top10 = pd.DataFrame(cg.get_coins_markets(vs_currency=currency, order='market_cap_desc', per_page=10, page=1, sparkline=False, price_change_percentage='1h,24h,7d'))

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
    st.subheader("Graphique sur le TOP 10 au dessus")

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

with st.container():
    # titre sur les volumes des exchanges sur 24h des top 10
    st.subheader(" Graphique des prix des 10 premières crypto-monnaies sur 24h")

    # récupération des données dans un dataframe
    df = top10_brut[['id', 'current_price', 'high_24h', 'low_24h', 'price_change_percentage_24h']]

    # renommer les colonnes
    df = df.rename(columns={'id': 'Nom', 'current_price': 'Prix', 'high_24h': 'Haut 24h', 'low_24h': 'Bas 24h', 'price_change_percentage_24h': 'Variation % 24h'})

    

   
################### EXCHANGES ####################
with st.container():
# Titre sur l'exchange Binance
    st.subheader("Dataset des Exchanges mis en forme")

    #mise en forme du dataframe

    # récupération des données dans un dataframe
    #Mise en forme du dataframe des exchanges pour ne récupérer que les colonnes qui nous intéressent
    df = pd.DataFrame(exchange)
    df = df[['id', 'name', 'year_established', 'country', 'trust_score', 'trade_volume_24h_btc', 'trade_volume_24h_btc_normalized']]

    st.write(df)
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
    #mise en forme des données en pourcentage
    df['Score de confiance'] = df['Score de confiance'].map('{:,.2f}%'.format)
    #mise en forme des données en pourcentage
    df['Année de création'] = df['Année de création'].map('{:,.0f}'.format)
    


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

    #st.write(df)

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

    st.subheader("Localisation des exchanges")
    # placement des points sur la map
    st.map(df, zoom=1, use_container_width=True)

    st.subheader("Camembert des exchanges par pays")
    # figure pie avec les pays et le nombre d'exchanges présent

    fig = px.pie(df, values='Nombre d\'exchanges', names='Country')
    st.plotly_chart(fig)

st.markdown('---')

with st.container():
    # titre sur les scores de confiance des exchanges
    st.subheader("Volumes d'échanges des exchanges")

    df = pd.DataFrame(exchange)

    df = df.head(20)

    # figure en barre sur les volumes d'échanges des exchanges
    fig = px.bar(df, x='name', y='trade_volume_24h_btc', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

    # figure en camembert sur les volumes d'échanges des exchanges
    st.subheader("Camembert sur volumes de trade des exchanges")
    fig = px.pie(df, values='trade_volume_24h_btc', names='name')
    st.plotly_chart(fig)

    # figure de nuage de point sur les volumes d'échanges par exchanges
    st.subheader("Nuage de points sur volumes de trade des exchanges")
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

    # figure pairplot sur les volumes d'échanges par exchanges
    st.subheader("Pairplot sur volumes de trade des exchanges")
    fig = px.scatter_matrix(df, dimensions=['name', 'trade_volume_24h_btc'], color='trade_volume_24h_btc')
    st.plotly_chart(fig)

    # figure altair sur les volumes d'échanges par exchanges
    st.subheader("Altair sur volumes de trade des exchanges")
    fig = alt.Chart(df).mark_circle().encode(
        x='name',
        y='trade_volume_24h_btc',
        color='trade_volume_24h_btc',
        tooltip=['name', 'trade_volume_24h_btc']
    )
    st.altair_chart(fig, use_container_width=True)

    # figure altair sur les volumes d'échages normalisés par exchanges
    st.subheader("Altair sur volumes normalisés de trade des exchanges")
    fig = alt.Chart(df).mark_circle().encode(
        x='name',
        y='trade_volume_24h_btc_normalized',
        color='trade_volume_24h_btc_normalized',
        tooltip=['name', 'trade_volume_24h_btc_normalized']
    )
    st.altair_chart(fig, use_container_width=True)


    st.markdown('---')




