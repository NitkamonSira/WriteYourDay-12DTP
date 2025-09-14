from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from database_connection import *
from check import *
from verification import *
from datetime import datetime
app = Flask(__name__)
app.secret_key = "dfolkxghnvofdlknv"


@app.route("/")
def home():
    return render_template("home.html", title = "home")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    email_entry = request.form.get("email")
    username_entry = request.form.get("username")
    password_entry = request.form.get("password")
    password_confirm = request.form.get("confirm_password")

    email = False
    username = False
    password = False
    register = False
    now = datetime.now().strftime("%Y%m%d%H%M")
    
    if request.method == "POST":
        if not check_email(email_entry):
            email = "this is not an email"

        elif check_user_data("email", "email", email_entry):
            email = "email exist"

        else:
            email = False

        if check_user_data("username", "username", username_entry):
            username = "username exist"
        elif "@" in username_entry:
            username = "username cannot contain @"
            
        if not check_password(password_entry):
            password = "password dont meet requirement"
        elif password_entry != password_confirm:
            password = "password dont match"

        if (email is not False) or (username is not False) or (password is not False):
            print("requirement dont pass")  # debug
        else:
            try:
                query = """INSERT INTO User (email, username, password, time, verification_code)
    VALUES (?, ?, ?, ?, ?);"""
                password_hash = convert_password(password_entry)
                code = verification_code(6)
                value = (email_entry, username_entry, password_hash, now, code)
                insert_data(query, value)
                register = True
                print("insert successful")
            except sqlite3.IntegrityError:
                print("fail to insert data")  # debug
    
    if register:
        query1 = f"SELECT id FROM User WHERE email = '{email_entry}'"
        session["id"] = get_data_from_database(query1)[0][0]
        send_email(email_password, email_entry, code, username_entry)
        return redirect(url_for("verify_page"))
    
    return render_template("sign_up.html",
                           title="sign up",
                           email=email,
                           username=username,
                           password=password)

@app.route("/verify", methods=["GET", "POST"])
def verify_page():
    code = request.form.get("code")
    id = session.get("id")
    email = get_data_from_database(f"SELECT email FROM User WHERE id = {id}")[0][0]
    query = f"SELECT verification_code FROM User WHERE email = '{email}'"
    verify = False
    if request.method == "POST":
        confirm = get_data_from_database(query)
        if code == confirm[0][0]:
            update_query = f"""UPDATE User
SET is_verified = 1
WHERE email = '{email}'"""
            insert_data(update_query)
            return redirect(url_for("main"))
        else:
            verify = True

    return render_template("verify.html",
                           title="Verify your account",
                           verify=verify,
                           email=email)


@app.route("/login", methods=["GET", "POST"])
def login():
    username_entry = request.form.get("email")
    password_entry = request.form.get("password")

    require = False
    if request.method == "POST":
        password_hash = convert_password(password_entry)
        username_check = len(username_entry.split("@"))

        if username_check == 1:
            require = "username"
        elif username_check == 2:
            require = "email"

        if len(username_entry.split()) > 1:
            require = True

        if require is not False:
            try:
                if check_user_data(require, "password", password_hash):
                    if get_data_from_database(f"SELECT is_verified FROM User WHERE {require} = '{username_entry}'")[0][0] == 0:

                        return redirect(url_for("verify_page"))
                    else:
                        query = f"SELECT id FROM User WHERE {require} = '{username_entry}'"
                        session["id"] = get_data_from_database(query)[0][0]
                        return redirect(url_for("main"))
                else:
                    require = True
            except sqlite3.IntegrityError:
                require = True

    return render_template("login.html",
                           title="login",
                           require=require)


@app.route("/diary/<int:id>", methods=["GET", "POST"])
def diary(id):
    current_id = session.get("id")
    if current_id is None:
        abort(401)
        
    diary_id = id
    save_button = request.form.get("save")
    query1 = f"""SELECT topic, info, rate FROM Entry WHERE id = {id}"""
    content = get_data_from_database(query1)[0]
    if request.method == "POST":
        title = request.form.get("diary_title")
        rate = request.form.get("rate")
        diary = request.form.get("diary")
        if save_button == "save":
            try:
                now = datetime.now().strftime("%Y%m%d%H%M%S")
                query = f"""UPDATE Entry
SET topic = ?, info = ?, rate = ?, last_open = ?, last_modified = ?
WHERE id = {id};"""
                params = (title, diary, rate, now, now)
                insert_data(query, params)
                return redirect(url_for('diary', id=diary_id))
            except sqlite3.IntegrityError:
                flash("fail to save your entry")
        
        try:
            query2 = f"""UPDATE Entry
SET last_open = {datetime.now().strftime("%Y%m%d%H%M%S")}
WHERE id = {id};"""
            insert_data(query2)
        except sqlite3.IntegrityError:
            pass
        return redirect(url_for("main"))
    return render_template("diary.html",
                           title="diary",
                           current_id=current_id,
                           topic=content[0],
                           info=content[1],
                           rate=content[2],
                           id=id)


@app.route("/main", methods=["GET", "POST"])
def main():
    id = session.get("id")
    print(id)
    if id is None:
        abort(401)
    user_query = f"SELECT username FROM User WHERE id = {id}"
    current_user = get_data_from_database(user_query)[0][0]
    diary_list_query = f"""SELECT id, topic, last_open FROM Entry WHERE id IN(
SELECT entry_id FROM UserEntry WHERE user_id = {id})
ORDER BY last_open DESC
"""
    diary_list = get_data_from_database(diary_list_query)
    if request.method == "POST":
        current_date = datetime.now().strftime("%Y%m%d%H%M%S")
        query = """INSERT INTO Entry (year, month, date, last_open, last_modified)
VALUES (?, ?, ?, ?, ?);"""
        params = (current_date[0:4],
                  current_date[4:6],
                  current_date[6:8],
                  current_date,
                  current_date)
        diary_id = insert_data(query, params)
        query2 = """INSERT INTO UserEntry (user_id, entry_id)
VALUES (?, ?);"""
        params2 = (id, diary_id)
        insert_data(query2, params2)
        return redirect(url_for("diary", id=diary_id))

    return render_template("main.html",
                           user=current_user,
                           diary_list=diary_list)


@app.route("/diary-archieve/<int:year>")
def diary_year(year):
    
    return render_template("year_month.html", year = year)


@app.route("/diary-archieve/<int:year>/<int:month>")
def diary_month(year, month):
    
    query = """SELECT id, year, month, date, topic FROM Entry 
WHERE id IN (SELECT entry_id FROM UserEntry 
WHERE user_id = (SELECT id FROM User WHERE username = ? OR email = ?)) AND year = ? AND month = ?
ORDER BY month"""
    diary_list = get_data_from_database(query)
    return render_template("diary_archieve.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")


@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.html")


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html")


if __name__ == "__main__":
    app.run(debug=True)
