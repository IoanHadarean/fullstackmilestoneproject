// Get HTML elements
var currentCardForm = document.getElementsByClassName('current-card-form')[0];
var newCardForm = document.getElementsByClassName('new-card-form')[0];
var useDefaultCard = document.getElementsByClassName('use-default-card');

// Hide card form if use default card is checked, else show it
for (var i = 0; i < useDefaultCard.length; i++) {
    useDefaultCard[i].addEventListener('change', function() {
        if (this.checked) {
            console.log(this);
            newCardForm.style.display = 'none';
            currentCardForm.style.display = 'block';
        }
        else {
            newCardForm.style.display = 'block';
            currentCardForm.style.display = 'none';
        }
    });
}

