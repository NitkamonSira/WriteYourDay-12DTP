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
    username_entry = request.form.get("username")
    password_entry = request.form.get("password")
    password_confirm = request.form.get("confirm_password")
    print(email_entry) #debug
    print(username_entry) #debug
    print(password_entry) #debug
    email = True
    username = True
    password = True
    if request.method == "POST":
        if not check_email(email_entry):
            email = False
            print("not email") #debug
        elif check_user_data("email", "email", email_entry):
            email = False
            print("email exist") #debug
        else:
            email = True
            print("everything is alright") #debug
            
        if check_user_data("username", "username", username_entry):
            username = False
            print("username exist")
            
        if not check_password(password_entry):
            password = False
            print("password dont meet requirement")
        elif password_entry != password_confirm:
            password = False
            print("password dont match")
    
    
    if request.method == "POST":
        try:
            query = """INSERT INTO Test (email, username, password)
VALUES (?, ?, ?);"""
            value = (email_entry, username_entry, hash(password_entry))
            insert_data(query, value)
        except sqlite3.IntegrityError:
            print("fail to insert data")
    
    return render_template("sign_up.html", title = "sign up", email = email, username = username, password = password)

if __name__ == "__main__":
    app.run(debug = True)