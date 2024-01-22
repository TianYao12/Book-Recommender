import os
import streamlit as st 
from dotenv import load_dotenv
from backend import load_db, search
from langchain.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings

# Prep data
load_dotenv(".env.local")
KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN")

model = HuggingFaceInferenceAPIEmbeddings(
        api_key=KEY, model_name="sentence-transformers/all-MiniLM-l6-v2"
    )
db = load_db(model)

# Context
st.title("Book Recommender")
st.write("Search for some general themes and/or details of a book: ")
