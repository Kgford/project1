import os
import csv
import requests 
import json
import sys
import ast
#from models import *
from itertools import chain
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, jsonify, make_response
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.secret_key = "OCML3BRawWEUeaxcuKHLpw"
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)
book_list = {"reviewer": "","review_date": "", "review": "","review_date": ""}

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv("DATABASE_URL")
#db2 = SQLAlchemy(app)
#db2.create_all()
#db2.session.commit()


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
    row_headers = db.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'books'").fetchall()
    row_header = [item for sublist in row_headers for item in sublist]
    res = to_json(book_list,row_header)
    books = json.loads(res)
    return render_template("books.html", book_list=books)

@app.route("/book/<int:book_id>")
def book(book_id):
    """Lists details about a single book."""
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
    
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    
	# get book stats from goodreads API.
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1utQKMYrlMKe3YJxQoXyeg", "isbns": book.isbn})
    if resp.status_code !=200:
        return jsonify({"error": "Goodreads no longer supports this book"}), 422
    
    myJSON = resp.json()
    myDICT = myJSON["books"]
    if db.execute("SELECT * FROM reviews WHERE books_id = :books_id", {"books_id": book.id}).rowcount == 0:
        review = 'No Review'
        reviewer = 'No Review'
    else:
        reviews = db.execute("SELECT * FROM reviews WHERE books_id = :books_id", {"books_id": book.id}).fetchone()
        review=reviews.review
        reviewer=reviews.reviewer
    print(book)    
    return render_template("book.html", myDICT=myDICT, book=book, review=review, reviewer=reviewer)
 	
@app.route("/stats", methods=["POST"])
def stats():
    print('test')
    book_id = request.form['book_id']
    #print(isbn)
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
    
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    
    # get book stats from goodreads API.
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1utQKMYrlMKe3YJxQoXyeg", "isbns": book.isbn})
    success = True
    if resp.status_code !=200:
        success = False
    
    myJSON = resp.json()
    myDICT = myJSON["books"]
    print(myDICT)
    return jsonify({"success": success, "myDICT": myDICT})
    
@app.route("/searchbook", methods=["POST"])
def search():
    json_data = []
    row_header = []
    select = request.form['selection']
    input = request.form['inputVal']
        
    # Search for books on the database. onload will have a input =="" and load everything	
    if input != "":
        book_list = db.execute("SELECT * FROM books").fetchall()
    else: 
        #book_list = db.execute("SELECT * FROM books WHERE select: LIKE input:", {"select":select,"input":input+"%"}).fetchall()
        book_list = db.execute("SELECT * FROM books WHERE 'isbn%' LIKE '3%'").fetchall()
    # Make sure request succeeded
    #if db.execute("SELECT * FROM books WHERE :select LIKE input:", {"select":select,"input":input+"%"}).rowcount == 0:
       #book_list = db.execute("SELECT * FROM books WHERE 'isbn%' LIKE '123%'").fetchall()
    
    row_headers = db.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'books'").fetchall()
    row_header = [item for sublist in row_headers for item in sublist]
    res = to_json(book_list,row_header)
    books = json.loads(res)
    return jsonify({"success": True, "book_list": books})
    
@app.route("/review/<int:book_id>")
def review(book_id):
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
    
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    return render_template("review.html", book=book)
	
@app.route("/reviews", methods=["POST"])
def reviews():
    now = datetime.now()
    timestamp = datetime.now()
    """add review to a single book."""
    book = request.form['book']
    review = request.form['review']
	
    success = True
	# Get a count of existing reviews
    count = db.execute("SELECT * FROM reviews WHERE books_id = :books_id", {"books_id": book_id}).fetchall()
    print('count = ',count)
	
    db.execute("INSERT INTO reviews (reviewer, review_date, review,books_id) VALUES (:reviewer, :review_date, :review, :books_id)",
    {"reviewer": session.get('username'), "review_date":timestamp, "author": book.author, "review": review, "books_id": book_id})
     
    # Check for a new review
    if db.execute("SELECT * FROM reviews WHERE books_id = :books_id", 
			{"books_id": book_id}).rowcount()<=count:
        success = False
	# Get all reviews
    reviews = db.execute("SELECT * FROM reviews WHERE books_id = :books_id",
                            {"books_id": book_id}).fetchall()  
                            
    row_headers = db.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'reviews'").fetchall()
    row_header = [item for sublist in row_headers for item in sublist]
    res = to_json(reviews,row_header)
    rev = json.loads(res)
    return jsonify({"success": success, "reviews": rev}) 
	
@app.route("/api/books/<int:book_id>")
def book_api(book_id):
    """Return details about a single book."""
    if db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).rowcount == 0:
        return jsonify({"error": "Invalid book_id"}), 422
    
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1utQKMYrlMKe3YJxQoXyeg", "isbns": book.isbn})
    myJSON = resp.json()
    print(myJSON)
    myDICT = myJSON["books"]
    b = myDICT[0]
    print("b = ",b["ratings_count"])
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
		"isbn": book.isbn,
		"isbn13": myDICT[0]["isbn13"],
		"ratings_count": myDICT[0]["ratings_count"],
		"reviews_count": myDICT[0]["reviews_count"],
		"text_reviews_count": myDICT[0]["text_reviews_count"],
		"work_ratings_count": myDICT[0]["work_ratings_count"],
		"work_reviews_count": myDICT[0]["work_reviews_count"],
		"work_text_reviews_count": myDICT[0]["work_text_reviews_count"],
		"average_rating": myDICT[0]["average_rating"]
    }) 
    
def to_json(lst,columns):
    keys = []
    columns[0] = str(columns[0])
    for d in lst:
       keys.append(dict(zip(columns,d)))
   
    data = json.dumps(keys)
    return data
    

def dec_serializer(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
	