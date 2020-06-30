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
				document.getElementById('table_id').innerHTML = "";
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
						var tr = document.createElement("tr");
						var row=document.getElementById('table_id').insertRow()
						var cell1 = row.insertCell(0)
						var cell2 = row.insertCell(1)
						var cell3 = row.insertCell(2)
						var cell4 = row.insertCell(3)
						pathArray = window.location.href;
						pathArray = pathArray.substring(0, pathArray.lastIndexOf("/"));
						url = `${pathArray}/book/${book_id}`
						//alert(url)
						// Create the text node for anchor element. 
						cell1.innerHTML = `<a href=${url}>${isbn}</a>`;
						cell2.innerHTML = `<a href=${url}>${author}</a>`;
						cell3.innerHTML = `<a href=${url}>${title}</a>`;
						cell4.innerHTML = `<a href=${url}>${year}</a>`;
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