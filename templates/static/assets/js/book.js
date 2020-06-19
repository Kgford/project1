document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure buttons
    socket.on('connect', () => {

        // Each button should emit a "submit vote" event
        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
				const selection = button.dataset.search;
				alert(`selection =  ${selection}`);
				const inputVal = document.getElementById(`tx_${selection}`).value;
				alert(`inputBal =  ${inputVal}`);
				socket.emit('submit search',selection,inputVal);
            };
		});
    });

    // When a  Updat
    socket.on('get booklist', book_list => {
		for (active_book in book_list) { 
		    var link1 = document.createElement('a');
			document.querySelector('#isbn').innerHTML = active_book.isbn;
			link1.href = url_for('book', book_id=active_book.id);			
			link1.innerHTML = active_book.isbn;
			
            var link2 = document.createElement('a');
			document.querySelector('#title').innerHTML = active_book.title;
			link2.href = url_for('book', book_id=active_book.id);
			link2.innerHTML = active_book.title;
			
			var link3 = document.createElement('a');
			document.querySelector('#author').innerHTML = active_book.author;
			link3.href = url_for('book', book_id=active_book.id);
			link3.innerHTML = active_book.author}
			
			var link4 = document.createElement('a');
			document.querySelector('#isbn').innerHTML = active_book.year;
			link4.href = url_for('book', book_id=active_book.id);
			link4.innerHTML = active_book.year;
			
			 // Stop form from submitting
            return false;
		
    });
});
