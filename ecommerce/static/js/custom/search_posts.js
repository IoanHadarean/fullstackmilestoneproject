// Get HTML elements
var searchInputPosts = document.getElementById('search_posts');
var searchInputDrafts = document.getElementById('search_drafts');
var searchResultsPosts = document.getElementById('search-results-posts');
var searchResultsDrafts = document.getElementById('search-results-drafts');
var searchTypeAhead = document.getElementById('search-typeahead');

// Colors
var white = '#ffffff';
var royalBlue = '#4285f4';
var black = '#000000';

// Add event listeners
if (searchInputPosts) {
    searchInputPosts.addEventListener('keyup', getPostsResults);
}
if (searchInputDrafts) {
    searchInputDrafts.addEventListener('keyup', getDraftsResults);
}
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


function getPostsResults() {
    let xhr = new XMLHttpRequest();
    var searchRequest = null;
    // Abort old pending requests
    if (searchRequest) {
        searchRequest.abort();
    }

    // Unbind event listener before new AJAX call
    searchInputPosts.removeEventListener('keyup', getPostsResults);

    // Get the search text from the search input
    let searchText = searchInputPosts.value;

    // Clear the search results
    searchResultsPosts.innerHTML = '';

    // Remove search typeahead border after results are cleared
    searchTypeAhead.style.border = 'none';

    if (searchText) {
        xhr.onload = function() {
            if (this.readyState == 4 && this.status == 200) {
                let results = JSON.parse(xhr.responseText);

                // Clear the search results
                if (searchResultsPosts) {
                    searchResultsPosts.innerHTML = '';
                }

                // Modify the search ul background color to white
                searchResultsPosts.style.backgroundColor = white;

                // Loop through the list of dictionaries
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {

                        // Get title and slug from list of dictionaries
                        let title = Object.keys(results[i]);
                        let pk = Object.values(results[i]);

                        // Create the li element
                        let li = document.createElement('li');
                        li.style.paddingTop = '0.3125rem';
                        li.style.paddingBottom = '0.3125rem';
                        li.style.height = '2.1875rem';
                        li.style.paddingLeft = '0.9375rem';
                        li.style.fontWeight = '400';
                        li.style.overflow = 'hidden';
                        li.setAttribute('id', pk);

                        // Create link for search result product
                        let linkTag = document.createElement('a');
                        linkTag.href = "/forum/post/" + pk;
                        linkTag.style.color = black;
                        linkTag.style.display = 'block';

                        // Change the border of search typeahead
                        searchTypeAhead.style.border = '0.0625rem grey solid';
                        searchTypeAhead.style.borderTop = '0';

                        // Add mouse enter and mouse out event listeners for li and link
                        li.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = royalBlue;
                            linkTag.style.color = white;
                        });

                        li.addEventListener('mouseout', function() {
                            li.style.backgroundColor = white;
                            linkTag.style.color = black;
                        });

                        linkTag.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = royalBlue;
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
                        searchResultsPosts.appendChild(li);
                    }
                }
                else {
                    // Create the li element
                    let li = document.createElement('li');
                    li.style.paddingTop = '0.3125rem';
                    li.style.paddingBottom = '0.3125rem';
                    li.style.height = '2.1875rem';
                    li.style.paddingLeft = '0.9375rem';
                    li.style.fontWeight = '400';
                    li.style.overflow = 'hidden';
                    li.innerHTML = searchText;

                    // Change the border of search typeahead
                    searchTypeAhead.style.border = '0.0625rem grey solid';
                    searchTypeAhead.style.borderTop = '0';

                    // Add mouse enter and mouse out event listeners for li
                    li.addEventListener('mouseenter', function() {
                        li.style.backgroundColor = royalBlue;
                    });

                    li.addEventListener('mouseout', function() {
                        li.style.backgroundColor = white;
                    });

                    // Append li to search results
                    searchResultsPosts.appendChild(li);
                }
            }
        };
    }
    xhr.onerror = function() {
        console.log('Request error...');
    };
    xhr.open("POST", "/forum/posts_results/" + searchText + "/", true);
    // Assign the csrftoken to a variable so it can be used in the AJAX
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
}

function getDraftsResults() {
    let xhr = new XMLHttpRequest();
    var searchRequest = null;
    // Abort old pending requests
    if (searchRequest) {
        searchRequest.abort();
    }

    // Unbind event listener before new AJAX call
    searchInputDrafts.removeEventListener('keyup', getDraftsResults);

    // Get the search text from the search input
    let searchText = searchInputDrafts.value;

    // Clear the search results
    searchResultsDrafts.innerHTML = '';

    // Remove search typeahead border after results are cleared
    searchTypeAhead.style.border = 'none';

    if (searchText) {
        xhr.onload = function() {
            if (this.readyState == 4 && this.status == 200) {
                let results = JSON.parse(xhr.responseText);

                // Clear the search results
                if (searchResultsDrafts) {
                    searchResultsDrafts.innerHTML = '';
                }

                // Modify the search ul background color to white
                searchResultsDrafts.style.backgroundColor = white;

                // Loop through the list of dictionaries
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {

                        // Get title and slug from list of dictionaries
                        let title = Object.keys(results[i]);
                        let pk = Object.values(results[i]);

                        // Create the li element
                        let li = document.createElement('li');
                        li.style.paddingTop = '0.3125rem';
                        li.style.paddingBottom = '0.3125rem';
                        li.style.height = '2.1875rem';
                        li.style.paddingLeft = '0.9375rem';
                        li.style.fontWeight = '400';
                        li.style.overflow = 'hidden';
                        li.setAttribute('id', pk);

                        // Create link for search result product
                        let linkTag = document.createElement('a');
                        linkTag.href = "/forum/post/" + pk;
                        linkTag.style.color = black;
                        linkTag.style.display = 'block';


                        // Add mouse enter and mouse out event listeners for li and link
                        li.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = royalBlue;
                            linkTag.style.color = white;
                        });

                        li.addEventListener('mouseout', function() {
                            li.style.backgroundColor = white;
                            linkTag.style.color = black;
                        });

                        linkTag.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = royalBlue;
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
                        searchResultsDrafts.appendChild(li);
                    }
                }
                else {
                    // Create the li element
                    let li = document.createElement('li');
                    li.style.paddingTop = '0.3125rem';
                    li.style.paddingBottom = '0.3125rem';
                    li.style.height = '2.1875rem';
                    li.style.paddingLeft = '0.9375rem';
                    li.style.fontWeight = '400';
                    li.style.overflow = 'hidden';
                    li.innerHTML = searchText;

                    // Add mouse enter and mouse out event listeners for li
                    li.addEventListener('mouseenter', function() {
                        li.style.backgroundColor = royalBlue;
                    });

                    li.addEventListener('mouseout', function() {
                        li.style.backgroundColor = white;
                    });

                    // Append li to search results
                    searchResultsDrafts.appendChild(li);
                }

                // Remove navbar margin bottom bootstrap class
            }
        };
    }
    xhr.onerror = function() {
        console.log('Request error...');
    };
    xhr.open("POST", "/forum/drafts_results/" + searchText + "/", true);
    // Assign the csrftoken to a variable so it can be used in the AJAX
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
}

// Performed debouncing to avoid unnecessary requests on keyup
var debounceTimeout = null;

if (searchInputPosts) {
    searchInputPosts.addEventListener('keyup', function(event) {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(getPostsResults, 100);
    });
}

if (searchInputDrafts) {
    searchInputDrafts.addEventListener('keyup', function(event) {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(getDraftsResults, 100);
    });
}
