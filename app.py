from flask import Flask, render_template, request, redirect, flash, url_for
from database_connection import *
from check import *
from verification import *
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
    email = False
    username = False
    password = False
    register = False
    if request.method == "POST":
        if not check_email(email_entry):
            email = "this is not an email"
            print("not email") #debug
        elif check_user_data("email", "email", email_entry):
            email = "email exist"
            print("email exist") #debug
        else:
            email = False
            print("everything is alright") #debug
            
        if check_user_data("username", "username", username_entry):
            username = "username exist"
            print("username exist") #debug
        elif "@" in username_entry:
            username = "username cannot contain @"
            
        if not check_password(password_entry):
            password = "password dont meet requirement"
            print("password dont meet requirement") #debug
        elif password_entry != password_confirm:
            password = "password dont match"
            print("password dont match") #debug
        
        print(f"{email} + {username} + {password}")
        if  (email is not False) or (username is not False) or (password is not False):
            print("requirement dont pass") #debug
        else:
            try:
                query = """INSERT INTO User (email, username, password)
    VALUES (?, ?, ?);"""
                value = (email_entry, username_entry, hash(password_entry))
                insert_data(query, value)
                register = True
                print("insert successful")
            except sqlite3.IntegrityError:
                print("fail to insert data") #debug
    
    if register:
        send_email(sender_email, sender_email_password, email_entry, "test")
    
    return render_template("sign_up.html", title = "sign up", email = email, username = username, password = password)

@app.route("/login", methods=["GET", "POST"])
def login():
    username_entry = request.form.get("email")
    password_entry = request.form.get("password")
    if request.method == "POST":
        try:
            query = ""
            check_user_data()
        except sqlite3.IntegrityError:
            pass
    
    return render_template("login.html", title = "login")

if __name__ == "__main__":
    app.run(debug = True)