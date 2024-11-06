from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import random


app = Flask(__name__)
CORS(app)

# Initialize empty flashcards list and review statistics
flashcards = []
current_index = None
review_statistics = {
    "total": 0,
    "correct": 0,
    "incorrect": 0
}

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
    global current_index, review_statistics

    if not flashcards:
        return jsonify({"error": "No flashcards available for review"}), 404

    # Randomly select a flashcard for review
    current_index = random.randint(0, len(flashcards) - 1)

    # Increment the total count of reviewed questions
    review_statistics["total"] += 1

    return jsonify({"question": flashcards[current_index]["question"]}), 200

# Endpoint to reveal the answer for the current flashcard
@app.route('/review/reveal', methods=['GET'])
def reveal_answer():
    if current_index is None:
        return jsonify({"error": "No flashcard selected. Use /review/next first"}), 400

    answer = flashcards[current_index]["answer"]
    return jsonify({"answer": answer}), 200

# Review statistics for correct and incorrect answers
review_stats = {"correct": 0, "incorrect": 0}

# Endpoint to submit if the user got the answer correct or not
@app.route('/review/submit', methods=['POST'])
def submit_answer():
    data = request.get_json()
    if "correct" in data:
        if data["correct"]:
            review_stats["correct"] += 1
        else:
            review_stats["incorrect"] += 1
        return jsonify({"message": "Answer recorded successfully"}), 200
    else:
        return jsonify({"error": "Invalid data"}), 400

@app.route('/end_review', methods=['GET'])
def end_review():
    # Capture the stats before resetting
    total = review_stats["correct"] + review_stats["incorrect"]
    correct = review_stats["correct"]
    incorrect = review_stats["incorrect"]

    # Reset the statistics for the next session
    review_stats["correct"] = 0
    review_stats["incorrect"] = 0

    # Return the final statistics
    return jsonify({
        "total": total,
        "correct": correct,
        "incorrect": incorrect
    }), 200


if __name__ == '__main__':
    app.run(port=5002, debug=True)

