from flask import Flask, render_template, request
from database_connection import *
from check import *
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", title = "home")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    email_entry = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    print(email_entry)
    print(username)
    print(password)
    if not check_email(email_entry):
        email = False
    elif not check_user_data("email", "email", email_entry):
        email = False
    else:
        email = True
    
    return render_template("sign_up.html", title = "sign up", email = email)

if __name__ == "__main__":
    app.run(debug = True)