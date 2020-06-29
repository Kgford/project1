
(window.onload = function () {
    document.addEventListener('DOMContentLoaded', () => {
		const selection = "";
		const inputVal = "";
		const request = new XMLHttpRequest();
		request.open('POST', '/searchbook');
		
		// Callback function for when request is completed
		request.onload = () =>{
			var res = JSON.parse(request.responseText)
			indata = JSON.stringify(res)
			_book = JSON.parse(indata)
			sucess = JSON.stringify(_book["success"])
				
			// Update the result div
			if (sucess) {
				// Load the entire booklist
				var num = 0;
				for (active_book in res.book_list) { 
					alert(res.book_list[num].title);
					var a1 = document.createElement('a');
					alert('al = ',a1);
					//a1.href = url_for('book', book_id=res.book_list[num].id);
					var node1 = document.createTextNode(res.book_list[num].isbn);
					alert('nodal = ',nodel);
					a1.appendChild(node1);
					var element1 = document.getElementById("b_isbn");
					element1.appendChild(a1);
					alert('elementl = ',element1)
					
					var a2 = document.createElement('a');
					//a2.href = url_for('book', book_id=res.book_list[num].id);
					var node2 = document.createTextNode(res.book_list[num].title);
					a2.appendChild(node2);
					var element2 = document.getElementById("b_title");
					element2.appendChild(a2);
					
					var a3 = document.createElement('a');
					//a3.href = url_for('book', book_id=res.book_list[num].id);
					var node3 = document.createTextNode(res.book_list[num].author);
					a3.appendChild(node3);
					var element3 = document.getElementById("b_author");
					element3.appendChild(a3);
					
					var a4 = document.createElement('a');
					//a4.href = url_for('book', book_id=res.book_list[num].id);
					var node4 = document.createTextNode(res.book_list[num].year);
					a4.appendChild(node4);
					var element4 = document.getElementById("b_year");
					element4.appendChild(a4);	
					num++;						
				}
			}
		};	
    });
});