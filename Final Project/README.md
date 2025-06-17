Flask Library Management System
This is a basic web application for managing a library's book collection, built with Flask. It includes user authentication with different roles (Librarian and Student).

## How to Run This Application

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository

First, clone this GitHub repository. Make sure to navigate into the `source_code` directory after cloning:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/source_code
```
*(Remember to replace `your-username` and `your-repo-name` with your actual GitHub username and repository name.)*

### 2. Set Up a Python Virtual Environment

It's best practice to use a virtual environment. From within the `source_code` directory:

```bash
python -m venv venv
```

**Activate the virtual environment:**
* **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
* **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 3. Install Dependencies

With your virtual environment activated, install the necessary Python libraries:

```bash
pip install Flask Flask-PyMongo Flask-Bcrypt Flask-Login
```

### 4. MongoDB Setup

This application requires a MongoDB database.
* Ensure you have MongoDB installed and running on your machine.
* The application expects MongoDB to be accessible at `mongodb://localhost:27017/`.
* The database `library_db` and its collections will be created automatically upon first use (e.g., when you register a user or add a book).

### 5. Prepare Static Files

Make sure your `static` folder contains the necessary `css` and `images` subfolders with their respective files:

```
source_code/
├── static/
│   ├── css/
│   │   └── styles.css
│   └── images/
│       ├── library_banner.jpg  # Main website banner
│       ├── your_book_cover1.jpg # Example book cover
│       └── your_book_cover2.png # Another example book cover
└── ...
```
* `styles.css` should be in `static/css/`.
* Your main website banner image (e.g., `library_banner.jpg`) and all book cover images should be in `static/images/`.

### 6. Run the Application

Once all the above steps are complete and your virtual environment is active, run the Flask application from the `source_code` directory:

```bash
python app.py
```

You can then access the application in your web browser, typically at:
* `http://127.0.0.1:5000/` (will redirect to the login page)
* Or directly: `http://127.0.0.1:5000/login` or `http://127.0.0.1:5000/register`

---
