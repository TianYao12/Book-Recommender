import os
import time
import json
from tqdm import tqdm
from dotenv import load_dotenv
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv(".env.local")
KEY = os.environ["HUGGINGFACEHUB_API_TOKEN"]

# turns web-scrapped JSON documents into LangChain documents
def get_json_data() -> list:
    books = json.load(open("data/goodreads_books.json", "r")
                      )  # get json data from file
    documents = []

    for b in books:
        documents.append(Document(page_content=b["description"],  # append each book's information to documents list
            metadata={
            "title": b["title"],
            "authors": b["authors"],
            "image": b["image_url"],
            "url": b["url"]
        }))

    print(
        f"Loaded {len(documents)} documents\n Next we will split this into chunks")

    # perhaps switch up these numbers later
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(documents)
    return chunks

# turns document chunks into vectore stores


def get_vector_store(chunks: list, model: HuggingFaceInferenceAPIEmbeddings) -> FAISS:
    vsdatabase = []
    for i in tqdm(range(0, len(chunks), 400)):
        partial_vs = FAISS.from_documents(chunks[i: i+400], model) # 400 at a limit limit with Huggingface API
        vsdatabase.append(partial_vs)
        time.sleep(3)

    # Merge partial vector stores into one large vector store
    for partial_vs in tqdm(vsdatabase[1:]):
        vsdatabase[0].merge_from(partial_vs)
    vsdatabase[0].save_local("data/complete_vector_store")


def main():
    # load embeddings model
    model = HuggingFaceInferenceAPIEmbeddings(
        api_key=KEY, model_name="sentence-transformers/all-MiniLM-l6-v2"
    )

    # get vectorstore
    chunks = get_json_data()
    get_vector_store(chunks, model)


if __name__ == "__main__":
    main()
