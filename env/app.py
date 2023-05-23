## archivo .py del scrapper, en caso de usar selenium agregar en el env el plugin para el scraper
import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import os

# Agregar un .env de lista de paginas a screapear

class WebScrapper:
    def __init__(self,driver):
        self.category = ""
        self.url_base = ""
        self.driver = driver


#Connect Database Postgersql
conn = psycopg2.connect(
    host = os.getenv("HOST"),
    database = os.getenv("DATABASE"),
    user = os.getenv("USER"),
    password = os.getenv("PASS")
    port = os.getenv("HOST")
)

cursor = conn.cursor()