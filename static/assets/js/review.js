document.addEventListener('DOMContentLoaded', () => {
	document.querySelectorAll('button').forEach(button => {
		button.onclick = () => {
			alert("i am here in js")
			const get_id = document.getElementById("bookvar").value
			const book_id = parseInt(get_id.match(/\d+/),10)
			const get_review = document.getElementById("text").value;
			const request = new XMLHttpRequest();
			request.open('POST', '/reviews');
			
			// Callback function for when request is completed
			request.onload = () =>{
			var res = JSON.parse(request.responseText)
			alert(res.reviews[0].id)
			alert(res.reviews[0].reviewer)
			alert(res.reviews[0].review_date)
			alert(res.reviews[0].review)
			indata = JSON.stringify(res)
			_book = JSON.parse(indata)
			sucess = JSON.stringify(_book["success"])
			alert(success)
			alert(res.reviews[0].title);
			alert(res.reviews[0].review)
			// Update the result div
			if (success) {
				// Load the entire review_list
				for (active_review in review_list) { 
					var para1 = document.createElement('p');
					var node1 = document.createTextNode(`Reviewer: &{res.reviews[0]reviewer}`);
					para1.appendChild(node1);
					var element1 = document.getElementById("reviews");
					element1.appendChild(para1);
					
					var para2 = document.createElement('p');
					var node2 = document.createTextNode(`Review Date: &{res.reviews[0].review_date}`);
					para2.appendChild(node2);
					var element2 = document.getElementById("reviews");
					element2.appendChild(para2);
					
					var para3 = document.createElement('p');
					var node3 = document.createTextNode(`Review: &{res.reviews[0].review}`);
					para.appendChild(node3);
					var element3 = document.getElementById("reviews");
					element3.appendChild(para3);	
					//space
					var para4 = document.createElement('p');
					var node4 = document.createTextNode("");
					para4.appendChild(node4);
					var element4 = document.getElementById("reviews");
					element4.appendChild(para);	
				}
			};
		};	
		// Add data to send with request
		const data = new FormData();
		data.append("book_id", book_id);
		data.append("review", get_review);
		
		// Send request
		request.send(data);
		return false;
		};
	});
});