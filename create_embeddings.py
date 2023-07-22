import requests
from urllib.parse import urljoin
import pickle
from langchain import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import pylibmagic
from langchain.document_loaders import PlaywrightURLLoader, PyPDFLoader
from langchain.document_loaders.merge import MergedDataLoader
from dotenv import load_dotenv

import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

urls =['https://aryanswebsite.azurewebsites.net/',
       'https://aryanswebsite.azurewebsites.net/experiences',
       'https://aryanswebsite.azurewebsites.net/projects',
       'https://aryanswebsite.azurewebsites.net/certifications']
for url in urls:
    print(url)

loader_web = PlaywrightURLLoader(urls=urls)
loader_pdf = PyPDFLoader("static/resume.pdf")
loader_all = MergedDataLoader(loaders=[loader_web, loader_pdf])


data = loader_all.load()


text_splitter = CharacterTextSplitter(separator='\n',
                                      chunk_size=2000,
                                      chunk_overlap=200)


docs = text_splitter.split_documents(data)

embeddings = OpenAIEmbeddings()
vectorStore_openAI = FAISS.from_documents(docs, embeddings)

with open("my_website_embeddings", "wb") as f:
    pickle.dump(vectorStore_openAI, f)