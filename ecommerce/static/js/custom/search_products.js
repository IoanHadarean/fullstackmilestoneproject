// Get HTML elements
var searchInput = document.getElementById('search_box');
var searchResults = document.getElementById('search-results-products');
var navbar = document.getElementsByClassName('navbar-dark')[0];
var searchTypeAhead = document.getElementById('search-typeahead');


// Add event listeners
searchInput.addEventListener('keyup', getProductResults);

// Function for retrieving the csrftoken cookie
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function getProductResults() {
    let xhr = new XMLHttpRequest();

    // Unbind event listener before new AJAX call
    searchInput.removeEventListener('keyup', getProductResults);

    var searchRequest = null;
    // Abort old pending requests
    if (searchRequest) {
        searchRequest.abort();
    }

    // Get the search text from the search input
    let searchText = searchInput.value;

    // Clear the search results
    searchResults.innerHTML = '';


    // Remove search typeahead border after results are cleared
    searchTypeAhead.style.border = 'none';

    if (searchText) {
        xhr.onload = function() {
            if (this.readyState == 4 && this.status == 200) {
                let results = JSON.parse(xhr.responseText);

                // Clear the search results
                if (searchResults) {
                    searchResults.innerHTML = '';
                }

                // Colors
                var white = '#ffffff';
                var black = '#000000';
                var rockBlue = '#929fba';


                // Modify the search ul background Color to white
                searchResults.style.backgroundColor = white;

                // Loop through the list of dictionaries
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {

                        // Get title and slug from list of dictionaries
                        let title = Object.keys(results[i]);
                        let slug = Object.values(results[i]);

                        // Create the li element
                        let li = document.createElement('li');
                        li.style.paddingTop = '0.5rem';
                        li.style.paddingBottom = '0.5rem';
                        li.style.paddingLeft = '0.625rem';
                        li.style.marginRight = '0.625rem';
                        li.style.overflow = 'hidden';
                        li.setAttribute('id', slug);

                        // Create link for search result product
                        let linkTag = document.createElement('a');
                        linkTag.href = "/shoppingcart/product/" + slug;
                        linkTag.style.color = black;
                        linkTag.style.display = 'block';

                        // Change the border of search typeahead
                        searchTypeAhead.style.border = '0.0625rem grey solid';
                        searchTypeAhead.style.borderTop = '0';

                        // Add mouse enter and mouse out event listeners for li and link
                        li.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = rockBlue;
                            linkTag.style.color = 'white';
                        });

                        li.addEventListener('mouseout', function() {
                            li.style.backgroundColor = white;
                            linkTag.style.color = black;
                        });

                        linkTag.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = rockBlue;
                            linkTag.style.color = white;
                        });

                        linkTag.addEventListener('mouseout', function() {
                            li.style.backgroundColor = white;
                            linkTag.style.color = black;
                        });

                        // Append title as text node to link
                        linkTag.appendChild(document.createTextNode(title));

                        // Append link to li and li to search results
                        li.appendChild(linkTag);
                        searchResults.appendChild(li);
                    }
                }
                else {
                    // Create the li element
                    let li = document.createElement('li');
                    li.style.paddingTop = '0.5rem';
                    li.style.paddingBottom = '0.5rem';
                    li.style.paddingLeft = '0.625rem';
                    li.style.marginRight = '0.625rem';
                    li.style.overflow = 'hidden';
                    li.innerHTML = searchText;

                    // Change the border of search typeahead
                    searchTypeAhead.style.border = '0.0625rem grey solid';
                    searchTypeAhead.style.borderTop = '0';


                    // Add mouse enter and mouse out event listeners for li
                    li.addEventListener('mouseenter', function() {
                        li.style.backgroundColor = rockBlue;
                    });

                    li.addEventListener('mouseout', function() {
                        li.style.backgroundColor = white;
                    });

                    // Append li to search results
                    searchResults.appendChild(li);
                }

                // Remove navbar margin bottom bootstrap class
                navbar.classList.remove('mb-5');
            }
        };
    }
    xhr.onerror = function() {
        console.log('Request error...');
    };
    xhr.open("POST", "/shoppingcart/products_results/" + searchText + "/", true);
    // Assign the csrftoken to a variable so it can be used in the AJAX
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
}


// Performed debouncing to avoid unnecessary requests on keyup
var debounceTimeout = null;

searchInput.addEventListener('keyup', function(event) {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(getProductResults, 100);
});
