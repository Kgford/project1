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

@app.route('/', methods=['GET', 'POST'])
def index():
    now = datetime.now()
    #print("now = ",now)
    timestamp = datetime.now()
    print("timestamp = ",timestamp)
    print("RowCount2 = ",db.execute("SELECT * FROM users WHERE name = :username AND password = :password",
    {"username":request.form.get("username"),"password":request.form.get("password")}).rowcount)
    if request.method == "POST":
        if db.execute("SELECT * FROM users WHERE name = :username AND password = :password", {"username":request.form.get("username"),"password":request.form.get("password")}).rowcount == 0:
            return redirect(url_for('signup'))
        else:
            db.execute("UPDATE users SET last_login = :last_login WHERE name = :username AND password = :password",
            {"last_login":timestamp, "username": request.form.get("username"), "password": request.form.get("password")})
            session['current_user'] = request.form.get("username")
            session['username'] = request.form.get("username")
            session['password'] = request.form.get("password")
            session['email'] = request.form.get("email")
            return redirect(url_for('books'))
        return render_template ("index.html",index_type="SIGNIN",UserN="User Name",PassW="Password")
    else:      
        return render_template ("index.html",index_type="SIGNIN",UserN="User Name",PassW="Password")
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template ("signup.html",index_type="SIGNUP",UserN="User Name",PassW="Password")
    elif request.method == "POST":
        timestamp = datetime.now()
        if db.execute("SELECT * FROM users WHERE name = :username AND password = :password",{"username":request.form.get("username"),"password":request.form.get("password")}).rowcount == 0:
			# Create new user
            db.execute("INSERT INTO users (name, password,email,created_on,last_login) VALUES (:username, :password, :email, :created_on, :last_login)",
					    {"username": request.form.get("username"), "password": request.form.get("password"), "email": request.form.get("email"), "created_on": timestamp, "last_login": timestamp})
            db.commit()
            session['current_user'] = request.form.get("username")
            session['username'] = request.form.get("username")
            session['password'] = request.form.get("password")
            session['email'] = request.form.get("email")
            return render_template ("signup.html",index_type="SIGNUP",UserN="User Name",PassW="Password")
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