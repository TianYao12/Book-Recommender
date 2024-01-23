import os
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores.faiss import FAISS

# get huggingface api token
load_dotenv(".env.local")
KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Searches for the top 5 similar books for the search query
def search(query: str, database: FAISS, k: int = 5) -> list:
    return database.similarity_search(query, k=k)

# load vector store
def load_db(embeddings: HuggingFaceInferenceAPIEmbeddings) -> FAISS:
    return FAISS.load_local("data/complete_vector_store", embeddings)

model = HuggingFaceInferenceAPIEmbeddings(
    api_key=KEY, model_name="sentence-transformers/all-MiniLM-l6-v2"
)
db = load_db(model)

# Context
st.title("Book Recommender")
st.write("Search for some general themes and details of books: ")

# Search inputs
with st.sidebar:
    with st.form(key='user_input'):
        query = st.text_input("Book details", max_chars=100,
                              placeholder="Wizards in castles")
        submit = st.form_submit_button("Search")

if submit and query:
    results = search(query, db)
    st.write("**Here are some books you may be interested in**")

    for result in results:
        metadata = result.metadata
        title = metadata['title']
        image = metadata['image']
        authors = metadata['authors']
        url = metadata['url']

        st.markdown(f"[{title}]({url})")

        col1, col2 = st.columns([1, 2])
        col1.image(image, caption=title, use_column_width=False, width=200)

        col2.write("Author(s):")
        for author in authors:
            col2.write(author)
        col2.write("Description:")
        col2.write(result.page_content)
       
# user presses submit and does not provide any prompt
elif submit and not query:
    st.write("You didn't write anything. Please type something in")
