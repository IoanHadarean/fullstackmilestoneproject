// Get HTML elements
var hideableShippingForm = document.getElementsByClassName('hideable_shipping_form')[0];
var hideableBillingForm = document.getElementsByClassName('hideable_billing_form')[0];

var useDefaultShipping = document.querySelector("input[name=use_default_shipping]");
var useDefaultBilling = document.querySelector("input[name=use_default_billing]");
var sameBillingAddress = document.querySelector("input[name=same_billing_address]");

// Hide shipping form if use default shipping is checked, else show it
if (useDefaultShipping) {
    useDefaultShipping.addEventListener('change', function() {
        if (this.checked) {
            hideableShippingForm.style.display = 'none';
        }
        else {
            hideableShippingForm.style.display = 'block';
        }
    });
}

// Hide billing form if use default billing is checked, else show it
if (useDefaultBilling) {
    useDefaultBilling.addEventListener('change', function() {
        if (this.checked) {
            hideableBillingForm.style.display = 'none';
        }
        else {
            hideableBillingForm.style.display = 'block';
        }
    });
}

// Hide billing form if billing address is the same as shipping address is checked, else show it
sameBillingAddress.addEventListener('change', function() {
    if (this.checked) {
        hideableBillingForm.style.display = 'none';
        
    }
    else {
        hideableBillingForm.style.display = 'block';
    }
});
