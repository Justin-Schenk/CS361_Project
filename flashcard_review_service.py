from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

# Initialize empty flashcards list
flashcards = []
current_index = None

# Function to fetch flashcards from creation service
def load_flashcards():
    global flashcards
    try:
        response = requests.get("http://localhost:5001/flashcards")  # URL of flashcard creation service
        if response.status_code == 200:
            flashcards = response.json()
        else:
            print("Failed to fetch flashcards.")
    except Exception as e:
        print(f"Error loading flashcards: {e}")

# Endpoint to start reviewing flashcards (selects a random question)
@app.route('/review/next', methods=['GET'])
def next_flashcard():
    load_flashcards()  # Ensure flashcards are loaded
    global current_index
    if not flashcards:
        return jsonify({"error": "No flashcards available for review"}), 404

    # Randomly select a flashcard for review
    current_index = random.randint(0, len(flashcards) - 1)
    return jsonify({"question": flashcards[current_index]["question"]}), 200

# Endpoint to reveal the answer for the current flashcard
@app.route('/review/reveal', methods=['GET'])
def reveal_answer():
    if current_index is None:
        return jsonify({"error": "No flashcard selected. Use /review/next first"}), 400

    answer = flashcards[current_index]["answer"]
    return jsonify({"answer": answer}), 200

# Endpoint to submit if the user got the answer correct or not
@app.route('/review/submit', methods=['POST'])
def submit_answer():
    if current_index is None:
        return jsonify({"error": "No flashcard selected. Use /review/next first"}), 400

    correct = request.json.get("correct")
    if correct is None:
        return jsonify({"error": "Missing 'correct' field in request body"}), 400

    message = "Well done!" if correct else "Keep trying!"
    return jsonify({"message": message}), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)
