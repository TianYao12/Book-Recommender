import os
from bs4 import BeautifulSoup
import requests

def get_games():
    book_url = "https://www.goodreads.com/book/show/"
    req = requests.get(url=book_url).json()
    for i in range(2000):


