from flask import Flask, render_template,jsonify,request
from flask_cors import CORS
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from waitress import serve
import os
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

#for production
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
# PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
# PINECONE_API_ENV = os.environ['PINECONE_API_ENV']

#for testing
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")


pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)
index_name = "portfolio"

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    # Add your chatbot logic here
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    question = data['message']
    with get_openai_callback() as cb:
        # with open(vectore_path, "rb") as f:
        #     VectorStore = pickle.load(f)
        embeddings = OpenAIEmbeddings()
        #VectorStore = FAISS.load_local("faiss_index_portfolio", embeddings)
        docsearch = Pinecone.from_existing_index(index_name, embeddings)
        llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
        chain = load_qa_chain(llm, chain_type="stuff")
        
        docs = docsearch.similarity_search(question)
        answer = chain.run(input_documents=docs, question=question)
        # print(cb)
        # print(answer)
    
    # Convert newlines in the answer to HTML line breaks '<br>'
    formatted_answer = answer.replace('\n', '<br>')
    
    response = {
        'reply': formatted_answer
    }
    return jsonify(response)

@app.route('/experiences')
def experiences():
    # Add your logic to fetch and pass past experiences data to the template
    return render_template('experiences.html')


@app.route('/projects')
def projects():
    # Add your logic to fetch and pass projects data to the template
    return render_template('projects.html')

@app.route('/skills')
def skills():
    # Add your logic to fetch and pass skills data to the template
    return render_template('skills.html')

@app.route('/certifications')
def certifications():
    # Add your logic to fetch and pass certifications data to the template
    return render_template('certifications.html')



if __name__ == '__main__':
    serve(app,host="0.0.0.0",port=80)
