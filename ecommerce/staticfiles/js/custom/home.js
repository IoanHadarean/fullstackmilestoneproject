/* global location */

// Check the current location path
// Get the filter nav links
// If the href of the nav link is equal to the current
// location path add the 'active' class to the link
(function() {
    var current = location.pathname;
    var navLinks = document.getElementsByClassName('nav-filter');
    for (var i = 0; i < navLinks.length; i++) {
        if (navLinks[i].getAttribute('href').indexOf(current) !== -1 && current != '/') {
            navLinks[i].parentElement.classList.add('active');
        }
        else if (current == '/') {
            navLinks[0].parentElement.classList.add('active');
        }
    }
})();