from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os
import csv

app = Flask(__name__)
CORS(app)
# In-memory storage for flashcards
flashcards = pd.DataFrame(columns=['question', 'answer'])


# Endpoint to add flashcards from a CSV file upload
@app.route('/upload_flashcards', methods=['POST'])
def upload_flashcards():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        file = request.files['file']

        # Check if a file was uploaded
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Check for CSV format
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "File must be a CSV"}), 400

        try:
            # Read the CSV file into a DataFrame
            new_flashcards = pd.read_csv(file)
        except pd.errors.ParserError as e:
            return jsonify({"error": f"Failed to parse CSV file: {e}"}), 400

        # Validate that it has the required columns
        if not all(column in new_flashcards.columns for column in ['question', 'answer']):
            return jsonify({"error": "CSV file must contain 'question' and 'answer' columns"}), 400

        global flashcards
        flashcards = pd.concat([flashcards, new_flashcards], ignore_index=True)

        return jsonify({"message": "Flashcards added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to manually add a single flashcard
@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    try:
        question = request.form.get('question')
        answer = request.form.get('answer')

        if not question or not answer:
            return jsonify({"error": "Both 'question' and 'answer' are required"}), 400

        global flashcards
        new_flashcard = pd.DataFrame([{'question': question, 'answer': answer}])
        flashcards = pd.concat([flashcards, new_flashcard], ignore_index=True)

        # Append the new flashcard to the CSV file
        with open('flashcards.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([question, answer])

        return jsonify({"message": "Flashcard added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to view all flashcards (for testing purposes)
@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    try:
        return jsonify(flashcards.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001, debug=True)
