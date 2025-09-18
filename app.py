from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from database_connection import get_data_from_database, update_data, check_user_data
from check import check_email, check_password, convert_password
from verification import send_email, verification_code
from datetime import datetime
import sqlite3
app = Flask(__name__)
app.secret_key = "Your Secret key"  # replace this with your secret key
DATABASE = "diary.db"
SERVER = "smtp.gmail.com"
PORT = 587
SENDER_EMAIL = "Your email address"  # replace this with your email address
email_password = "Your email app password"  # replace this with your app password


@app.route("/")
def home():
    return render_template("home.html", title="home")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    # redirect to main if already login
    if session.get("id") is not None:
        return redirect(url_for("main"))
    # get entry from html page
    email_entry = request.form.get("email")
    username_entry = request.form.get("username")
    password_entry = request.form.get("password")
    password_confirm = request.form.get("confirm_password")

    # validation to link with html page
    email = False
    username = False
    password = False
    register = False
    now = datetime.now().strftime("%Y%m%d%H%M")
    if request.method == "POST":
        # email validation
        if email_entry == "":  # blank entry
            email = "Please enter your email."
        elif not check_email(email_entry):  # basic email check
            email = "This is not an email!"
        elif check_user_data("email", "email", email_entry):
            # check that email is exist in database
            email = "This email is already exist."
        else:
            email = False
        # username validation
        if username_entry == "":  # blank entry
            username = "Please enter your username."
        elif check_user_data("username", "username", username_entry):
            # check that username is exist in database
            username = "This username is already exist."
        elif "@" in username_entry:
            # prevent issue when login
            username = "Username cannot contain @"
        elif " " in username_entry:
            # prevent issue when login
            username = "Username cannot contain white space"
        # password validation
        if not check_password(password_entry):
            password = "Your password is not passing the requirement."
        elif password_entry != password_confirm:
            password = "Your password is not matching."

        if (email is False) and (username is False) and (password is False):
            # ensure that entry pass all criteria
            # insert data to database
            try:
                query = """INSERT INTO User (email, username, password, time, verification_code)
VALUES (?, ?, ?, ?, ?);"""
                # hash password for secure storing
                password_hash = convert_password(password_entry)
                code = verification_code(6)  # for verification process
                value = (email_entry, username_entry, password_hash, now, code)
                update_data(query, value)  # insert date into database
                register = True  # link with verification process
            except sqlite3.IntegrityError:
                abort(404)  # take users to 404 page
    # take user to email verification process
    if register:
        query1 = f"SELECT id FROM User WHERE email = '{email_entry}'"
        # get the user id from User table to use in other page of website
        session["id"] = get_data_from_database(query1)[0][0]
        # send verification email
        send_email(email_password, email_entry, code, username_entry)
        # take user to verification page
        return redirect(url_for("verify_page"))

    return render_template("sign_up.html",
                           title="sign up",
                           email=email,
                           username=username,
                           password=password,)


