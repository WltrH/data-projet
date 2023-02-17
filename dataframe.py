#import des bibliothèques pour statistiques et graphiques
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import json
warnings.filterwarnings('ignore')


#fonction d'ouverture d'un fichier json en argument
def openjson(file):
    with open(file) as f:
        data = json.load(f)
    return data

#fonction de mise dans un dataframe les inforamtions de data
def dataframe(data):
    df = pd.DataFrame(data)
    return df


