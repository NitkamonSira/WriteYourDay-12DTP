from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", title = "home")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    birthday = request.form.get("birthday")
    
    return render_template("sign_up.html", title = "sign up")

if __name__ == "__main__":
    app.run(debug = True)