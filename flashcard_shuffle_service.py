from flask import Flask, jsonify
import csv
import random

app = Flask(__name__)


# Shuffle/Randomize Flashcards Service
@app.route('/shuffle_flashcards', methods=['POST'])
def shuffle_flashcards():
    flashcards = []
    with open('flashcards.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            flashcards.append(row)

    random.shuffle(flashcards)

    with open('flashcards.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(flashcards)

    return jsonify({'message': "Flashcards shuffled successfully."}), 200


# Example usage
if __name__ == '__main__':
    app.run(port=5004, debug=True)