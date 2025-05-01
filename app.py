from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", title = "home")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
       email = request.form.get("email")
       return "email: " + email
    return render_template("sign_up.html")

if __name__ == "__main__":
    app.run(debug = True)