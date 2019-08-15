// Get Back Button
var backButton = document.getElementsByClassName('back-button')[0];

// Add event listener
if (backButton) {
    backButton.addEventListener('click', backToPreviousPage);
}

// Go back to previous page
function backToPreviousPage() {
    window.history.go(-1);
}
