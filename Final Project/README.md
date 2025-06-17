Flask Library Management System
A basic web application for managing library books and user authentication.

---

## How to Run Locally

1.  **Navigate to the project directory:**
    ```bash
    cd your-repo-name/source_code
    ```
    *(Replace `your-repo-name` with your actual repository name.)*

2.  **Activate Pipenv shell:**
    ```bash
    pipenv shell
    ```
    *(If you don't have Pipenv, install it first: `pip install pipenv`)*

3.  **Install dependencies:**
    ```bash
    pipenv install flask flask-pymongo flask-bcrypt flask-login
    ```

4.  **Ensure MongoDB is running** on `mongodb://localhost:27017/`.

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```

6.  **Access in browser:** Go to `http://127.0.0.1:5000/`
