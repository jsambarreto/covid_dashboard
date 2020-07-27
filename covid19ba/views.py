from django.shortcuts import render
import pandas as pd
import os.path
from datetime import datetime
from .services import atualizadados, covid19, covid19m, mapa

def index(request):
    data_ex = datetime.now().date()
    aux=open('covid19ba/data/data_at.txt', 'r') 
    data_arm = aux.readline()
    aux.close()
    data_exibicao = data_ex.strftime("%d/%m/%Y")
    
    if str(data_ex) != data_arm:
        atualizadados.atualizadados()
        covid19.covid()
        covid19m.covidm()
        mapa.atualiza_mapa()
        # read data                                                                                                  
    data = pd.read_csv("covid19ba/data/caso_full.csv", sep = ',')
    data = data.loc[data['state']=='BA']
    data2=data[['city','last_available_confirmed']].loc[data['state']=='BA'].loc[data['city']!='Salvador']
    rs = data2.groupby('city')['last_available_confirmed'].max()
    visu = rs.to_frame().reset_index().sort_values(by = 'last_available_confirmed', ascending = False).rename(columns={'city': 'Município', 'last_available_confirmed': 'Total de casos confirmados'})
    categories = list(rs.index)
    values = list(rs.values)
    
    table_content = visu.to_html(index=None, justify = 'left')
    table_content = table_content.replace("","")
    table_content = table_content.replace('class="dataframe"',"class='table table-striped'")
    table_content = table_content.replace('border="1"',"")
    context = {"categories": categories, 'values': values, 'table_data':table_content, 'data_exibicao':data_exibicao}
    #    return render(request, 'index2.html', context=context)
    return render(request, 'index2.html', context=context)