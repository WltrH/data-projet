import streamlit as st
import streamlit_option_menu as st_option_menu
import pandas as pd
import plotly.express as px
import api as api
import warnings

from streamlit_extras import dataframe_explorer
from streamlit_extras.chart_container import chart_container

warnings.filterwarnings('ignore')


####################Setting######################
page_title = "Blockchain Data Analysis"
page_icon = ":bar_chart:"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

#################################################


############### sidebar ####################
with st.sidebar.header("Menu"):
    refresh = st.sidebar.button('Actualiser')

    if refresh:
        st.experimental_rerun()
    st.sidebar.markdown('---')

   
    
    #if selected == 'Accueil':
        

    # menu de navigation
    #page = st.sidebar.radio("Choisissez une page", ('Accueil', 'Top 10', 'Analyse des crypto-monnaies', 'Analyse des crypto-monnaies individuelles'))

#############################################



# presentation of the application
st.write('The app retrieves live data from a crypto-currency market API and allows you to select different options such as the currency and crypto-currencies to display.The app also displays relevant charts and tables to help visualize and analyze crypto-currency market data. Finally, it allows you to display the Top10 crypto-currencies in terms of market capitalization and view the data of each crypto-currency individually.')

currency = 'usd'

# Data retrieval through API functions
top10 = api.get_top10(currency)
exchange_simple = api.get_exchange_simple()

# transformation des données en dataframe
top10_brut = pd.DataFrame(top10)
exchange = pd.DataFrame(exchange_simple)


################### TOP 10 Data ####################

with st.container():
    st.subheader(' Dataset of the top 10 Crypto currencies by capitalization formatted')
    
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
    st.subheader("Analysis on the top 10 crypto-currencies")

    # formatting of the top10 dataframe to retrieve only the columns of interest
    top10 = top10_brut[['id','market_cap', 'current_price', 'fully_diluted_valuation', 'total_volume', 'high_24h', 'low_24h', 'price_change_24h', 'price_change_percentage_24h', 'market_cap_change_24h', 'market_cap_change_percentage_24h', 'circulating_supply', 'total_supply']]
    # rename the columns
    top10 = top10.rename(columns={'id': 'Nom', 'current_price': 'Prix', 'market_cap': 'Capitalisation', 'fully_diluted_valuation': 'Valeur totale', 'total_volume': 'Volume total', 'high_24h': 'Haut 24h', 'low_24h': 'Bas 24h', 'price_change_24h': 'Variation 24h', 'price_change_percentage_24h': 'Variation % 24h', 'market_cap_change_24h': 'Variation capitalisation 24h', 'market_cap_change_percentage_24h': 'Variation capitalisation % 24h', 'circulating_supply': 'Circulation', 'total_supply': 'Total'})

    st.subheader("Histogram of the Capitalization of the top 10 crypto-currencies")
    # bar chart of the capitalizations of the top 10 crypto currencies
    fig = px.bar(top10, x='Nom', y='Capitalisation', color='Capitalisation', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

    st.subheader("Volume pie chart of the top 10 crypto-currencies")
    # pie chart of the volumes of the top 10 crypto currencies
    fig = px.pie(top10, values='Volume total', names='Nom')
    st.plotly_chart(fig)

    st.markdown('---')


################################################ Crypto ###############################################
with st.container():

    # Tittle
    st.subheader("Market Cap volumes of the top 10 crypto-currencies over 24 hours")

    # data recovery in a dataframe
    df = pd.DataFrame(top10_brut)

    # dot plot on crypto currencies prices
    fig = px.scatter(df, x='current_price', y='market_cap', color='id', size='market_cap', hover_name='id', log_x=True, size_max=60)
    st.plotly_chart(fig)

    st.subheader("Histogram of the top 10 crypto-currencies over 24 hours")

    fig = px.bar(df, x='id', y='price_change_percentage_24h', color='price_change_percentage_24h', color_continuous_scale='Viridis')
    st.plotly_chart(fig)

    # dot plot on cirvulating supply
    fig = px.scatter(df, x='current_price', y='circulating_supply', color='id', size='circulating_supply', hover_name='id', log_x=True, size_max=60)
    st.plotly_chart(fig)

    # bar chart of circulating supply
    fig = px.bar(df, x='id', y='circulating_supply', color='circulating_supply', color_continuous_scale='Viridis')
    st.plotly_chart(fig)


   
################### EXCHANGES ####################
with st.container():
    # Tittle
    st.subheader("Formatted Exchanges Dataset")

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

    st.subheader("Location of exchanges in the world")
    # placement of points on the map
    st.map(df, zoom=1, use_container_width=True)

    st.markdown('---')

    st.subheader("Percentage of exchanges located in the world by country")

    # figure with the countries and the number of exchanges present
    fig = px.pie(df, values='Nombre d\'exchanges', names='Country')
    st.plotly_chart(fig)

st.markdown('---')

with st.container():
    # trade volume of exchanges on map
    st.subheader("Trade volume of exchanges in the world")

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
  
    # scatter plot on trade volumes of exchanges by country
    fig = px.area(df, x="Country", y="trade_volume_24h_btc", color="Country")
    st.plotly_chart(fig)


    st.markdown('---')

    # garder dans le dataset que certaines données
    df = df[['Country', 'longitude', 'latitude', 'trade_volume_24h_btc']]

    # figure with bubble map on trade volumes of exchanges
    st.subheader("Trade volumes of exchanges by country in the world")
    fig = px.scatter_geo(df, locations="Country", locationmode='country names', color="Country", hover_name="Country", size="trade_volume_24h_btc", projection="natural earth")
    st.plotly_chart(fig)

    st.markdown('---')

    # pie chart on trade volumes of exchanges by country
    st.subheader("Trade volumes of exchanges by country")
    fig = px.pie(df, values='trade_volume_24h_btc', names='Country')
    st.plotly_chart(fig)

    st.markdown('---')


with st.container():
    # Tittle
    st.subheader("Trade volumes of exchanges by country")

    df = pd.DataFrame(exchange)

    df = df.head(20)

    # is a pie chart of the trading volumes of the exchanges
    st.subheader("Percentage of trade volumes of exchanges over 24 hours in BTC")
    fig = px.pie(df, values='trade_volume_24h_btc', names='name')
    st.plotly_chart(fig)
    st.markdown ('---')

    # Scatter plot of trade volumes by trade
    st.subheader("Trade volumes of BTC exchanges over 24 hours without Binance")
    df = df[df['name'] != 'Binance']
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    st.markdown('---')

    # pairplot figure on trade volumes by exchange
    fig = px.scatter_matrix(df, dimensions=['name', 'trade_volume_24h_btc'], color='trade_volume_24h_btc')
    st.plotly_chart(fig)
    st.markdown('---')

    st.subheader("Normalized trade volumes of exchanges over 24 hours in BTC without Binance")

    fig = px.scatter_3d(df, x='name', y='trade_volume_24h_btc_normalized', z='trade_volume_24h_btc', color='trade_volume_24h_btc', size='trade_volume_24h_btc', hover_name='name', size_max=20, opacity=0.7)
    st.plotly_chart(fig)
    st.markdown('---')

 
    fig = px.scatter(df, x='name', y='trade_volume_24h_btc_normalized', color='trade_volume_24h_btc', color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    st.markdown('---')

# CoinGecko
st.header("Powerded by :")
st.image('img/logo.png', use_column_width=True)


