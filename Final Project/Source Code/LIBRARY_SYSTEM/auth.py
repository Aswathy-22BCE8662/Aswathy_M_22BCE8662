# auth.py
from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user # Import current_user
from extensions import mongo, bcrypt # Assuming extensions are imported correctly
from models import User # Assuming User model is imported correctly

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # If a user is already logged in, redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        role = request.form["role"]

        # Check if email already exists
        if mongo.db.users.find_one({"email": email}):
            flash("Email already exists. Please choose a different one or login.", "danger")
            return redirect(url_for("auth.register"))

        # Insert new user into the database
        mongo.db.users.insert_one({"email": email, "password": password, "role": role})
        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If a user is already logged in, redirect them to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_data = mongo.db.users.find_one({"email": email})

        # Validate user credentials
        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(user_data)
            login_user(user) # Log the user in
            flash("Logged in successfully!", "success")
            # Redirect to the dashboard after successful login
            return redirect(url_for("book.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required # Requires user to be logged in to access this route
def logout():
    logout_user() # Log the user out
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login")) # Redirect to login page after logout
