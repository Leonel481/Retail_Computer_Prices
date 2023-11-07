import requests
import re
import pandas as pd
import pymysql
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import numpy as np
import json
# import os
import time
from unicodedata import normalize
s=HTMLSession()

from Funciones import *

if __name__ == '__main__':
# def lambda_handler(event, context):   

    # Abre el archivo JSON en modo lectura
    with open('Direcciones_url.json', 'r') as archivo_json:
    # Carga el contenido del archivo JSON en un diccionario
        enlaces = json.load(archivo_json)

    brands = brand()
                

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



    brands_l = {"marca":brands}
    brand_json = json.dumps(brands_l)

    category_dic = {"categoria":["Placa Madre","Cooler Refrigeración",
                        "Memoria Ram","Case","Fuente de Poder",
                        "Procesador","Almacenamiento","Tarjeta de Video",
                        "Monitores"]
                        }

    category_json = json.dumps(category_dic)

    company_dic = {"empresa":["Impacto","Sercoplus","Cyccomputer"]}
    company_json = json.dumps(company_dic)

    data_codes = data_total[['codes']]
    data_codes_l = data_codes.to_dict(orient='records')
    data_codes_json = json.dumps(data_codes_l)

    # conn = pymysql.connect(host='localhost',
    #                         user='Leo', 
    #                         passwd='L4l14g4.492', 
    #                         db='dbtestscraping', 
    #                         connect_timeout=30)

    conn = pymysql.connect(host='database-appcps.cxrjcnbakf8k.us-east-1.rds.amazonaws.com',
                        user='adminAppCPS', 
                        passwd='4dm1nFtg4slCPS', 
                        db='dbscraping', 
                        connect_timeout=150)

    ##DB local usar: dbtestscraping, DB AWS: dbscraping
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbscraping.products_category")
    categoria_df = pd.DataFrame(cursor.fetchall(), columns=['categoria_id','categoria'])

    data_total_t = data_total.merge(categoria_df, on='categoria', how='left')
    data_total_t = data_total_t.drop(columns='categoria')

    cursor.execute("SELECT * FROM dbscraping.products_company")
    company_df = pd.DataFrame(cursor.fetchall(), columns=['empresa_id','empresa'])

    data_total_t = data_total_t.merge(company_df, on='empresa', how='left')
    data_total_t = data_total_t.drop(columns='empresa')

    cursor.execute("SELECT * FROM dbscraping.products_brand")
    marca_df = pd.DataFrame(cursor.fetchall(), columns=['marca_id','marca'])

    data_total_t = data_total_t.merge(marca_df, on='marca', how='left')
    data_total_t = data_total_t.drop(columns='marca')

    cursor.execute("SELECT * FROM dbscraping.products_codes")
    codes_df = pd.DataFrame(cursor.fetchall(), columns=['codes_id','codes'])

    data_total_t = data_total_t.merge(codes_df, on='codes', how='left')
    data_total_t = data_total_t.drop(columns='codes')

    data_total_t = data_total_t.fillna(value=0)

    data_total_dic = data_total_t.to_dict(orient='records')

    data_json= json.dumps(data_total_dic)

    #Carga de datos Codes
    parsed_codes = json.loads(data_codes_json)

    with conn.cursor() as cursor:
        for row in parsed_codes:
                sql = """
                    INSERT IGNORE INTO dbscraping.products_codes (codes)
                    VALUES (%s)
                """
                cursor.execute(sql, (row['codes']))

    conn.commit()

    #Carga de datos Company
    parsed_company = json.loads(company_json)
    with conn.cursor() as cursor:
        for row in parsed_company['empresa']:
                sql = """
                    INSERT IGNORE INTO dbscraping.products_company (empresa)
                    VALUES (%s)
                """
                cursor.execute(sql, (row))

    conn.commit()

    #Carga de datos Category
    parsed_category = json.loads(category_json)
    with conn.cursor() as cursor:
        for row in parsed_category['categoria']:
                sql = """
                    INSERT IGNORE INTO dbscraping.products_category (categoria)
                    VALUES (%s)
                """
                cursor.execute(sql, (row))

    conn.commit()

    #Carga de datos Brand
    parsed_brand = json.loads(brand_json)
    with conn.cursor() as cursor:
        for row in parsed_brand['marca']:
                sql = """
                    INSERT IGNORE INTO dbscraping.products_brand (marca)
                    VALUES (%s)
                """
                cursor.execute(sql, (row))

    conn.commit()

    #Carga de datos Productos
    parsed_data = json.loads(data_json)
    with conn.cursor() as cursor:
        for row in parsed_data:
                sql = """
                    INSERT IGNORE INTO dbscraping.products_product (titles,links,codes_id,stocks,ratings,prices_usd,prices_pen,images,Fecha,categoria_id,empresa_id,marca_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (row['titles'],row['links'],row['codes_id'],row['stocks'],row['ratings'],row['prices_usd'],row['prices_pen'],
                                        row['images'],row['Fecha'],row['categoria_id'],row['empresa_id'],row['marca_id']))

    conn.commit()

    conn.close()


    # return  {
    #     'statuscode':200,
    #     'body_data': 'Succesful'
    # }


    # data_total = data_total.dropna(subset=['marca'])
    data_total.to_csv(r'C:\GitHub\prices10.csv',index=False)
    print('succes')  