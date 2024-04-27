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

@app.route("/login", methods=["GET","POST"])
def login():
    session.pop('username', None)
    if request.method == "POST":

        option = request.form['options']
        username = request.form.get("username")
        session['username'] = request.form.get("username")
        password = request.form.get("password")

        if len(list(register_collection.find({"username": username, "option": option}))) == 0:
            flash('User does not exist','error')
            return render_template('login.html')

        for user_record in register_collection.find({"username": username, "option":option}):
            if check_password_hash(user_record['password'], password):
                if option == 'Groccery Store':
                    session["username"] = username
                    flash("Logged-In Successfully",'success')
                    return render_template("dashboard-store.html")
                else:
                    session["username"] = username
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
    return redirect('/')
    

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":

        option = request.form['options']
        name = request.form.get("name")
        address = request.form.get("address")
        username = request.form.get("username")
        session['username'] = request.form.get("username")
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
            flash('Registered Successfully', 'success')
            return render_template("dashboard-store.html")
        else:
            flash('Registered Successfully', 'success')
            return render_template("dashboard-bank.html")

    else:
        return render_template("register.html")
    