from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Це дозволить React отримувати доступ до Flask API

@app.route('/api/data', methods=['GET'])
def get_data():
    db = sqlite3.connect('./student.db')
    cursore = db.cursor()
    data = cursore.execute("SELECT * FROM student").fetchall()
    return jsonify(data)

@app.route('/api/append', methods=['POST'])
def append_data():
    data = request.get_json()
    db = sqlite3.connect('./student.db')
    cursore = db.cursor()
    student = cursore.execute("SELECT * FROM student").fetchall()
    message = ""
    for item in student:
        if data['number'] in item:
            message = f"Учень: {item[1]}, з номером {item[3]} вже є в базі даних"
            break
    if message == "":
        message = "Учень усіпшно добавлений"
        cursore.execute('''
            INSERT INTO student (PIB, Grade, number)
            VALUES (?, ?, ?)
            ''', ( data["student"], data["grade"], data["number"] ))
        db.commit()
    db.close()
    print(data)
    return message

@app.route('/api/day', methods=['POST'])
def calendar():
    months = [
        "january", "february", "march", "april", "may", "june",
        "july", "august", "september", "october", "november", "december"
    ]
    month = request.form.get("month")
    dayN = request.form.get("day")
    day = f"{months[int(month)]}24"
    db = sqlite3.connect('./student.db')
    cursor = db.cursor()
    query = f"SELECT * FROM {day} WHERE day = {dayN}"
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)