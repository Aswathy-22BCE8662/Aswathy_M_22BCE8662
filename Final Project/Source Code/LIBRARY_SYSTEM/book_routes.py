# book_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import mongo # Assuming extensions are imported correctly
from bson.objectid import ObjectId

book_bp = Blueprint("book", __name__)

@book_bp.route("/dashboard")
@login_required # Requires user to be logged in to access this route
def dashboard():
    # Fetch all books from the database
    books = mongo.db.books.find()
    # Pass books and current_user object to the template
    return render_template("dashboard.html", books=books, user=current_user)

@book_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_book():
    # Only librarians can add books
    if not current_user.is_admin():
        flash("You are not authorized to add books.", "danger")
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        # Insert new book details into the database
        mongo.db.books.insert_one({
            "title": request.form["title"],
            "author": request.form["author"],
            "category": request.form.get("category", ""), # Use .get() for optional fields
            "year": request.form.get("year", ""),
            "cover": request.form.get("cover", "")
        })
        flash("Book added successfully!", "success")
        return redirect(url_for("book.dashboard"))
    return render_template("add_book.html")

@book_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_book(id):
    # Only librarians can edit books
    if not current_user.is_admin():
        flash("You are not authorized to edit books.", "danger")
        return redirect(url_for("book.dashboard"))

    # Find the book by its ObjectId
    book = mongo.db.books.find_one({"_id": ObjectId(id)})
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for("book.dashboard"))

    if request.method == "POST":
        # Update book details in the database
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
    # Render edit form with existing book data
    return render_template("edit_book.html", book=book)

@book_bp.route("/delete/<id>")
@login_required
def delete_book(id):
    # Only librarians can delete books
    if not current_user.is_admin():
        flash("You are not authorized to delete books.", "danger")
        return redirect(url_for("book.dashboard"))

    # Delete the book by its ObjectId
    mongo.db.books.delete_one({"_id": ObjectId(id)})
    flash("Book deleted successfully!", "success")
    return redirect(url_for("book.dashboard"))

# Optional: A separate page to view all books (e.g., for students without dashboard actions)
@book_bp.route("/books")
# Removed @login_required here to allow conditional check for redirection in the route logic
def books_collection():
    # If user is not authenticated, redirect them to the login page immediately
    if not current_user.is_authenticated:
        flash("Please log in to view the book collection.", "warning")
        return redirect(url_for('auth.login'))

    books = mongo.db.books.find()
    return render_template("books.html", books=books, user=current_user) # Pass user for conditional display
