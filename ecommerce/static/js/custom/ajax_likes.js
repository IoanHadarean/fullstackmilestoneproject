// Get HTML elements
var totalLikes = document.getElementById('total-likes');
var likeBtn = document.getElementById('like-post');
var dislikeBtn = document.getElementById('dislike-post');
var hiddenLikeFormInput = document.getElementById('like-form-input');

// Add event listeners
if (likeBtn) {
    likeBtn.addEventListener('click', likePost);
}
if (dislikeBtn) {
    dislikeBtn.addEventListener('click', dislikePost);
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

// AJAX function for liking a post
function likePost(e) {
    let pk = hiddenLikeFormInput.value;
    let xhr = new XMLHttpRequest();
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            let response = JSON.parse(xhr.responseText);
            
            // Change the total likes count message and font weight
            totalLikes.style.fontWeight = 'bolder';
            if (response.total_likes.length == 1) {
                if (response.total_likes[0] == 'You') {
                    totalLikes.innerHTML =  "You like this";
                }
                else if (isNaN(response.total_likes[0])) {
                   totalLikes.innerHTML = response.total_likes[0] + " likes this"; 
                }
                else {
                   totalLikes.innerHTML = response.total_likes[0] + " people like this";  
                }
            }
            else if (response.total_likes.length == 2) {
                if (response.total_likes[0] == 'You') {
                   totalLikes.innerHTML = "You and " + response.total_likes[1] + " like this";
                }
                else {
                   totalLikes.innerHTML = response.total_likes[0] + " and " + response.total_likes[1] + " like this"; 
                }
            }
        }
    };
    xhr.onerror = function() {
        console.log('Request error...');
    };
    xhr.open("POST", "/forum/post/" + pk + "/" + "like/");
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
    e.preventDefault();
}

// AJAX function for disliking a post
function dislikePost(e) {
    let pk = hiddenLikeFormInput.value;
    let xhr = new XMLHttpRequest();
    xhr.onload = function() {
        if (this.readyState == 4 && this.status == 200) {
            let response = JSON.parse(xhr.responseText);
            
            // Change the total likes count message and font weight
            totalLikes.style.fontWeight = 'bolder';
            if (response.total_likes.length == 1) {
                if (response.total_likes[0] == 'You') {
                    totalLikes.innerHTML =  "You like this";
                }
                else if (isNaN(response.total_likes[0])) {
                   totalLikes.innerHTML = response.total_likes[0] + " likes this"; 
                }
                else if (response.total_likes[0] != 0) {
                   totalLikes.innerHTML = response.total_likes[0] + " people like this";  
                }
                else {
                   totalLikes.innerHTML = "No likes";
                }
            }
            else if (response.total_likes.length == 2) {
                if (response.total_likes[0] == 'You') {
                   totalLikes.innerHTML = "You and " + response.total_likes[1] + " like this";
                }
                else {
                   totalLikes.innerHTML = response.total_likes[0] + " and " + response.total_likes[1] + " like this"; 
                }
            }
        }
    };
    xhr.onerror = function() {
        console.log('Request error...');
    };
    xhr.open("POST", "/forum/post/" + pk + "/" + "dislike/");
    let csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send();
    e.preventDefault();
}
