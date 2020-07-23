from django.shortcuts import render
import pandas as pd
import os

def index(request):

    # read data                                                                                                  
	
    data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + "/data/caso_full.csv", sep = ',')
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
	
    context = {"categories": categories, 'values': values, 'table_data':table_content}
    return render(request, 'index2.html', context=context)