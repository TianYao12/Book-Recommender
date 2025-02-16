This is book recommender where the user inputs a general prompt about a book's theme or details and it returns the top 5 books that suits the prompt.
The data is webscrapped from Goodreads (book title, author(s), description, image, url) and stored as vector stores (numerical data that the computer can understand not text data)

The user's prompt is also turned into vector stores and a FAISS similarity search on the data
The frontend is done in Streamlit and returns the top 5 books along with their metadata ((book title, author(s), image)

## Update:
- Added a CRAG implementation to test on other web scrapped books
