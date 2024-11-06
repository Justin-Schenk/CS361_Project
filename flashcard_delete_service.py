from flask import Flask, request, jsonify
import csv

app = Flask(__name__)


# Deletion Service
@app.route('/delete_flashcard', methods=['POST'])
def delete_flashcard():
    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({'error': 'No word provided'}), 400

    updated_flashcards = []
    with open('flashcards.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != word:
                updated_flashcards.append(row)

    with open('flashcards.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_flashcards)

    return jsonify({'message': f"Flashcard with word '{word}' deleted successfully."}), 200


# Example usage
if __name__ == '__main__':
    app.run(port=5003, debug=True)