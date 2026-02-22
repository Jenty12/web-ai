import os
import sqlite3
from flask import Flask, render_template, request, redirect, session
from image_ai import generate_image
from video_ai import generate_video

app = Flask(__name__)
app.secret_key = "secretkey"

def get_db():
    return sqlite3.connect("users.db")

with get_db() as db:
    db.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cur = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()

        if user:
            session["user"] = username
            return redirect("/intro")   # ✅ animation trước dashboard
        else:
            return "Sai tài khoản hoặc mật khẩu"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )
            db.commit()
            return redirect("/")
        except:
            return "Username đã tồn tại"

    return render_template("register.html")


# ✅ Trang animation trung gian
@app.route("/intro")
def intro():
    if "user" not in session:
        return redirect("/")
    return render_template("intro.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    result = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        mode = request.form["mode"]

        if mode == "image":
            result = generate_image(prompt)
        else:
            result = generate_video(prompt)

    return render_template("dashboard.html", result=result)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    os.makedirs("static/outputs", exist_ok=True)
    app.run(port=5000, debug=True)