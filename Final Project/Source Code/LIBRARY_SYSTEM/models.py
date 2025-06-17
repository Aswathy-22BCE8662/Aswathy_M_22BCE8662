# models.py
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        """
        Initializes a User object from MongoDB user data.
        The _id from MongoDB is converted to a string for Flask-Login compatibility.
        """
        self.id = str(user_data["_id"])
        self.email = user_data["email"]

        self.role = user_data.get("role", "student")

    def is_admin(self):
        """
        Checks if the user has the 'librarian' role.
        """
        return self.role == "librarian"
