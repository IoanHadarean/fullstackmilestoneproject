// Get HTML elements
var currentCardForm = document.getElementsByClassName('current-card-form')[0];
var newCardForm = document.getElementsByClassName('new-card-form')[0];
var useDefaultCard = document.querySelector("input[name=use_default_card]");
var savedCards = document.getElementsByClassName('saved_card');

/*
Hide the new card form if use default card is checked, else show it
Hide the saved cards if use default card is checked
*/
if (useDefaultCard) {
    useDefaultCard.addEventListener('change', function() {
        if (this.checked == true) {
            for (var j = 0; j < savedCards.length; j++) {
                savedCards[j].style.display = 'none';
            }
            newCardForm.style.display = 'none';
            currentCardForm.style.display = 'block';
        }
        else {
            for (var j = 0; j < savedCards.length; j++) {
                savedCards[j].style.display = 'block';
            }
            newCardForm.style.display = 'block';
            currentCardForm.style.display = 'none';
        }
    });
}
