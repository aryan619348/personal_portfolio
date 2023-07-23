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
from langchain.vectorstores import Pinecone
import pinecone
import os
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY', '678e32a3-6032-41cf-ba35-4646120509f3')
PINECONE_API_ENV = os.environ.get('PINECONE_API_ENV', 'us-west4-gcp-free')

pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "portfolio"

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

docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)
""