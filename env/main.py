import requests
import re
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import os
import json
import time
from unicodedata import normalize
s=HTMLSession()

from Funciones import *

# Abre el archivo JSON en modo lectura
with open('Direcciones_url.json', 'r') as archivo_json:
    # Carga el contenido del archivo JSON en un diccionario
    enlaces = json.load(archivo_json)

def normalize_text(s):
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    s_normalize = normalize('NFKC', normalize('NFKD', s).translate(trans_tab))
    return s_normalize

brands = brand()

def look_brand(title, brands):
    dict_brands = {"CM ": "COOLER MASTER", "HIKSEMI": "HIKSEMI", "RYZEN": "AMD", "PROART": "ASUS", "WD": "WESTERN DIGITAL"}
    for brand in brands:
        if brand in title:
            return brand
        else:
            for k, v in dict_brands.items():
                if k in title:
                    return v
                

if __name__ == '__main__':
    data_total = pd.DataFrame()
    print(time.time())
    for k, v in enlaces['Impacto']['Categorias'].items():
        I_componentes = Impacto(enlaces['Impacto']['Principal'], v, 'df')
        I_componentes_pag = I_componentes.pagination()
        I_componentes_datos = I_componentes.scraper(I_componentes_pag)
        I_componentes_datos['categoria'] = k
        I_componentes_datos['empresa'] = "Impacto"
        data_total = pd.concat([data_total, I_componentes_datos])
    print('Impacto succes - Procces Time: ', time.time())

    for k, v in enlaces['Sercoplus']['Categorias'].items():
        S_componentes = Sercoplus(enlaces['Sercoplus']['Principal'], v, 'df')
        S_componentes_pag = S_componentes.pagination()
        S_componentes_datos = S_componentes.scraper(S_componentes_pag)
        S_componentes_datos['categoria'] = k
        S_componentes_datos['empresa'] = "Sercoplus"
        data_total = pd.concat([data_total, S_componentes_datos])
    print('Sercoplus succes - Procces Time: ',time.time())

    for k, v in enlaces['Cyccomputer']['Categorias'].items():
        C_componentes = Cyccomputer(enlaces['Cyccomputer']['Principal'], v, 'df')
        C_componentes_pag = C_componentes.pagination()
        C_componentes_datos = C_componentes.scraper(C_componentes_pag)
        C_componentes_datos['categoria'] = k
        C_componentes_datos['empresa'] = "Cyccomputer"
        data_total = pd.concat([data_total, C_componentes_datos])
    print('Cyc succes - Procces Time: ',time.time())   

    #### Agregar la columna de marca
    data_total['marca'] =  data_total.apply(lambda row: look_brand(normalize_text(row.titles), brands), axis=1)
    data_total = data_total.dropna(subset=['marca'])
    

