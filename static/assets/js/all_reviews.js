
(window.onload = function () {
    document.addEventListener('DOMContentLoaded', () => {
		const selection = button.dataset.search;
			const book = document.getElementById("book").value;
			const get_review = document.getElementById("text").value;
			const request = new XMLHttpRequest();
			request.open('POST', '/review');
			
			// Callback function for when request is completed
			request.onload = () =>{
			//const data = JSON.parse(request.responseText)
			const indata = request.responseText
			var data = JSON.parse(indata);
			var review_list = JSON.parse(data.review)
			alert(data.success)
			alert(data.reviews)
			// Update the result div
		if (data.success) {
			// Load the entire booklist
			for (active_book in book_list) { 
				// Load the entire review_list
				for (active_review in review_list) { 
				var para1 = document.createElement('p');
				var node1 = document.createTextNode(`Reviewer: &{active_review.reviewer}`);
				para1.appendChild(node1);
				var element1 = document.getElementById("reviews");
				element1.appendChild(para1);
				
				var para2 = document.createElement('p');
				var node2 = document.createTextNode(`Review Date: &{active_review.review_date}`);
				para2.appendChild(node2);
				var element2 = document.getElementById("reviews");
				element2.appendChild(para2);
				
				var para3 = document.createElement('p');
				var node3 = document.createTextNode(`Review: &{active_review.reviewer}`);
				para.appendChild(node3);
				var element3 = document.getElementById("reviews");
				element3.appendChild(para3);	
				//space
				var para4 = document.createElement('p');
				var node4 = document.createTextNode("");
				para4.appendChild(node4);
				var element4 = document.getElementById("reviews");
				element4.appendChild(para);	
		};
		// Add data to send with request
		const data = new FormData();
		data.append("book", book);
		data.append("review", get_review);
		// Send request
		request.send(data);
		return false;
	});	
});
