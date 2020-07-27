import pandas as pd
import matplotlib.pyplot as plt
#import gzip
#import shutil
import requests
import numpy as np
import matplotlib as mpl
#import seaborn as sns
#import datetime
import warnings
import os
warnings.filterwarnings("ignore")

def covidm():
        
    data = pd.read_csv('covid19ba/data/caso_full.csv', sep= ',', parse_dates=True)
    data2=pd.DataFrame(columns=['cidade','total_obito'])
    data = data.loc[data['state']=='BA']
    data2=data[['city','last_available_deaths']].groupby(['city']).agg(
        total_obito=pd.NamedAgg(column='last_available_deaths', aggfunc=max)
        )

    #data2.sort_values(by='total_obito', ascending=False).head(10)

    serieEstado_=pd.DataFrame()
    serieEstado_ = data[['date','city','last_available_deaths']].loc[data['state']=='BA']
    serieEstado_.rename(columns={'last_available_deaths': 'BA'}, inplace=True)
    serieEstado_.set_index('date')

    cidades=serieEstado_.city.unique()
    cidadesDict_  = {elem : pd.DataFrame() for elem in cidades}
    for cidade in cidadesDict_:
        cidadesDict_[cidade] = pd.DataFrame(columns=['date','last_available_deaths'])
        cidadesDict_[cidade] = data[['date','last_available_deaths']][data.city==cidade]
        cidadesDict_[cidade].rename(columns={'last_available_deaths': cidade}, inplace=True)
        cidadesDict_[cidade].set_index('date')
    listColumns=cidades.tolist()
    listColumns.insert(0,'date')

    cidadesBahia_ = pd.DataFrame(columns=['date'])
    for cidade in cidadesDict_:
        cidadesBahia_ = pd.merge(cidadesBahia_,cidadesDict_[cidade],how = 'outer', on='date', sort=True)
    cidadesBahia_.columns = listColumns
    cidadesBahia_.dropna(axis='columns', how='all',inplace=True)#, how='all')
    cidadesBahia_.head()
    #cidadesBahia.to_csv('dados_bahia_m.csv',index=False)
    cidadesBahia_.set_index('date', inplace=True)
    cidades=cidadesBahia_.columns
    plt.rcParams["figure.figsize"] = (23, 9)
    plt.rcParams['legend.fontsize'] = 25
    plt.yscale('log')
    for i in cidades:
        #or (i =='Salvador')
        if (int(cidadesBahia_[i].max())<=50): 
            continue
        elif (i =='Feira de Santana'):
            cidadesBahia_[i].plot(linewidth=6, label = '%s, %d' % (i, int(cidadesBahia_[i].max())))
        else:
            cidadesBahia_[i].plot(label = '%s, %d' % (i, int(cidadesBahia_[i].max())))
    plt.tick_params(labelsize='medium', width=3)
    plt.xticks(rotation=30, fontsize=20,label=cidadesBahia_.index)
    plt.yticks(fontsize=20)
    plt.title('Curva Mortalidade Covid 19, Bahia',fontsize=40)   
    plt.grid(True)
    plt.legend()
    plt.savefig('covid19ba/static/image/CurvaCovidMortalidade.png')
    plt.close()