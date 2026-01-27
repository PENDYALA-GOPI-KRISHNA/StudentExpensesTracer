from flask import Flask, request, redirect
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
    port=os.environ.get("DB_PORT")
)

cursor = db.cursor(dictionary=True)

@app.route("/")
def home():
    return "Flask backend running on Render 🚀"

@app.route("/enroll", methods=["POST"])
def enroll():
    data = request.get_json()
    cursor.execute(
        "INSERT INTO students (name, email, course) VALUES (%s,%s,%s)",
        (data["name"], data["email"], data["course"])
    )
    db.commit()
    return {"message": "Student enrolled"}

@app.route("/students")
def students():
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

@app.route("/delete/<int:id>")
def delete(id):
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return {"message": "Deleted"}

if __name__ == "__main__":
    app.run()
