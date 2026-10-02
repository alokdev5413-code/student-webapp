from flask import Flask, render_template, request, redirect
import pyodbc
import os

app = Flask(__name__)

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.environ['DB_SERVER']};"
        f"DATABASE={os.environ['DB_NAME']};"
        f"UID={os.environ['DB_USER']};"
        f"PWD={os.environ['DB_PASSWORD']};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]

        cursor.execute(
            "INSERT INTO Students (Name, Email, Mobile) VALUES (?, ?, ?)",
            name, email, mobile
        )
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT Id, Name, Email, Mobile FROM Students ORDER BY Id DESC")
    students = cursor.fetchall()
    conn.close()

    return render_template("index.html", students=students)

if __name__ == "__main__":
    app.run()
