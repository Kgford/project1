d(window.onload = function () {
    document.addEventListener('DOMContentLoaded', () => {
		alert("i am here")
		const selection = "";
		const get_id = document.getElementById("bookvar").value
		const book_id = parseInt(get_id.match(/\d+/),10)
				
		const request = new XMLHttpRequest();
		request.open('POST', '/all_reviews');
		
		// Callback function for when request is completed
		request.onload = () =>{
		var res = JSON.parse(request.responseText)
		indata = JSON.stringify(res)
		_book = JSON.parse(indata)
		success = JSON.stringify(_book["success"])
		
		indata = JSON.stringify(res)
		_book = JSON.parse(indata)
		sucess = JSON.stringify(_book["success"])
		// Update the result div
		if (success) {
			// Load the entire review_list
			var num = 0;
			var a = "" ;
			for (active_review in res.reviews) { 
				id = res.reviews[0].id
				reviewer = res.reviews[0].reviewer
				review_date = res.reviews[0].review_date
				review = res.reviews[0].review
				var tr1 = document.getElementById('reviews')
				var newline1 = document.createElement('p');
				var textnode1 = `Reviewer: ${reviewer}`
				//alert(textnode);
				var node1 = document.createTextNode(textnode1);
				tr1.appendChild(node1);
				
				var tr2 = document.getElementById('reviews')
				var newline2 = document.createElement('p');
				var textnode2 = `         Review Date: ${review_date}`
				//alert(textnode);
				var node2 = document.createTextNode(textnode2);
				tr2.appendChild(node2);
				
				var tr3 = document.getElementById('reviews')
				var newline3 = document.createElement('p');
				var textnode3 = `         Review: ${review}`
				//alert(textnode);
				var node3 = document.createTextNode(textnode3);
				tr3.appendChild(node3);
				num++;			
			}
		}
		// Add data to send with request
		const data = new FormData();
		data.append("book_id", book_id);
		
		// Send request
		request.send(data);
		return false;
		};
	});
});