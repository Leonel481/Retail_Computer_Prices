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

def Iterador(f):
    """Función que permite descargar los datos 15 veces como máximo y los consolida en una tabla total para posteriormente eliminar los duplicados
    en función del código de referencia y mantiene los datos más recientes"""
    def Wrapper(*args):
        data = pd.DataFrame()
        for r in range(0, 15):
            dft = f(*args)
            if r == 0:
                y = len(dft)
            data = pd.concat([data, dft])
            data = data.drop_duplicates(subset=['codes'], keep='last')
            if len(data)>=y:
                break
            else:
                pass
        return data
    return Wrapper

class Impacto:
    def __init__(self, url_base, category, source):
        self.url_base = url_base
        self.category = category
        self.source = source
        self.list_titles = []
        self.list_links = []
        self.list_codes = []
        self.list_stocks = []
        self.list_ratings = []
        self.list_prices_usd = []
        self.list_prices_pen = []
        self.list_images = []        
    def __str__(self):
        return f"Extrae informacion de la categoria: {self.category} y la almacenada: {self.source}"
    def pagination(self):
        r = s.get(self.url_base + self.category)
        soup = BeautifulSoup(r.text, 'html.parser')
        pages = soup.find('ul',class_= 'pagination')
        number_pag = int(pages.find_all('a', class_= 'page-link')[-2].text)
        return number_pag
    
    def scraper(self, n):
        for i in range(1, n + 1):
            url = self.url_base + self.category + "&page=" + str(i)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            titles = soup.find_all('h4', class_='product-title')
            details = soup.find_all('div', class_='detail')
            ratings = soup.find_all('ul', class_='product-rating')
            prices = soup.find_all('div', class_='product-price')
            images = soup.find_all('div', class_='product-image')

            for title in titles:
                a = title.text.strip()
                self.list_titles.append(a)
                b = title.find('a')['href']  
                self.list_links.append(b)

            for detail in details:
                a = detail.text.strip()
                list_temp = a.split('\n')
                b = re.sub(r'[\D]+', '', list_temp[0])
                c = re.sub(r'[\D]+', '', list_temp[1])
                self.list_codes.append(b)
                self.list_stocks.append(c)

            for rating in ratings:
                list_temp_r = rating.find_all('li', class_='rating-on')
                self.list_ratings.append(len(list_temp_r))

            for price in prices:
                list_temp_pr = price.text.strip().split('\n')
                p_sol = float(re.sub(r'[\s$\-,]+','',list_temp_pr[0]))
                p_dollar = float(re.sub(r'[\sS\-\/,]+','',list_temp_pr[1]))
                self.list_prices_usd.append(p_sol)
                self.list_prices_pen.append(p_dollar)

            for image in images:
                i = image.find('img')['src']
                self.list_images.append(i)
            data = {'titles':self.list_titles, 'links':self.list_links, 'codes':self.list_codes, 'stocks':self.list_stocks,
                    'ratings':self.list_ratings, 'prices_usd':self.list_prices_usd, 'prices_pen':self.list_prices_pen, 'images':self.list_images}
        dataDF = pd.DataFrame(data = data)
        dataDF['Fecha'] = datetime.now().strftime('%d-%m-%Y %H:%M')
        return dataDF
    
