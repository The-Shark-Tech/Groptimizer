import os
from flask import Flask, flash, redirect, render_template, request, session
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient, InsertOne
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRETKEY")

client = MongoClient(os.getenv("MONGODB_KEY"))
db = client["Groptimizer"]
register_collection = db["Register"]

@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        return render_template("home.html")

@app.route("/cart", methods=["GET","POST"])
def cart():
    if request.method == "POST":
        return render_template('cart.html')
    else:
        if session.get('logged_in') is not True:
            flash('Login To Access Cart')
            return render_template("home.html")
        else:
            return render_template('cart.html')

@app.route("/store", methods=["GET","POST"])
def store():
    if request.method == "POST":
        return render_template('store.html')
    else:
        if session.get('logged_in') is not True:
            flash('Login To Access Store Details')
            return render_template("home.html")
        else:
            return render_template('store.html')

@app.route("/browse", methods=["GET","POST"])
def browse():
    if request.method == "POST":
        return render_template('browse.html')
    else:
        if session.get('logged_in') is not True:
            flash('Login To Browse Stores')
            return render_template("home.html")
        else:
            return render_template('browse.html')

@app.route("/track", methods=["GET"])
def track():
    if request.method == "POST":
        return render_template('order-details.html')
    else:
        if session.get('logged_in') is not True:
            flash('Login To Access Tracking Details')
            return render_template("home.html")
        else:
            return render_template('order-details.html')

@app.route("/dashboard-b", methods=["GET","POST"])
def dashboard_b():
    if session['option'] == "Food Bank":
        if request.method == 'POST':
            return render_template('dashboard-bank.html') 
        else:
            if session.get('logged_in') is True:
                return render_template('dashboard-bank.html')
            else:
                flash("Login To Access")
                return render_template('login.html')
    else:
        flash("Login To Access")
        return render_template('login.html')
        
@app.route("/dashboard-s", methods=["GET","POST"])
def dashboard_s():
    if session['option'] == "Groccery Store":
        if request.method == 'POST':
            return render_template('dashboard-store.html') 
        else:
            if session.get('logged_in') is True:
                return render_template('dashboard-store.html')
            else:
                flash("Login To Access")
                return render_template('login.html')
    else:
        flash("Login To Access")
        return render_template('login.html')

@app.route("/login", methods=["GET","POST"])
def login():
    session.pop('username', None)
    if request.method == "POST":

        option = request.form['options']
        username = request.form.get("username")
        password = request.form.get("password")

        if len(list(register_collection.find({"username": username, "option": option}))) == 0:
            flash('User does not exist','error')
            return render_template('login.html')

        for user_record in register_collection.find({"username": username, "option":option}):
            if check_password_hash(user_record['password'], password):
                if option == 'Groccery Store':
                    session["username"] = username
                    session['logged_in'] = True
                    session['option'] = request.form.get("options")
                    flash("Logged-In Successfully",'success')
                    return render_template("dashboard-store.html")
                else:
                    session["username"] = username
                    session['logged_in'] = True
                    session['option'] = request.form.get("options")
                    flash("Logged-In Successfully",'success')
                    return render_template("dashboard-bank.html")
            else:
                flash('Invalid Password','error')
                return render_template('login.html')
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('options', None)
    session.pop('logged_in', None)
    return redirect('/')
    

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":

        option = request.form['options']
        name = request.form.get("name")
        address = request.form.get("address")
        username = request.form.get("username")
        email = request.form.get("email")
        phno = request.form.get("phno")
        website = request.form.get("website")
        password = request.form.get("password")

        user = {
            "option": option,
            "name": name,
            "address": address,
            "username": username,
            "email": email,
            "phno": phno,
            "website": website,
            "password": generate_password_hash(password)
        }

        register_collection.insert_one(user)
        
        if option == 'Groccery Store':
            session["username"] = username
            session['logged_in'] = True
            session['option'] = request.form.get("options")
            flash('Registered Successfully', 'success')
            return render_template("dashboard-store.html")
        else:
            session["username"] = username
            session['logged_in'] = True
            session['option'] = request.form.get("options")
            flash('Registered Successfully', 'success')
            return render_template("dashboard-bank.html")

    else:
        return render_template("register.html")
    