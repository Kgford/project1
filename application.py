import os
import csv
import requests 
import sys
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    #print("now = ",now)
    timestamp = datetime.now()
    print("timestamp = ",timestamp)
    print("RowCount2 = ",db.execute("SELECT * FROM users WHERE name = :username AND password = :password",
    {"username":request.form.get("username"),"password":request.form.get("password")}).rowcount)
    if request.method == "POST":
        if db.execute("SELECT * FROM users WHERE name = :username AND password = :password",
        {"username":request.form.get("username"),"password":request.form.get("password")}).rowcount == 0:
            return redirect(url_for('signup'))
        else:
            db.execute("UPDATE users SET last_login = :last_login WHERE name = :username AND password = :password",
            {"last_login":timestamp, "username": request.form.get("username"), "password": request.form.get("password")})
            session['current_user'] = request.form.get("username")
            session['username'] = request.form.get("username")
            session['password'] = request.form.get("password")
            session['email'] = request.form.get("email")
			session['user_id'] = db.execute("SELECT * FROM users WHERE name = :name", {"name": request.form.get("username")}).fetchone()
            return redirect(url_for('books'))
        return render_template ("index.html",index_type="SIGNIN",UserN="User Name",PassW="Password")
    return render_template ("index.html",index_type="SIGNIN",UserN="User Name",PassW="Password")
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        timestamp = datetime.now()
        if db.execute("SELECT * FROM users WHERE name = :username AND password = :password",{"username":request.form.get("username"),"password":request.form.get("password")}).rowcount == 0:
			# Create new user
            db.execute("INSERT INTO users (name, password, email,created_on,last_login) VALUES (:username, :password, :email, :created_on, :last_login)",
					    {"username": request.form.get("username"), "password": request.form.get("password"), "email": request.form.get("email"), "created_on": timestamp, "last_login": timestamp})
            db.commit()
            session['current_user'] = request.form.get("username")
            session['username'] = request.form.get("username")
            session['password'] = request.form.get("password")
            session['email'] = request.form.get("email")
			session['user_id'] = db.execute("SELECT * FROM users WHERE name = :name", {"name": request.form.get("username")}).fetchone()
            return redirect(url_for('index'))
        return render_template ("signup.html",index_type="SIGNUP",UserN="User Name",PassW="Password")
    return render_template ("signup.html",index_type="SIGNUP",UserN="User Name",PassW="Password")
 
@app.route('/logout')
def logout():
   # remove the user from the session if it is there
   session.pop('current_user', None)
   session.pop('username', None)
   session.pop('password', None)
   session.pop('email', None)
   session.pop('user_id', None)
   return redirect(url_for('index'))
  
 
@app.route("/books")
def books():
    book_list = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", book_list=book_list)

@app.route("/book/<int:book_id>")
def book(book_id):
    """Lists details about a single flight."""
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
        
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    print(book)
    # get book stats from API.
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "UE95aOMmNDw2qGQ8eSZKQ", "isbns": book.isbn})
    myJSON = resp.json()
    return render_template("book.html", myJSON=myJSON)
	
    
	
@app.route("/api/books/<int:book_id>")
def flight_api(book_id):
    """Return details about a single book."""
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
    
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    print(book)
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "UE95aOMmNDw2qGQ8eSZKQ", "isbns": book.isbn})
    myJSON = resp.json()
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
		"isbn": book.isbn,
		"isbn13": myJSON.books[0].isbn13,
		"ratings_count": myJSON.books[0].ratings_count,
		"reviews_count": myJSON.books[0].reviews_count,
		"text_reviews_count": myJSON.books[0].text_reviews_count,
		"work_ratings_count": myJSON.books[0].work_ratings_count,
		"work_reviews_count": myJSON.books[0].work_reviews_count,
		"work_text_reviews_count": myJSON.books[0].work_text_reviews_count,
		"average_rating": myJSON.books[0].average_rating,
        "average_score": myJSON.books[0].average_score"
	}) 