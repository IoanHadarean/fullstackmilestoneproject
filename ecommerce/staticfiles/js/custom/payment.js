// Get HTML elements
var currentCardForm = document.getElementsByClassName('current-card-form')[0];
var newCardForm = document.getElementsByClassName('new-card-form')[0];
var useDefaultCard = document.querySelector('input[name=use_default_card]');

// Hide card form if use default card is checked, else show it
if (useDefaultCard) {
    useDefaultCard.addEventListener('change', function() {
        if (this.checked) {
            newCardForm.style.display = 'none';
            currentCardForm.style.display = 'block';
        }
        else {
            newCardForm.style.display = 'block';
            currentCardForm.style.display = 'none';
        }
    });
}
