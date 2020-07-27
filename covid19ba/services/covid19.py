
import pandas as pd
import matplotlib.pyplot as plt
import gzip
import shutil
import requests
import numpy as np
import os.path
from datetime import datetime

def covid():
    data = pd.read_csv('covid19ba/data/caso_full.csv', sep= ',', parse_dates=True)
    data2=pd.DataFrame(columns=['cidade','tota_casos'])
    data = data.loc[data['state']=='BA']
    data2=data[['city','last_available_confirmed']].groupby(['city']).agg(
        total_casos=pd.NamedAgg(column='last_available_confirmed', aggfunc=max)
        )
    #data2.sort_values(by='total_casos', ascending=False).head(10)
    serieEstado=pd.DataFrame()
    serieEstado = data[['date','city','last_available_confirmed']].loc[data['state']=='BA']
    serieEstado.rename(columns={'last_available_confirmed': 'BA'}, inplace=True)
    serieEstado.set_index('date')

    cidades=serieEstado.city.unique()
    cidadesDict  = {elem : pd.DataFrame() for elem in cidades}
    for cidade in cidadesDict:
        cidadesDict[cidade] = pd.DataFrame(columns=['date','last_available_confirmed'])
        cidadesDict[cidade] = data[['date','last_available_confirmed']][data.city==cidade]
        cidadesDict[cidade].rename(columns={'last_available_confirmed': cidade}, inplace=True)
        cidadesDict[cidade].set_index('date')

    listColumns=cidades.tolist()
    listColumns.insert(0,'date')
    cidadesBahia = pd.DataFrame(columns=['date'])
    for cidade in cidadesDict:
        cidadesBahia = pd.merge(cidadesBahia,cidadesDict[cidade],how = 'outer', on='date', sort=True)
    cidadesBahia.columns = listColumns
    cidadesBahia.dropna(axis='columns', how='all',inplace=True)#, how='all')
    cidadesBahia.head()

    #cidadesBahia.to_csv('dados_bahia.csv',index=False)
    cidadesBahia.set_index('date', inplace=True)
    cidades=cidadesBahia.columns

    plt.rcParams["figure.figsize"] = (20, 10)
    plt.rcParams['legend.fontsize'] = 25
    plt.yscale('log')

    for i in cidades:
        #i =='Salvador') or
        if (int(cidadesBahia[i].max())<=1000) or (i=='Importados/Indefinidos'):
            continue
        elif (i =='Feira de Santana'):
            cidadesBahia[i].plot(linewidth=6, label = '%s, %d' % (i, int(cidadesBahia[i].max())))
        else:
            cidadesBahia[i].plot(label = '%s, %d' % (i, int(cidadesBahia[i].max())))
    plt.tick_params(labelsize='medium', width=3)
    plt.xticks(rotation=30, fontsize=20,label=cidadesBahia.index)
    plt.yticks(fontsize=20)
    plt.title('Curva Covid-19, Bahia',fontsize=40)
    plt.grid(True)
    plt.legend()
    plt.savefig('covid19ba/static/image/CurvaCovid.png')
    plt.close()

    
