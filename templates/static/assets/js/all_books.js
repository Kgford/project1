/* globals Chart:false, feather:false */

(window.onload = function () {
   'use strict'
    const selection = "";
	const inputVal = "";
	alert("all books =  " + inputVal);
	socket.emit('submit search',selection,inputVal);

    // When a  Updat
    socket.on('get booklist', book_list => {
		for (active_book in book_list) { 
			var link1 = document.createElement('a');
			link1.href = url_for('book', book_id=active_book);
			link1.innerHTML = active_book.isbn;
			document.querySelector('#isbn').innerHTML = active_book.isbn;
			
			var link2 = document.createElement('a');
			link2.href = url_for('book', book_id=active_book);
			link2.innerHTML = active_book.title;
			document.querySelector('#title').innerHTML = active_book.title;
			
			var link3 = document.createElement('a');
			link3.href = url_for('book', book_id=active_book);
			link3.innerHTML = active_book.author;
			document.querySelector('#author').innerHTML = active_book.author;
			
			var link4 = document.createElement('a');
			link4.href = url_for('book', book_id=active_book);
			link4.innerHTML = active_book.year;
			document.querySelector('#isbn').innerHTML = active_book.year;
		}
		
    });
});
