import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
# postgres://nndlrvbypifbsc:489f961108e3ce19c3b11b35ef3605affcec1777458c458fa231666d6e228cba@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d6841qjeijbslk
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
count = db.execute("SELECT * FROM users WHERE name = :username", {"username": session['username']}).rowcount
print(count)

@app.route('/', methods=['GET', 'POST']) 
def index():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
	if request.methed = "GET"
	    if session.get('current_user') is not None:
		    return render_template ("index.html",index_type="Active User Signin",UserN=session['username'],PassW=session['password'])
        else:
            return render_template ("index.html",index_type="Signin",UserN="User Name",PassW="")
    elif request.methed = "POST"    
		session['current_user'] = request.form.get("username")
		if db.execute("SELECT * FROM users WHERE name = :username", 
		        {"username": request.form.get("username")},
		        "AND password = :password",{"password": request.form.get("password")}).rowcount == 0:
            return render_template ("signup.html")
        db.execute("UPDATE users SET last_login = :last_login",{"last_login":timestamp},
        		 " WHERE name = :username",{"username": request.form.get("username")},
		         "AND password = :password",{"password": request.form.get("password")})
        return redirect(url_for('books'))   
		       
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.methed = "GET":
        return render_template("error.html", message="Please attempt signin first.")
    elif request.methed = "GET":
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        if db.execute("SELECT * FROM users WHERE name = :username",{"username":request.form.get("username")}).rowcount == 0:
			# Create new user
            db.execute("INSERT INTO users (name, password,email,created_on,last_login) VALUES (:username, :password, :email, :created_on, :last_login)",
					    {"username": username, "password": password, "email": email, "created_on": timestamp, "last_login": timestamp})
            db.commit()
            session['current_user'] = request.form.get("username")
            session['username'] = request.form.get("username")
            session['password'] = request.form.get("password")
            session['email'] = request.form.get("email")
            return render_template ("signup.html")
    return redirect(url_for('index'))
   
@app.route("/books")
def books():
    book = db.execute("SELECT * FROM books").fetchall()
    return render_template("books.html", book=book)
	
	
@app.route('/logout')
def logout():
   # remove the user from the session if it is there
   session.pop('current_user', None)
   session.pop('username', None)
   session.pop('password', None)
   session.pop('email', None)
   return redirect(url_for('index'))
 
"""
@app.route("/api/books/<int:book_id>")
def flight_api(book_id):
    """Return details about a single book."""

    # Make sure flight exists.
    book = Flight.query.get(flight_id)
    if book is None:
        return jsonify({"error": "Invalid book_id"}), 422

    # Get all passengers.
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
            "origin": flight.origin,
            "destination": flight.destination,
            "duration": flight.duration,
            "passengers": names
        }) 
"""