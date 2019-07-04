// Get HTML alert
let alerts = document.querySelectorAll('.alert');

// Clear alert after 3 seconds
setTimeout(clearError, 5000);


function clearError() {
    if (alerts) {
        for ( var i = 0; i < alerts.length ; i++) {
            alerts[i].remove();
        }
    }
}