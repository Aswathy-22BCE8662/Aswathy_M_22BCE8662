# book_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import mongo
from bson.objectid import ObjectId

book_bp = Blueprint("book", __name__)

@book_bp.route("/dashboard")
@login_required 
def dashboard():

    books = mongo.db.books.find()
    return render_template("dashboard.html", books=books, user=current_user)

@book_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_book():

    if not current_user.is_admin():
        flash("You are not authorized to add books.", "danger")
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        mongo.db.books.insert_one({
            "title": request.form["title"],
            "author": request.form["author"],
            "category": request.form.get("category", ""),
            "year": request.form.get("year", ""),
            "cover": request.form.get("cover", "")
        })
        flash("Book added successfully!", "success")
        return redirect(url_for("book.dashboard"))
    return render_template("add_book.html")

@book_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_book(id):
    if not current_user.is_admin():
        flash("You are not authorized to edit books.", "danger")
        return redirect(url_for("book.dashboard"))

    book = mongo.db.books.find_one({"_id": ObjectId(id)})
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":

        mongo.db.books.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "title": request.form["title"],
                "author": request.form["author"],
                "category": request.form.get("category", ""),
                "year": request.form.get("year", ""),
                "cover": request.form.get("cover", "")
            }}
        )
        flash("Book updated successfully!", "success")
        return redirect(url_for("book.dashboard"))

    return render_template("edit_book.html", book=book)

@book_bp.route("/delete/<id>")
@login_required
def delete_book(id):

    if not current_user.is_admin():
        flash("You are not authorized to delete books.", "danger")
        return redirect(url_for("book.dashboard"))

    mongo.db.books.delete_one({"_id": ObjectId(id)})
    flash("Book deleted successfully!", "success")
    return redirect(url_for("book.dashboard"))


@book_bp.route("/books")

def books_collection():
    if not current_user.is_authenticated:
        flash("Please log in to view the book collection.", "warning")
        return redirect(url_for('auth.login'))

    books = mongo.db.books.find()
    return render_template("books.html", books=books, user=current_user)
