import os
import csv
import requests 
import json
import sys
import ast
from itertools import chain
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
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
    return render_template("book.html", myDICT=myDICT, book=book, review=review, reviewer=reviewer)
 	
@app.route("/stats", methods=["POST"])
def stats():
    isbn = request.form['book_isbn']
    # get book stats from goodreads API.
    resp = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "1utQKMYrlMKe3YJxQoXyeg", "isbns": isbn})
    success = True
    if resp.status_code !=200:
        success = False
    
    myJSON = resp.json()
    myDICT = myJSON["books"]
    return jsonify({"success": success, "myDICT": myDICT})
    
@app.route("/searchbook", methods=["POST"])
def search():
    select = request.form['selection']
    print("select = ",select)
    input = request.form['inputVal']
    print("input = ",input)
    
    # Search for books on the database. onload will have a input =="" and load everything	
    if input != "":
        book_list = db.execute("SELECT * FROM books").fetchall()
    else: 
        #book_list = db.execute("SELECT * FROM books WHERE select: LIKE input:", {"select":select,"input":input+"%"}).fetchall()
        book_list = db.execute("SELECT * FROM books WHERE 'isbn%' LIKE '3%'").fetchall()
    # Make sure request succeeded
    #if db.execute("SELECT * FROM books WHERE :select LIKE input:", {"select":select,"input":input+"%"}).rowcount == 0:
       #book_list = db.execute("SELECT * FROM books WHERE 'isbn%' LIKE '123%'").fetchall()
    
    columns = ('index','isbn', 'title','author', 'year')
    active_key = 'books'
    book_list_json  = to_json(book_list,columns,active_key)
    #print(" book_list_json = ",book_list_json)
    test = jsonify({"success": True, "book_list": book_list_json})
    book_list =  test.json()
    
    print(test["book_list"])
    return jsonify({"success": True})
    
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
   
    # create a json
    columns = ('index','reviewer', 'review_date','review', 'year')
    active_key = 'reviews'
    reviews_json = to_json(reviews,columns,active_key)
    return jsonify({"success": success, "reviews": reviews_json}) 
	
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
    
def to_json(list,columns,active_key):
    """
    Jsonify the sql alchemy query result.
    """
    x = 0
    d = dict()
    d1 = dict()
    st = ""
    for active_list in list:
        d[x] = {columns[1]:active_list[1],
        columns[2]:active_list[2],
        columns[3]:active_list[3],
        columns[4]:active_list[4]}
        x +=1
    # this only yealds on result . must fix
    
    for y in range(0, x-1):
        if y==0:
           st += "{" + json.dumps(d[y]) + ","
        else:
            st += json.dumps(d[y]) + ","
    st += json.dumps(d[y]) + "}"	
    
	# don't know which is needed at this point yet string or dict
    #print(st)
    #d1 = json.loads(st)
    #print(dl)
    return st	