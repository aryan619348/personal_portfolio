from flask import Flask, render_template,jsonify,request

app = Flask(__name__)

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
    message = data['message']

    # Your chatbot logic goes here
    # Process the user's message and generate a system reply

    # For example, let's say the system reply is stored in the 'system_reply' variable
    system_reply = "This is the system's reply."

    response = {
        'reply': system_reply
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
    app.run(debug=True,port=5000)
