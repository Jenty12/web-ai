import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, session
from image_ai import generate_image
from video_ai import generate_video

app = Flask(__name__)
app.secret_key = "secretkey"

users = {}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")

        return "Sai tài khoản"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        users[request.form["username"]] = request.form["password"]
        return redirect("/")

    return render_template("register.html")


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