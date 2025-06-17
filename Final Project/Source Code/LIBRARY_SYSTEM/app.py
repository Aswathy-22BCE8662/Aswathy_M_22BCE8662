# app.py
from flask import Flask, redirect, url_for # Import redirect and url_for
from extensions import mongo, bcrypt, login_manager
from models import User
from bson.objectid import ObjectId

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key" # Replace with a strong, secret key in production

    # Config
    app.config["MONGO_URI"] = "mongodb://localhost:27017/library_db"

    # Init extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" # Route name for the login page

    # Blueprints
    from auth import auth_bp
    from book_routes import book_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)

    # Login loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Load user from MongoDB by ID
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user_data) if user_data else None

    # --- New: Default route to redirect to login ---
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # Run in debug mode for development
