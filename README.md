# Project 1
Web Programming with Python and JavaScript
Project1 submission demonstrates Python Flask with sqlalchemy and javascript

index.html - 	Login Page. It searches the User table for an active user using username and password. If it cannot find you it redirects to signup.
		Timestamp: 0:00:15

signup.html -	New User Page. It adds a new user to the User table  using username, password, and email. After success, it redirect back to login.
		Timestamp: 0:00:15		

books.html - 	Main Page. Loads on successful login. Timestamp: 0:00:39 This page will search the table books by isbn, author, and title using the LIKE feature. 
		Timestamp: 0:01:01 When you click on a Table Row, it will redirect to book.html.Timestamp: 0:01:38  It has a logout link that will unload the session username. 
		If you try to manually load Books.html, you will get an error and you must login again. Timestamp: 0:02:21 

book.html	Selected Book Page. Highlights the selected book featuring a chart with goodreads api information. Timestamp: 0:01:24 There is also a link to redirect to
		the project api /api/books/7. Timestamp: 0:01:45  From here you can add a local review by clicking the button.Timestamp: 0:01:50 

review.html	Local Review Page. From here you can add your own review that is saved on the review database table.

		
