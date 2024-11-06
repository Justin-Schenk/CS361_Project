from flask import Flask, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for creating flashcards
@app.route('/create_flashcards')
def create_flashcards():
    return render_template('create_flashcards.html')

# Route for reviewing flashcards
@app.route('/review_flashcards')
def review_flashcards():
    return render_template('review_flashcards.html')

# Route for settings
@app.route('/settings')
def settings():
    return render_template('settings.html')

# Route for results
@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)