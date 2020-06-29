/* globals Chart:false, feather:false */
(window.onload = function () {   
'use strict'    
var title = "This is a test"    
var chart = new CanvasJS.Chart("reviewChart", {	
	animationEnabled: true,		title:{		text: " Rating Details"	},	
	axisX:{interval: 1	},	
	data: [{type: "bar",	
		name: "Rating Details",		
		axisYType: "secondary",		
		color: "#014D65",		
		dataPoints: [{ y: 100, label: "ratings_count" },
		{ y: 50, label: "reviews_count" },
		{ y: 65, label: "text_reviews_count" },
		{ y: 4, label: "work_ratings_count" },
		{ y: 6, label: "work_reviews_count" },	
		{ y: 110, label: "work_text_reviews_count" },
		{ y: 49, label: "average_rating" },
		{ y: 38, label: "average_score" }		
		]	
	}]
});
chart.render();
}) 