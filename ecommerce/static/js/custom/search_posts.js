// Get HTML elements
let searchInputPosts = document.getElementById('search_posts');
let searchInputDrafts = document.getElementById('search_drafts');
let searchResultsPosts = document.getElementById('search-results-posts');
let searchResultsDrafts = document.getElementById('search-results-drafts');

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
    let searchText = searchInputPosts.value;
    searchResultsPosts.innerHTML = '';
    if (searchText) {
        xhr.onload = function() {
            if (this.readyState == 4 && this.status == 200) {
                let results = JSON.parse(xhr.responseText);
                if (searchResultsPosts) {
                    searchResultsPosts.innerHTML = '';
                }

                // Modify the search ul background color to white
                searchResultsPosts.style.backgroundColor = 'white';

                // Loop through the list of dictionaries
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {

                        // Get title and slug from list of dictionaries
                        let title = Object.keys(results[i]);
                        let pk = Object.values(results[i]);

                        // Create the li element
                        let li = document.createElement('li');
                        li.style.paddingTop = '5px';
                        li.style.paddingBottom = '5px';
                        li.style.height = '35px';
                        li.style.paddingLeft = '10px';
                        li.setAttribute('id', pk);

                        // Create link for search result product
                        let linkTag = document.createElement('a');
                        linkTag.href = "/forum/post/" + pk;
                        linkTag.style.color = 'black';
                        linkTag.style.display = 'block';


                        // Add mouse enter and mouse out event listeners for li and link
                        li.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = '#4285f4';
                            linkTag.style.color = 'white';
                        });

                        li.addEventListener('mouseout', function() {
                            li.style.backgroundColor = 'white';
                            linkTag.style.color = 'black';
                        });

                        linkTag.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = '#4285f4';
                            linkTag.style.color = 'white';
                        });

                        linkTag.addEventListener('mouseout', function() {
                            li.style.backgroundColor = 'white';
                            linkTag.style.color = 'black';
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
                    li.style.paddingTop = '5px';
                    li.style.paddingBottom = '5px';
                    li.style.paddingLeft = '10px';
                    li.style.height = '35px';
                    li.innerHTML = searchText;

                    // Add mouse enter and mouse out event listeners for li
                    li.addEventListener('mouseenter', function() {
                        li.style.backgroundColor = '#4285f4';
                    });

                    li.addEventListener('mouseout', function() {
                        li.style.backgroundColor = 'white';
                    });

                    // Append li to search results
                    searchResultsPosts.appendChild(li);
                }

                // Remove navbar margin bottom bootstrap class
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
    let searchText = searchInputDrafts.value;
    searchResultsDrafts.innerHTML = '';
    if (searchText) {
        xhr.onload = function() {
            if (this.readyState == 4 && this.status == 200) {
                let results = JSON.parse(xhr.responseText);
                if (searchResultsDrafts) {
                    searchResultsDrafts.innerHTML = '';
                }

                // Modify the search ul background color to white
                searchResultsDrafts.style.backgroundColor = 'white';

                // Loop through the list of dictionaries
                if (results.length > 0) {
                    for (var i = 0; i < results.length; i++) {

                        // Get title and slug from list of dictionaries
                        let title = Object.keys(results[i]);
                        let pk = Object.values(results[i]);

                        // Create the li element
                        let li = document.createElement('li');
                        li.style.paddingTop = '5px';
                        li.style.paddingBottom = '5px';
                        li.style.height = '35px';
                        li.style.paddingLeft = '10px';
                        li.setAttribute('id', pk);

                        // Create link for search result product
                        let linkTag = document.createElement('a');
                        linkTag.href = "/forum/post/" + pk;
                        linkTag.style.color = 'black';
                        linkTag.style.display = 'block';


                        // Add mouse enter and mouse out event listeners for li and link
                        li.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = '#4285f4';
                            linkTag.style.color = 'white';
                        });

                        li.addEventListener('mouseout', function() {
                            li.style.backgroundColor = 'white';
                            linkTag.style.color = 'black';
                        });

                        linkTag.addEventListener('mouseenter', function() {
                            li.style.backgroundColor = '#4285f4';
                            linkTag.style.color = 'white';
                        });

                        linkTag.addEventListener('mouseout', function() {
                            li.style.backgroundColor = 'white';
                            linkTag.style.color = 'black';
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
                    li.style.paddingTop = '5px';
                    li.style.paddingBottom = '5px';
                    li.style.paddingLeft = '10px';
                    li.style.height = '35px';
                    li.innerHTML = searchText;

                    // Add mouse enter and mouse out event listeners for li
                    li.addEventListener('mouseenter', function() {
                        li.style.backgroundColor = '#4285f4';
                    });

                    li.addEventListener('mouseout', function() {
                        li.style.backgroundColor = 'white';
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
