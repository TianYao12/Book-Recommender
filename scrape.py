import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import time

def scrape_book_info(book_id):
    url = f'https://www.goodreads.com/book/show/{book_id}'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting information with error handling
    title_element = soup.select_one('h1[data-testid="bookTitle"]')
    image_element = soup.select_one('img[class="ResponsiveImage"]')
    description_element = soup.select_one('span[class="Formatted"]')
    author_elements = soup.find_all(
        'span', class_='ContributorLink__name', attrs={'data-testid': 'name'})

    # Check if elements are present before extracting text or attributes
    title = title_element.get_text(strip=True) if title_element else None
    image_url = image_element['src'] if image_element and 'src' in image_element.attrs else None
    description = description_element.get_text(
        strip=True) if description_element else None
    authors = list(set(author_element.get_text(strip=True) for author_element in author_elements))


    book_info = {
        'title': title,
        'image_url': image_url,
        'description': description,
        'url': url,
        'authors': authors
    }
    return book_info


def scrape_books(start_id, end_id, step):
    all_books_info = []

    for book_id in range(start_id, end_id, step):
        book_info = scrape_book_info(book_id)
        if book_info and book_info['title'] and book_info['image_url'] and book_info['description']:
            all_books_info.append(book_info)
        lag = np.random.uniform(low=1, high=3)
        print(f'...waiting {round(lag,1)} seconds...')
        time.sleep(lag)
    return all_books_info


if __name__ == "__main__":
    start_book_id = 1
    end_book_id = 10000
    step = 10

    book_info_list = scrape_books(start_book_id, end_book_id, step)

    # print(book_info_list)

    # Save the scraped data to a JSON file
    with open('goodreads_books.json', 'w') as f:
        json.dump(book_info_list, f, indent=2)
