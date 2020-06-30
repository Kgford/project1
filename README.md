# Project 1
Web Programming with Python and JavaScript
Project1 submission demonstrates Python Flask with sqlalchemy and javascript

index.html - 	Login Page. It searches the User table for an active user using username and password. If it cannot find you it redirects to signup.

signup.html -	New User Page. It adds a new user to the User table  using username, password, and email. After success, it redirect back to login.

books.html - 	Main Page. Loads on successful login. This page will search the table books by isbn, author, and title using the LIKE feature. 
		When you click on a Table Row, it will redirect to book.html. It has a logout link that will unload the session username. 
		If you try to manually load Books.html, you will get an error and you must login again. 

book.html	Selected Book Page. Highlights the selected book featuring a chart with goodreads api information. There is also a link to redirect to
		the project api /api/books/7. From here you can add a local review by clicking the button.

review.html	Local Review Page. From here you can add your own review that is saved on the review database table.

		
