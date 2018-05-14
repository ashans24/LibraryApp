var response = $('#bookListData').data()['other'];

console.log(response);

// Search container rendering
var searchContainer = document.getElementById('searchContainer');

while (searchContainer.firstChild){
	searchContainer.removeChild(searchContainer.firstChild);
}

var totalResultsNum = response["total-results"];
var startResultsNum = response["results-start"];
var endResultsNum = response["results-end"];

console.log("Search container entered");

var divNode = document.createElement("DIV");
divNode.className="results-data";

var totalResultsNode = document.createElement("P");
var totalResultsText = document.createTextNode('The total results are: '+totalResultsNum);
totalResultsNode.appendChild(totalResultsText);
divNode.appendChild(totalResultsNode);

var startResultsNode = document.createElement("P");
var startResultsText = document.createTextNode('Start results: '+startResultsNum);
startResultsNode.appendChild(startResultsText);
divNode.appendChild(startResultsNode);

var endResultsNode = document.createElement("P");
var endResultsText = document.createTextNode('end results: '+endResultsNum);
endResultsNode.appendChild(endResultsText);
divNode.appendChild(endResultsNode);

searchContainer.appendChild(divNode);

var bookListContainer = document.getElementById('bookDataList');

while (bookListContainer.firstChild){
	bookListContainer.removeChild(bookListContainer.firstChild);
}

$.each(response['results']['work'], function() {
	console.log(this['best_book']);

	var listEl = document.createElement("LI");
	listEl.className ="book-details";

	var imageDiv = document.createElement("DIV");
	imageDiv.className = "data-section image";

	var coverImg = document.createElement("IMG");
	coverImg.className = "book-cover";
	coverImg.src = this['best_book']['image_url'];
	if (coverImg.alt != null) coverImg.alt = this['best_book']['title'];

	imageDiv.appendChild(coverImg);
	listEl.appendChild(imageDiv);

	var dataDiv = document.createElement("DIV");
	dataDiv.className = "data-section bookinfo";

	var bksmmary = document.createElement("DIV");
	bksmmary.className = "book-summary";

	var titleH = document.createElement("H4");
	var titleLink = document.createElement("A");
	titleLink.href = "#";
	var titleString = document.createTextNode(this['best_book']['title']);
	titleLink.appendChild(titleString);
	titleH.appendChild(titleLink);
	bksmmary.appendChild(titleH);

	var authorData = document.createElement("P");
	var authorText = document.createTextNode("Author: " + this['best_book']['author']['name']);
	authorData.appendChild(authorText);

	var ratingsData = document.createElement("P");
	var ratingsText = document.createTextNode("Average Ratings: " + this["average_rating"]);
	ratingsData.appendChild(ratingsText);

	bksmmary.appendChild(authorData);
	bksmmary.appendChild(ratingsData);

	listEl.appendChild(bksmmary);

	bookListContainer.appendChild(listEl);

});

// // Page Number rendering

// angular.forEach(document.querySelectorAll('.page-numbers'), function(divElement) {
// 	var pageNumberDiv = angular.element(divElement);
// 	var numOfResults = totalResultsNum - endResultsNum;

// 	pageNumberDiv.empty();

// 	// Conditional statement that enables next and previous page rendering
// 	if (startResultsNum == 1 && endResultsNum != totalResultsNum) {
// 		// First page with more than 1 pages
// 		pageNumberDiv.append(
// 				'<button ng-click="next()">Next Page</button>'
// 			);
// 	}
// 	else if (startResultsNum != 1) {
// 		// Not the first page
		
// 		if(endResultsNum == totalResultsNum){
// 			// The last page
// 			pageNumberDiv.append(
// 				'<p><button>Previous Page</button></p>'
// 			);
// 		}
// 		else {
// 			// All other pages
// 			pageNumberDiv.append(
// 				'<p><button ng-click="next()">Next Page</button></p>'
// 				+'<p><button>Previous Page</button></p>'
// 			);
// 		}
// 	}
// });

// // Book List rendering
// var bookList = angular.element(document.querySelector('#bookDataList'));
// bookList.empty();

// angular.forEach(response.data["results"]["work"], function(bookDatas, key) {
	
// 	var bookHtml = '<li class="book-details">'
// 		+'<div class="data-section image">' 
// 		+'<img class="book-cover" src="'+ bookDatas["best_book"]["image_url"] + '" alt="'
// 		+ bookDatas["best_book"]["title"] + '" />'
// 		+'</div>'
// 		+'<div class="data-section bookinfo"><div class="book-summary">'//bookinfo 
//         +'<h4><a href="#">' + bookDatas["best_book"]["title"] + '</a></h4>'
//         +'<p>Author: ' + bookDatas["best_book"]["author"]["name"] + '</p>'
//         +'<p>Average ratings: ' + bookDatas["average_rating"] + '</p>'
// 		+'</div></div></li>';


// 	bookList.append(bookHtml);

// });