class Sercoplus:
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47'}
    def __init__(self, url_base, category, source):
        self.url_base = url_base
        self.category = category
        self.source = source
        self.list_titles=[]
        self.list_links=[]
        self.list_stocks=[]
        self.list_codes=[]
        self.list_prices_usd=[]
        self.list_prices_pen=[]
        self.list_images = []
    def __str__(self):
        return f"Extrae informacion de la categoria: {self.category} y la almacenada: {self.source}"
    def pagination(self):
        """Permite obtener el número de páginas totales de la categoria a escrapear"""
        url = self.url_base + self.category
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        pages = soup.find('ul', class_='page-list')
        pagina_final = pages.find_all('a', class_='js-search-link')[-2].text
        pagina_final = int(pagina_final.strip())
        return pagina_final
    @Iterador
    def scraper(self, n):
        session = requests.Session()
        for i in range(1, n + 1):
            if i == 1:
                url = self.url_base + self.category
            else:
                url = self.url_base + self.category + '?page=' + str(i)
            r = session.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            blocks = soup.find_all('article', class_ = "product-miniature js-product-miniature")
            for block in blocks:
                first_block = block.find_all('a', class_='product-cover-link')
                self.list_links.append(first_block[0]['href'])
                self.list_titles.append(first_block[0].find('img', class_="img-fluid js-lazy")['title'])
                try:
                    img = first_block[0].find('img', class_="img-fluid js-lazy")['data-original']
                    self.list_images.append(img)
                except KeyError:
                    self.list_images.append(None)
                third_block = block.find_all('div', class_='product-price-and-shipping d-flex flex-column')
                stock = third_block[0].find_all('span', class_ = 'price product-price stock-mini')[1]['data-stock']
                code = third_block[0].find_all('span', class_ = 'price product-price stock-mini')[3].text
                price_usd = re.sub(r'[^\d,]', '', third_block[0].find_all('span', class_='price product-price currency2')[0].text).replace(',', '.')
                price_pen = re.sub(r'[^\d,]', '', third_block[0].find_all('span', class_='price product-price currency2')[1].text).replace(',', '.')
                self.list_stocks.append(int(stock.strip()))
                self.list_codes.append(code.strip())
                self.list_prices_usd.append(float(price_usd))
                self.list_prices_pen.append(float(price_pen))
            data = {'titles':self.list_titles, 'links':self.list_links, 'codes':self.list_codes, 'stocks':self.list_stocks,
                    'prices_usd':self.list_prices_usd, 'prices_pen':self.list_prices_pen, 'images':self.list_images}
        dataDF = pd.DataFrame(data = data)
        dataDF['Fecha'] = datetime.now().strftime('%d-%m-%Y %H:%M')
        return dataDF
    
class Cyccomputer:
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47'}
    def __init__(self, url_base, category, source):
        self.url_base = url_base
        self.category = category
        self.source = source
        self.list_titles=[]
        self.list_links=[]
        self.list_stocks=[]
        self.list_codes=[]
        self.list_prices_usd=[]
        self.list_prices_pen=[]
        self.list_images = []
    def __str__(self):
        return f"Extrae informacion de la categoria: {self.category} y la almacenada: {self.source}"
    def pagination(self):
        """Permite obtener el número de páginas totales de la categoria a escrapear"""
        url = self.url_base + self.category
        r = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        pages = soup.find('ul', class_='page-list clearfix text-sm-center')
        pagina_final = pages.find_all('a', class_='js-search-link')[-2].text
        pagina_final = int(pagina_final.strip())
        return pagina_final
    @Iterador
    def scraper(self, n):
        session = requests.Session()
        for i in range(1, n + 1):
            if i == 1:
                url = self.url_base + self.category
            else:
                url = self.url_base + self.category + '?page=' + str(i)
            r = session.get(url, headers=self.headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            soup_product = soup.find('div', class_ = "laberProductGrid laberProducts")
            total_blocks = soup_product.find_all('article', class_ = "product-miniature js-product-miniature")
            for total_block in total_blocks:
                code = total_block["data-id-product"]
                block = total_block.find('div', class_ = "laberProduct-container")
                link = block.find('a', class_ = "thumbnail product-thumbnail").get('href')
                image = block.find('a', class_ = "thumbnail product-thumbnail").find('span', class_ = "cover_image").find('img').get('src')
                titule = block.find('h2', class_ = "productName").text
                stock = re.sub(r'[^\d]', '', block.find('div', class_ = "product-quantities manufacturer_name").text)
                price_usd = re.sub(r'[^\d,]', '', block.find_all('span', class_ = "price pr")[0].text).replace(',','.')
                price_pen = re.sub(r'[^\d,]', '', block.find_all('span', class_ = "price pr")[1].text).replace(',','.')
                self.list_codes.append(code.strip())
                self.list_links.append(link)
                self.list_images.append(image)
                self.list_titles.append(titule.strip())
                self.list_stocks.append(int(stock.strip()))
                self.list_prices_usd.append(float(price_usd))
                self.list_prices_pen.append(float(price_pen))
            data = {'titles':self.list_titles, 'links':self.list_links, 'codes':self.list_codes, 'stocks':self.list_stocks,
                    'prices_usd':self.list_prices_usd, 'prices_pen':self.list_prices_pen, 'images':self.list_images}
        dataDF = pd.DataFrame(data = data)
        dataDF['Fecha'] = datetime.now().strftime('%d-%m-%Y %H:%M')
        return dataDF