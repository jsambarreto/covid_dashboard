import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gzip
import shutil
import requests
import subprocess
from geopy.geocoders import Nominatim
import folium
from folium import plugins

def atualiza_mapa():
    
    dataB = pd.read_csv('covid19ba/data/caso_full.csv', sep= ',', parse_dates=True)
    dataB['localizacao'] = dataB['city']+ ','+dataB['state']+',Brasil'
    dataB = dataB.dropna()
    dataBA = dataB.loc[dataB['state']=='BA']
    serie = dataBA.localizacao.unique()
    
    hsh_at = (str(hash(str(serie))))
    
    if hsh_at != ver_dt_map():
        hsh = open('covid19ba/data/hashCidades.txt', 'w+')
        hsh.write(hsh_at)
        geolocator = Nominatim(user_agent="AnaliseCovidBrasil")

        localizacao = []
        latitude = []
        longitude = []

        for user_location in serie:
            try:
                location = geolocator.geocode(user_location)
                localizacao.append(user_location)
                latitude.append(location.latitude)
                longitude.append(location.longitude)
            except:
                continue
        
        arq = open('covid19ba/data/ba_lat_lng.csv', 'w+')
        j = 0
        arq.write('localizacao;latitude;longitude\n')

        for i in serie: 
            try:
                #print('%s %s %s %i' % (localizacao[j], latitude[j], longitude[j], j))
                arq.write('%s;%s;%s \n' % (localizacao[j], latitude[j], longitude[j]))
                j+=1
            except:
                continue
        arq.close()

        dataloc = pd.read_csv('covid19ba/data/ba_lat_lng.csv', sep=';')
        dataBA_ = pd.merge(dataBA, dataloc, on = 'localizacao')
        coordenadas = np.column_stack((dataBA_.latitude, dataBA_.longitude))
        center = latitude[0],longitude[0]
        mapa = folium.Map(location = center,zoom_start=6,parse_html=True)
        mapa.add_child(plugins.HeatMap(coordenadas))
        mapa.save('covid19ba/static/image/mapacovid.html')

def ver_dt_map():
    hsh = open('covid19ba/data/hashCidades.txt', 'r')
    comp = hsh.readline()
    return comp
    