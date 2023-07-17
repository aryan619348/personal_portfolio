from flask import Flask, render_template

app = Flask(__name__)

app.static_folder = 'static'


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    # Add your chatbot logic here
    return render_template('chat.html')

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
    app.run(debug=True,port=8000)
