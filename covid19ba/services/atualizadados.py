import gzip
import shutil
import requests
import os.path
from datetime import datetime

def atualizadados():
    ler_data()
    url = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'
    r = requests.get(url, allow_redirects=True)
    open('covid19ba/data/caso_full.csv.gz', 'wb').write(r.content)

    with gzip.open('covid19ba/data/caso_full.csv.gz', 'rb') as entrada:
        with open('covid19ba/data/caso_full.csv', 'wb') as saida:
            shutil.copyfileobj(entrada, saida)

def ler_data():
    data_at = datetime.now().date()
    #if os.path.exists('covid19ba/data/data_at.txt'): 
    rr=open('covid19ba/data/data_at.txt', 'w+')
    rr.write(str(data_at))
    at = rr.readline()
    rr.close()
    #else:
     #   rr=open('covid19ba/data/data_at.txt', 'a+')
      #  rr.write(str(data_at))
      #  at = rr.readline()
       # rr.close()
    #return str(at) 
    