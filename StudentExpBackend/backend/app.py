from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# ✅ CREATE APP FIRST
app = Flask(__name__)  
CORS(app)

# ✅ DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gopi@123",
    database="StudentEXPTraker"
)

cursor = db.cursor(dictionary=True)

# ✅ HOME ROUTE
@app.route("/")
def home():
    return "Student Expense Tracker Backend is running"

# 🔐 LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    cursor.execute(
        "SELECT student_id FROM students WHERE email=%s AND password=%s",
        (data["email"], data["password"])
    )
    user = cursor.fetchone()
    if user:
        return jsonify(user)
    return {"error": "Invalid credentials"}, 401

#Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    cursor.execute(
        "INSERT INTO students (name, email, password) VALUES (%s,%s,%s)",
        (data["name"], data["email"], data["password"])
    )
    db.commit()
    return {"message": "Signup successful"}


# ➕ ADD EXPENSE
@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.json
    cursor.execute(
        """INSERT INTO expenses 
        (student_id, expenses_date, amount, category, discription)
        VALUES (%s,%s,%s,%s,%s)""",
        (
            data["student_id"],
            data["date"],
            data["amount"],
            data["category"],
            data["description"]
        )
    )
    db.commit()
    return {"message": "Expense added successfully"}

# # 📊 VIEW EXPENSES
# @app.route("/expenses/<int:student_id>", methods=["GET"])
# def get_expenses(student_id):
#     cursor.execute(
#         "SELECT * FROM expenses WHERE student_id=%s",
#         (student_id,)
#     )
#     return jsonify(cursor.fetchall())

#show expenses
@app.route("/expenses/<int:student_id>", methods=["GET"])
def get_expenses(student_id):
    cursor.execute(
        "SELECT * FROM expenses WHERE student_id=%s",
        (student_id,)
    )
    return jsonify(cursor.fetchall())


# ✅ RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)
