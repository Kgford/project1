document.addEventListener('DOMContentLoaded', () => {
	
	document.querySelectorAll('button').forEach(button => {
		button.onclick = () => {
			const selection = button.dataset.search;
			const inputVal = document.getElementById(`tx_${selection}`).value;
			const request = new XMLHttpRequest();
			request.open('POST', '/searchbook');
			
			// Callback function for when request is completed
			request.onload = () =>{
				const res = JSON.parse(request.responseText)
				indata = JSON.stringify(res)
				_book = JSON.parse(indata)
				sucs = JSON.stringify(_book["success"])
				sucs = JSON.parse(sucs)
				alert(sucs)
				_book = JSON.stringify(_book["book_list"])
				_book = JSON.parse(_book)
				alert(_book)
							
				
				// Update the result div
				if (sucs) {
					// Load the entire booklist
					for (active_book in _book) { 
					    alert(active_book)
						var a1 = document.createElement('a');
						a1.href = url_for('book', book_id=_book.id);
						var node1 = document.createTextNode(_book.isbn);
						a1.appendChild(node1);
						var element1 = document.getElementById("b_isbn");
						element1.appendChild(a1);
						
						var a2 = document.createElement('a');
						a2.href = url_for('book', book_id=_book.id);
						var node2 = document.createTextNode(_book.title);
						a2.appendChild(node2);
						var element2 = document.getElementById("b_title");
						element2.appendChild(a2);
						
						var a3 = document.createElement('a');
						a3.href = url_for('book', book_id=_book.id);
						var node3 = document.createTextNode(_book.author);
						a3.appendChild(node3);
						var element3 = document.getElementById("b_author");
						element3.appendChild(a3);
						
						var a4 = document.createElement('a');
						a4.href = url_for('book', book_id=_book.id);
						var node4 = document.createTextNode(_book.year);
						a4.appendChild(node4);
						var element4 = document.getElementById("b_year");
						element4.appendChild(a4);		
					}
				}
			}	
			// Add data to send with request
			const data = new FormData();
			data.append("inputVal", inputVal);
			data.append('selection', selection);
			// Send request
			request.send(data);
			return false;
		}
	});
});