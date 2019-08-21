// Get HTML elements
var cardNumber = document.querySelector("input[name=cardNumber]");
var cardExpMonth = document.querySelector("input[name=cardExpMonth]");
var cardExpYear = document.querySelector("input[name=cardExpYear]");
var cardCVV = document.querySelector("input[name=cardCVV]");


// Restricts input for the given textbox to the given inputFilter.
function setInputFilter(textbox, inputFilter) {
    ["input", "keydown", "keyup", "mousedown", "mouseup", "select", "contextmenu", "drop"].forEach(function(event) {
        textbox.addEventListener(event, function() {
            if (inputFilter(this.value)) {
                this.oldValue = this.value;
                this.oldSelectionStart = this.selectionStart;
                this.oldSelectionEnd = this.selectionEnd;
            }
            else if (this.hasOwnProperty("oldValue")) {
                this.value = this.oldValue;
                this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            }
        });
    });
}


// Install input filters for cardNumber, cardExpMonth, cardExpYear and cardCVV
setInputFilter(cardNumber, function(value) {
    return /^\d*$/.test(value);
});

setInputFilter(cardExpMonth, function(value) {
    return /^\d*$/.test(value);
});

setInputFilter(cardExpYear, function(value) {
    return /^\d*$/.test(value);
});

setInputFilter(cardCVV, function(value) {
    return /^\d*$/.test(value);
});
