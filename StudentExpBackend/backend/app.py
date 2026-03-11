from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host="aws-1-ap-southeast-2.pooler.supabase.com",
        database="postgres",
        user="postgres.qvlximgbpsmkschlxefk",
        password="gSGLbWpqS4xUlOhs",
        port=6543,
        sslmode="require"
    )
    return conn


# Test route
@app.route("/")
def home():
    return jsonify({"message": "Flask backend running 🚀"})


# Register
@app.route("/signup", methods=["POST"])
def register():
    try:
        data = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            "INSERT INTO students (name, email, password) VALUES (%s,%s,%s)",
            (data["name"], data["email"], data["password"])
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "User registered successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Get expenses
@app.route("/expenses/<int:student_id>", methods=["GET"])
def get_expenses(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            "SELECT * FROM expenses WHERE student_id=%s ORDER BY expenses_date DESC",
            (student_id,)
        )

        expenses = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(expenses)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add expense
@app.route("/add-expense", methods=["POST"])
def add_expense():
    try:
        data = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            """
            INSERT INTO expenses 
            (student_id, expenses_date, amount, category, description)
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

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Expense saved successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Login
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(
            "SELECT * FROM students WHERE email=%s AND password=%s",
            (data["email"], data["password"])
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return jsonify({"student_id": user["student_id"]})
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)