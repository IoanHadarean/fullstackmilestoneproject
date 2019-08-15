// Get HTML elements
var hideableShippingForm = document.getElementsByClassName('hideable_shipping_form')[0];
var hideableBillingForm = document.getElementsByClassName('hideable_billing_form')[0];

var useDefaultShipping = document.querySelector("input[name=use_default_shipping]");
var useDefaultBilling = document.querySelector("input[name=use_default_billing]");
var sameBillingAddress = document.querySelector("input[name=same_billing_address]");
var setDefaultAddressLabel = document.querySelector('label[for=set_default_shipping]');

// Hide shipping form if use default shipping is checked, else show it
if (useDefaultShipping) {
    useDefaultShipping.addEventListener('change', function() {
        if (this.checked == true && (sameBillingAddress.checked == false)) {
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
        if (this.checked == true) {
            hideableBillingForm.style.display = 'none';
        }
        else {
            hideableBillingForm.style.display = 'block';
        }
    });
}

// Hide billing form if same billing address is checked and default
// shipping is not checked, else show it
sameBillingAddress.addEventListener('change', function() {
    if (this.checked == true) {
        hideableBillingForm.style.display = 'none';
    }
    else if (this.checked == false && useDefaultShipping.checked == true) {
        hideableBillingForm.style.display = 'block';
        hideableShippingForm.style.display = 'none';
    }
    else {
        hideableBillingForm.style.display = 'block';
    }
});

// Change set default shipping address text when same billing address is checked
sameBillingAddress.addEventListener('change', function() {
    if (this.checked == true) {
        setDefaultAddressLabel.innerHTML = 'Save as default shipping/billing address';
    }
    else {
        setDefaultAddressLabel.innerHTML = 'Save as default shipping address';
    }
});
