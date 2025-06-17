# auth.py
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user 
from extensions import mongo, bcrypt 
from models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        role = request.form["role"]

        if mongo.db.users.find_one({"email": email}):
            flash("Email already exists. Please choose a different one or login.", "danger")
            return redirect(url_for("auth.register"))

        mongo.db.users.insert_one({"email": email, "password": password, "role": role})
        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_data = mongo.db.users.find_one({"email": email})

        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user) 
            flash("Logged in successfully!", "success")

            return redirect(url_for("book.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required 
def logout():
    logout_user() 
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login")) 
