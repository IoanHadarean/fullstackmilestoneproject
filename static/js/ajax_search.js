// Get HTML elements
let searchInput = document.getElementById('search_box');
console.log(searchInput);
let searchResults = document.getElementById('search-results');

// Add event listeners
searchInput.addEventListener('keyup', getItemCount);

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
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

var csrftoken = getCookie('csrftoken');

function getItemCount() {
    let xhr = new XMLHttpRequest();
    let searchText = searchInput.value;
    console.log(searchText);
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            let results = JSON.parse(xhr.responseText);
            console.log(results);
            if (searchResults) {
                searchResults.innerHTML = '';
            }
            for (var i = 0; i < results.length; i++) {
                let title =  Object.keys(results[i]);
                let slug = Object.values(results[i]);
                let li = document.createElement('li');
                let linkTag = document.createElement('a');
                linkTag.href = "/shoppingcart/product/" + slug;
                li.appendChild(linkTag);
                linkTag.appendChild(document.createTextNode(title));
                searchResults.appendChild(li);
            }
        }
        xhr.onerror = function() {
            console.log('Request error...');
        };
    };
    xhr.open("POST", "/shoppingcart/search_results/" + searchText + "/", true);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
}
