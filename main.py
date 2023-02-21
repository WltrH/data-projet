import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# création du titre
st.title("Crypto-Monnaies Data")

# création du sous-titre
st.subheader("Top 10 des crypto-monnaies")

# création d'un tableau des 10 premières crypto monnaies, en partant du fichier json Top10
# avec les colonnes suivantes : nom, prix, volume, capitalisation, %1h, %24h, %7j
df = pd.read_json('json/top10.json')
df = df[['name', 'current_price', 'total_volume', 'market_cap', 'price_change_percentage_1h_in_currency', 'price_change_percentage_24h_in_currency', 'price_change_percentage_7d_in_currency']]
df = df.rename(columns={'name': 'Nom', 'current_price': 'Prix', 'total_volume': 'Volume', 'market_cap': 'Capitalisation', 'price_change_percentage_1h_in_currency': '%1h', 'price_change_percentage_24h_in_currency': '%24h', 'price_change_percentage_7d_in_currency': '%7j'})
st.table(df)

# graphique des capitalisations des 10 premières crypto monnaies
df = pd.read_json('json/top10.json')
df = df[['name', 'market_cap']]
df = df.rename(columns={'name': 'Nom', 'market_cap': 'Capitalisation'})
df = df.sort_values(by='Capitalisation', ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x='Nom', y='Capitalisation', data=df)
plt.xticks(rotation=90)
plt.title('Capitalisation des 10 premières crypto monnaies')
st.pyplot()

