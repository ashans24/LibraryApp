var app = angular.module('bookListSearch', []);



app.config(['$interpolateProvider', function($interpolateProvider)
{
	$interpolateProvider.startSymbol('{a')
	$interpolateProvider.endSymbol('a}')
}]);



app.factory('SearchCache', function() {    
	var pageNumber = 1;
	var submitbtnpress = true;
	var searchString="";

	var submit = function() {
		this.submitbtnpress = true;
		this.searchString="";
	};

	var pageChange = function() {
		this.submitbtnpress = false;
	};

    var next = function() {
        pageNumber = this.pageNumber + 1;
    };

    var previous = function() {
        pageNumber = this.pageNumber - 1;
    };

    var reset = function() {
        pageNumber = 1;
        return pageNumber;
    };

    var setSearchString = function(value){
    	this.searchString = value;
    };

    return {
        pageNumber: pageNumber,
        nextPage: next,
        prevPage: previous,
        reset: reset,

        submitbtnpress: submitbtnpress,
		submit: submit,
		pageChange: pageChange,

		searchString: searchString,
		setSearchString: setSearchString
    };
});



app.controller('searchController', ['$scope', '$http', 'SearchCache', 
	function($scope, $http, SearchCache) {
	
		var pageNumber = SearchCache.reset();
		var submitbtn = SearchCache.submitbtnpress;
		var searchString = SearchCache.searchString;

		$scope.submit = function() {
			SearchCache.submit();
			SearchCache.setSearchString($scope.searchParam.toLowerCase().replace(new RegExp(' ', 'g'), '+'));

			console.log(SearchCache.submitbtnpress);
			$scope.search();
		}

		function next(){
			this.pageNumber = SearchCache.next();

			SearchCache.pageChange();

			console.log(this.pageNumber);
			console.log(this.submitbtn);

			$scope.search();
		}

		$scope.search = function(){
			$scope.submitted=true;

			if ($scope.searchParam){
				console.log("Before check " + this.pageNumber);

				if (SearchCache.submitbtnpress){
					this.pageNumber = SearchCache.reset();
				}
				else {
					this.pageNumber = SearchCache.pageNumber;
				}

				console.log("After check " + this.pageNumber);
				console.log(SearchCache.submitbtnpress);

				var searchParameter = SearchCache.searchString;

				console.log(JSON.stringify(searchParameter));

				$http.post('/searchbooks/' + searchParameter + '/' + this.pageNumber, {
					headers: {
	             		'Content-Type': 'application/json; charset=utf-8'
	        		}
				})
					.then(function(response){

						var totalResultsNum = response.data["total-results"];
						var startResultsNum = response.data["results-start"];
						var endResultsNum = response.data["results-end"];
						
						// Search container rendering
						var searchContainer = angular.element(document.querySelector('#searchContainer'));
						searchContainer.empty();

						var searchHtml = '<div class="results-data"><p>The total results are: '+
							totalResultsNum +'</p><p>Start results: '+
							startResultsNum +'</p><p>End results: '+
							endResultsNum +'</p></div>';

						searchContainer.append(searchHtml);

						// Page Number rendering

						angular.forEach(document.querySelectorAll('.page-numbers'), function(divElement) {
							var pageNumberDiv = angular.element(divElement);
							var numOfResults = totalResultsNum - endResultsNum;

							pageNumberDiv.empty();

							// Conditional statement that enables next and previous page rendering
							if (startResultsNum == 1 && endResultsNum != totalResultsNum) {
								// First page with more than 1 pages
								pageNumberDiv.append(
										'<p><button ng-click="next()">Next Page</button></p>'
									);
							}
							else if (startResultsNum != 1) {
								// Not the first page
								
								if(endResultsNum == totalResultsNum){
									// The last page
									pageNumberDiv.append(
										'<p><button>Previous Page</button></p>'
									);
								}
								else {
									// All other pages
									pageNumberDiv.append(
										'<p><button ng-click="next()">Next Page</button></p>'
										+'<p><button>Previous Page</button></p>'
									);
								}
							}
						});
						
						// Book List rendering
						var bookList = angular.element(document.querySelector('#bookDataList'));
						bookList.empty();

						angular.forEach(response.data["results"]["work"], function(bookDatas, key) {
							
							var bookHtml = '<li class="book-details">'
								+'<div class="data-section image">' 
								+'<img class="book-cover" src="'+ bookDatas["best_book"]["image_url"] + '" alt="'
								+ bookDatas["best_book"]["title"] + '" />'
								+'</div>'
								+'<div class="data-section bookinfo"><div class="book-summary">'//bookinfo 
						        +'<h4><a href="#">' + bookDatas["best_book"]["title"] + '</a></h4>'
						        +'<p>Author: ' + bookDatas["best_book"]["author"]["name"] + '</p>'
						        +'<p>Average ratings: ' + bookDatas["average_rating"] + '</p>'
								+'</div></div></li>';


							bookList.append(bookHtml);

						});
						
					});
			}
		}

	}
]);

// <div class="book-list">
//     <li class="book-details">
//       <div class="image">
//         <a href="/isbn/9780316246279"><img src="https://images-na.ssl-images-amazon.com/images/I/515zOsxnpQL._SL160_.jpg" alt="The Black Prism (Lightbringer)"></a>
//       </div>
//       <div class="bookinfo">
//         <h2><a href="/isbn/9780316246279">The Black Prism (Lightbringer)</a></h2>    
//                   <p>Author: Brent Weeks</p>
       
//         <p>ISBN-13: 9780316246279</p>
//                   <p>ISBN-10: 0316246271</p>
//                   <a class="btn view" href="/isbn/9780316246279">View This Book ›</a>
//         <p class="clear"></p>
//       </div>
//     </li>
// </div>		