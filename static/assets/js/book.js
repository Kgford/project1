document.addEventListener('DOMContentLoaded', () => {
	
	document.querySelectorAll('button').forEach(button => {
		button.onclick = () => {
			const selection = button.dataset.search;
			const inputVal = document.getElementById(`tx_${selection}`).value;
			const request = new XMLHttpRequest();
			request.open('POST', '/searchbook');
			
			// Callback function for when request is completed
			request.onload = () =>{
				var res = JSON.parse(request.responseText)
				indata = JSON.stringify(res)
				_book = JSON.parse(indata)
				sucess = JSON.stringify(_book["success"])
				
	             document.getElementById('b_line').innerHTML = "";
				// Update the result div
				if (sucess) {
					// Load the entire booklist
					var num = 0;
					var a = "" ;
					for (active_book in res.book_list) { 
					    book_id = res.book_list[num].id
						isbn = res.book_list[num].isbn
						author = res.book_list[num].author
						title = res.book_list[num].title
						year = res.book_list[num].year

					    var tr1 = document.getElementById('b_line')
					    var newline1 = document.createElement('a');
						newline1.setAttribute('href', `'url_for('book', book_id=[${book_id}]'`);
						var textnode1 = `ISBN: ${isbn}`
						//alert(textnode);
						var node1 = document.createTextNode(textnode1);
						tr1.appendChild(node1);
						
						var tr2 = document.getElementById('b_line')
					    var newline2 = document.createElement('a');
						newline2.setAttribute('href', `'url_for('book', book_id=[${book_id}]'`);
						var textnode2 = `TITLE: ${title}`
						//alert(textnode);
						var node2 = document.createTextNode(textnode2);
						tr2.appendChild(node2);
						
						var tr3 = document.getElementById('b_line')
					    var newline3 = document.createElement('a');
						newline3.setAttribute('href', `'url_for('book', book_id=[${book_id}]'`);
						var textnode3 = `AUTHOR: ${author}`
						//alert(textnode);
						var node3 = document.createTextNode(textnode3);
						tr3.appendChild(node3);
						
						var tr4 = document.getElementById('b_line')
					    var newline4 = document.createElement('a');
						newline4.setAttribute('href', `'url_for('book', book_id=[${book_id}]'`);
						var textnode4 = `YEAR: ${year}`
						//alert(textnode);
						var node4 = document.createTextNode(textnode4);
						tr4.appendChild(node4);
						num++;						
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