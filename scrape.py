import os
from bs4 import BeautifulSoup
import requests

def main():
    book_url = "https://www.goodreads.com/book/show/"
    for i in range(20):
        url = book_url + str(i)
        res = requests.get(url)
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.select(".Text__title1")
            print(links)
        else:
            print(f"Error: Unable to fetch the page. Status code: {res.status_code}")


if __name__ == '__main__':
    main()

