from flask import Flask, request
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# ✅ Local MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gopi@123",   # your mysql password
    database="studentexptraker",
    port=3306
)

cursor = db.cursor(dictionary=True)


@app.route("/")
def home():
    return "Flask backend running locally 🚀"


# ✅ Register
@app.route("/signup", methods=["POST"])
def register():
    data = request.get_json()

    cursor.execute(
        "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
        (data["name"], data["email"], data["password"])
    )
    db.commit()

    return {"message": "User registered successfully"}

from flask import jsonify  # Make sure this import is present at the top

# Fetch all expenses for a given student_id
@app.route("/expenses/<int:student_id>", methods=["GET"])
def get_expenses(student_id):
    try:
        cursor.execute(
            "SELECT * FROM expenses WHERE student_id=%s ORDER BY expenses_date DESC",
            (student_id,)
        )
        expenses = cursor.fetchall()
        return jsonify(expenses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add a new expense for a student
@app.route("/add-expense", methods=["POST"])
def add_expense():
    try:
        data = request.get_json()
        cursor.execute(
            """
            INSERT INTO expenses (student_id, expenses_date, amount, category, discription)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                data["student_id"],
                data["date"],
                data["amount"],
                data["category"],
                data["description"]
            )
        )
        db.commit()
        return jsonify({"message": "Expense saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Login (UPDATED TO MATCH YOUR REACT)
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        cursor.execute(
            "SELECT * FROM students WHERE email=%s AND password=%s",
            (data["email"], data["password"])
        )

        user = cursor.fetchone()

        if user:
            return {
                "student_id": user["student_id"]  # ✅ FIXED HERE
            }
        else:
            return {"message": "Invalid credentials"}, 401

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)