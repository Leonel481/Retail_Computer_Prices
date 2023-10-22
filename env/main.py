import requests
import re
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import os
import json
s=HTMLSession()

from Funciones import *

# Abre el archivo JSON en modo lectura
with open('env/Direcciones_url.json', 'r') as archivo_json:
    # Carga el contenido del archivo JSON en un diccionario
    enlaces = json.load(archivo_json)

if __name__ == '__main__':
    data_total = pd.DataFrame()
    for k, v in enlaces['Impacto']['Categorias'].items():
        I_componentes = Impacto(enlaces['Impacto']['Principal'], v, 'df')
        I_componentes_pag = I_componentes.pagination()
        I_componentes_datos = I_componentes.scraper(I_componentes_pag)
        I_componentes_datos['Categoria'] = k
        data_total = pd.concat([data_total, I_componentes_datos])
        
    for k, v in enlaces['Sercoplus']['Categorias'].items():
        S_componentes = Sercoplus(enlaces['Sercoplus']['Principal'], v, 'df')
        S_componentes_pag = S_componentes.pagination()
        S_componentes_datos = S_componentes.scraper(S_componentes_pag)
        S_componentes_datos['Categoria'] = k
        data_total = pd.concat([data_total, S_componentes_datos])

    for k, v in enlaces['Cyccomputer']['Categorias'].items():
        C_componentes = Cyccomputer(enlaces['Cyccomputer']['Principal'], v, 'df')
        C_componentes_pag = C_componentes.pagination()
        C_componentes_datos = C_componentes.scraper(S_componentes_pag)
        C_componentes_datos['Categoria'] = k
        data_total = pd.concat([data_total, C_componentes_datos])
    
    #### Agregar la columna de marca