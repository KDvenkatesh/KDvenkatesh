import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)    
app.secret_key = os.urandom(24)  

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="46Varalakshmi",
        database="student",
        autocommit=True  
    )
    cursor = db.cursor()
except mysql.connector.Error as e:
    print(f"Database connection error: {e}")
    exit(1) 

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        cursor.execute("SELECT * FROM login_table WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            flash(f"Login successful for {email}!", "success")
            return render_template("frontend1.html")
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("login")) 
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("Full_name") 
        email = request.form.get("email")
        password = request.form.get("password")

        if not full_name or not email or not password:
            flash("Full Name, Email, and Password are required!", "warning")
            return redirect(url_for("register"))
        try:
            query = "INSERT INTO login_table (Full_name, email, password) VALUES (%s, %s, %s)"
            values = (full_name, email, password)
            cursor.execute(query, values) 
            db.commit()  

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

        except mysql.connector.IntegrityError:  
            flash("This email is already registered!", "danger")  
        except mysql.connector.Error as e:
            flash(f"MySQL Error: {e}", "danger")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
