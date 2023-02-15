import os,sqlite3
from flask import Flask, render_template, session
from flask_session import Session
import re
from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date



app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'super secret key'
DATABASE = 'final-project.db'

db = sqlite3.connect(DATABASE, check_same_thread=False)
Session(app)

@app.route("/")
def index():
    session.clear()
    name = dict(
        {
            "name": "Namkeen",
            "perKG": 200,
            "Quantity": 5
        }
    )
    session["Admin"] = 1
    session["user_id"] = name
    session["cart"] = []
    item = dict({
        "name" : "Namkeen",
        "pricePerKG" : 200,
        "quantity" : 2,
         "discount" : 10,
         "totalPrice" : (200 * 2) - ( 10 * (200 * 2) * 0.01)
    })
    list_item =  session["cart"]
    list_item.append(item)
    session["user_name"] = "Harmeet"
    session["cart"] = list_item
    session["today_date"] = date.today()
    return render_template("index.html")

@app.route("/billGen")
def billGen():
    if request.method == 'POST':
        if request.form["submit_button"] == "Add Item":
            print("Add item")
        elif request.form["submit_button"] == "Edit":
            print("Edit")
        elif request.form["submit_button"] == "Delete":
            print("Delete")
        
    else:
        return render_template("billGen.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html" , errormsg = "must provide username ", code = 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html" , errormsg = "must provide password ", code = 403)

        # Query database for username
        rows = db.execute("SELECT * FROM Credentials WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template( "error.html" , errormsg = "invalid username and/or password", code = 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    Credentials = db.execute("Select * from Credentials")
    if request.method =="POST":
        name = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("confirmpassword")
        if not name:
            return render_template("error.html" , errormsg = "must provide username ", code = 400)

        if not password or password != repassword or not repassword:
            return render_template("error.html" , errormsg = "must provide password ", code = 403)

        Password_pattern = "^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s)).{8,15}$"
        compiled_regEx = re.compile(Password_pattern)
        match = re.search(compiled_regEx, password)
        if not match:
            return render_template("error.html" ,errormsg = "Password between 8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character " , code = 400)


        for user in Credentials:
            if name == user["username"]:
                return render_template("error.html",errormsg = "must provide username", code = 400)

        db.execute("INSERT INTO Credentials (username ,password) VALUES (? ,?)" , name , generate_password_hash(password))

        return redirect("/")

    else:
        return render_template("register.html")