@app.route("/verify", methods=["GET", "POST"])
def verify_page():
    code = request.form.get("code")  # get users code from html
    # get users verification code from database
    id = session.get("id")  # get id that stored in session
    email = get_data_from_database(f"SELECT email FROM User WHERE id = {id}")[0][0]
    verify = False  # for html display
    if request.method == "POST":
        query = f"SELECT verification_code FROM User WHERE email = '{email}'"
        confirm = get_data_from_database(query)  # get verification code from DB
        # checking that code that user entry match what in database
        if code == confirm[0][0]:
            update_query = f"""UPDATE User
SET is_verified = 1
WHERE email = '{email}'"""
            update_data(update_query)  # update DB
            return redirect(url_for("main"))
        else:
            verify = True  # for html display

    return render_template("verify.html",
                           title="Verify your account",
                           verify=verify,
                           email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    # redirect to main if already login
    if session.get("id") is not None:
        return redirect(url_for("main"))
    # get user entry from html
    username_entry = request.form.get("email")
    password_entry = request.form.get("password")

    require = False  # filtering and html display
    if request.method == "POST":
        password_hash = convert_password(password_entry)
        if username_entry == "" or password_entry == "":  # blank entry
            require = True  # for html display
        # checking that user entry is username or email
        username_check = len(username_entry.split("@"))
        if username_check == 1:
            require = "username"
        elif username_check == 2:
            require = "email"
        # ensure that there is no white space
        if len(username_entry.split()) > 1:
            require = True  # for html display

        if require is not False:
            try:
                # compare username or email with password in database
                if check_user_data(require, "password", password_hash):
                    # ensure that user already verify their account
                    query2 = f"""SELECT is_verified FROM User
WHERE {require} = '{username_entry}'"""
                    if get_data_from_database(query2)[0][0] == 0:
                        return redirect(url_for("verify_page"))
                    else:
                        query = f"""SELECT id FROM User
WHERE {require} = '{username_entry}'"""
                        session["id"] = get_data_from_database(query)[0][0]
                        return redirect(url_for("main"))
                else:
                    require = True  # for html display
            except sqlite3.IntegrityError or sqlite3.OperationalError:
                require = True  # for html display

    return render_template("login.html",
                           title="login",
                           require=require)


@app.route("/diary/<int:id>", methods=["GET", "POST"])
def diary(id):
    current_id = session.get("id")  # get user id that stored in session
    # ensure that user is login
    if current_id is None:
        abort(401)
    diary_id = id
    # prevent open the diary that doesn't exist
    query4 = f"SELECT id FROM Entry WHERE id = {diary_id}"
    diary_exist = get_data_from_database(query4)
    if diary_exist == []:
        abort(404)
    # prevent user from open other diary
    query3 = f"""SELECT user_id FROM UserEntry WHERE entry_id = {diary_id}"""
    if current_id != get_data_from_database(query3)[0][0]:
        abort(404)
    # get button value
    save_button = request.form.get("save")
    delete_button = request.form.get("delete")
    # get the default/saved diary entry
    query1 = f"""SELECT topic, info, rate, year, month, date FROM Entry
WHERE id = {id}"""
    content = get_data_from_database(query1)[0]
    # link with html textarea
    if content[1] is None:
        info = ""
    else:
        info = content[1]
    # formatting date
    date = f"{content[5]}/{content[4]}/{content[3]}"
    if request.method == "POST":
        # get entry from html
        title = request.form.get("diary_title")
        rate = request.form.get("rate")
        diary = request.form.get("diary")
        # when save button was clicked
        if save_button == "save":
            try:
                # save entry into diary
                now = datetime.now().strftime("%Y%m%d%H%M%S")
                query = f"""UPDATE Entry
SET topic = ?, info = ?, rate = ?, last_open = ?, last_modified = ?
WHERE id = {id};"""
                params = (title, diary, rate, now, str(now))
                update_data(query, params)
                return redirect(url_for('diary', id=diary_id))  # reload page
            except sqlite3.IntegrityError:
                flash("fail to save your entry")
        # when delete button was clicked
        if delete_button == "delete":
            try:
                # delete data in linking table
                query_delete1 = f"""DELETE FROM UserEntry
WHERE entry_id = {diary_id}"""
                update_data(query_delete1)
                # delete data in Entry table
                query_delete2 = f"""DELETE FROM Entry
WHERE id = {diary_id}"""
                update_data(query_delete2)
                return redirect(url_for("main"))  # take user back to /main
            except Exception:
                # take user to 404 in case of any error happened
                abort(404)
        # when user clicked exit button
        try:
            # update Entry table to help sorting in /main
            query2 = f"""UPDATE Entry
SET last_open = {datetime.now().strftime("%Y%m%d%H%M%S")}
WHERE id = {id};"""
            update_data(query2)
        except sqlite3.IntegrityError:
            # take user to 404 in case of any error happened
            abort(404)
        return redirect(url_for("main"))  # take user to /main
    return render_template("diary.html",
                           title="diary",
                           current_id=current_id,
                           topic=content[0],
                           info=info,
                           rate=content[2],
                           date=date,
                           id=id)


@app.route("/main", methods=["GET", "POST"])
def main():
    id = session.get("id")  # get user id that stored in session
    # abort 401 if user is not login
    if id is None:
        abort(401)
    # getting current user username to show on html
    user_query = f"SELECT username FROM User WHERE id = {id}"
    current_user = get_data_from_database(user_query)[0][0]
    # getting all diary that user have sorting by the time that last open
    # the diary that recently view will come first
    diary_list_query = f"""SELECT id, topic, last_modified, year, month, date
FROM Entry WHERE id IN(
SELECT entry_id FROM UserEntry WHERE user_id = {id})
ORDER BY last_open DESC
"""
    diary_list = get_data_from_database(diary_list_query)
    num_diary = len(diary_list)
    # get button value
    logout_button = request.form.get("logout")
    if request.method == "POST":
        # log user out when user clicked the log out button
        if logout_button == "logout":
            session["id"] = None  # clear session
            return redirect(url_for("home"))  # take user to the home page
        
        # when '+ new' button is clicked
        # create new diary in Entry table and insert keys into UserEntry table
        current_date = datetime.now().strftime("%Y%m%d%H%M%S")
        query = """INSERT INTO Entry (year, month, date, last_open, last_modified)
VALUES (?, ?, ?, ?, ?);"""
        params = (current_date[0:4],
                  current_date[4:6],
                  current_date[6:8],
                  current_date,
                  str(current_date))
        diary_id = update_data(query, params)
        query2 = """INSERT INTO UserEntry (user_id, entry_id)
VALUES (?, ?);"""
        params2 = (id, diary_id)
        update_data(query2, params2)
        # take user to the diary that created
        return redirect(url_for("diary", id=diary_id))

    return render_template("main.html",
                           title="Main",
                           user=current_user,
                           diary_list=diary_list,
                           num_diary=num_diary,
                           login=True)


@app.errorhandler(404)
def not_found(e):
    # custom 404
    return render_template("404.html")


@app.errorhandler(500)
def server_error(e):
    # custom 500
    return render_template("500.html")


@app.errorhandler(401)
def unauthorized(e):
    # custom 401
    return render_template("401.html")


if __name__ == "__main__":
    app.run(debug=True)
