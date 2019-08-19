// Get HTML elements
var currentCardForm = document.getElementsByClassName('current-card-form')[0];
var newCardForm = document.getElementsByClassName('new-card-form')[0];
var useDefaultCard = document.getElementsByClassName('use-default-card');


function filterCards(arr, card) {
    return arr.filter(function(element) {
        return element.id != card.id;
    });
}



// Hide the new card form if use default card is checked, else show it
// Display the current card form for each of the default cards if they are checked
for (var i = 0; i < useDefaultCard.length; i++) {
    useDefaultCard[i].addEventListener('change', function() {
        
        // Make an array from the use default card HTML collection
        // Filter the array by the checked default card
        // Hide all other use default card checkboxes if one is checked
        var cardArray = Array.prototype.slice.call(useDefaultCard);
        var filteredCards = filterCards(cardArray, this);
        if (this.checked == true) {
            for (var j = 0; j < filteredCards.length; j++) {
                document.getElementsByClassName(filteredCards[j].id)[0].style.display = 'none';
            }
            newCardForm.style.display = 'none';
            currentCardForm.style.display = 'block';
        }
        else {
            for (var j = 0; j < filteredCards.length; j++) {
                document.getElementsByClassName(filteredCards[j].id)[0].style.display = 'block';
            }
            newCardForm.style.display = 'block';
            currentCardForm.style.display = 'none';
        }
    });
}

