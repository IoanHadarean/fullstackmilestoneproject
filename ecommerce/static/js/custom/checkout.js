// Get shipping/billing forms and checkboxes
var hideableShippingForm = document.getElementsByClassName('hideable_shipping_form')[0];
var hideableBillingForm = document.getElementsByClassName('hideable_billing_form')[0];

var useDefaultShipping = document.querySelector("input[name=use_default_shipping]");
var useDefaultShippingContainer = document.getElementsByClassName('use-default-shipping')[0];
var useDefaultBilling = document.querySelector("input[name=use_default_billing]");
var useDefaultBillingContainer = document.getElementsByClassName('use-default-billing')[0];
var saveDefaultShipping = document.querySelector("input[name=set_default_shipping]");
var saveDefaultShippingContainer = document.getElementsByClassName('save-default-shipping')[0];
var sameBillingAddress = document.querySelector("input[name=same_billing_address]");
var setDefaultAddressLabel = document.querySelector('label[for=set_default_shipping]');

// Hide shipping form if use default shipping is checked, else show it
if (useDefaultShipping) {

    // On change event
    useDefaultShipping.addEventListener('change', function() {
        if (this.checked == true && (sameBillingAddress.checked == false)) {
            hideableShippingForm.style.display = 'none';
        }
        else if (this.checked == true && (sameBillingAddress.checked == true)) {
            hideableShippingForm.style.display = 'block';
            saveDefaultShippingContainer.style.display = 'none';
        }
        else {
            hideableShippingForm.style.display = 'block';
            saveDefaultShippingContainer.style.display = 'block';
        }
    });
}

// Hide billing form if use default billing is checked, else show it
if (useDefaultBilling) {

    // On change event
    useDefaultBilling.addEventListener('change', function() {
        if (this.checked == true) {
            hideableBillingForm.style.display = 'none';
        }
        else {
            hideableBillingForm.style.display = 'block';
        }
    });

    // On GET
    if (useDefaultBilling.checked == true) {
        hideableBillingForm.style.display = 'none';
    }
    else {
        hideableBillingForm.style.display = 'block';
    }
}

/*
Hide billing form if same billing address is checked and default shipping is not checked, else show it
Change set default shipping address text when same billing address is checked
*/
if (sameBillingAddress) {

    // On change event
    sameBillingAddress.addEventListener('change', function() {
        if (this.checked == true) {
            hideableBillingForm.style.display = 'none';
            setDefaultAddressLabel.innerHTML = 'Save as default shipping/billing address';
            if (useDefaultBillingContainer) {
                useDefaultBillingContainer.style.display = 'none';
            }
        }
        else {
            hideableBillingForm.style.display = 'block';
            setDefaultAddressLabel.innerHTML = 'Save as default shipping address';
            if (useDefaultBillingContainer) {
                useDefaultBillingContainer.style.display = 'block';
            }
            if (useDefaultShipping) {
                if (useDefaultShipping.checked == true) {
                    hideableShippingForm.style.display = 'none';
                }
            }
        }
    });

    // On GET
    if (sameBillingAddress.checked == true) {
        hideableBillingForm.style.display = 'none';
        setDefaultAddressLabel.innerHTML = 'Save as default shipping/billing address';
        if (useDefaultBillingContainer) {
            useDefaultBillingContainer.style.display = 'none';
        }
        if (saveDefaultShipping) {
            if (saveDefaultShipping.checked == true) {
                useDefaultShippingContainer.style.display = 'none';
            }
            else {
                useDefaultShippingContainer.style.display = 'block';
            }
        }
        if (useDefaultShipping) {
            if (useDefaultShipping.checked == true) {
                saveDefaultShippingContainer.style.display = 'none';
            }
            else {
                saveDefaultShippingContainer.style.display = 'block';
            }
        }
    }
    else {
        hideableBillingForm.style.display = 'block';
        setDefaultAddressLabel.innerHTML = 'Save as default shipping address';
        if (useDefaultBillingContainer) {
            useDefaultBillingContainer.style.display = 'block';
        }
        if (useDefaultShipping) {
            if (useDefaultShipping.checked == true) {
                hideableShippingForm.style.display = 'none';
            }
            else {
                hideableShippingForm.style.display = 'block';
            }
        }
        if (useDefaultBilling) {
            if (useDefaultBilling.checked == true) {
                hideableBillingForm.style.display = 'none';
            }
            else {
                hideableBillingForm.style.display = 'block';
            }
        }
    }
}

// Hide use default shipping is save default shipping is checked, else show it
if (saveDefaultShipping) {

    // On change event
    saveDefaultShipping.addEventListener('change', function() {
        if (this.checked == true) {
            useDefaultShippingContainer.style.display = 'none';
        }
        else {
            useDefaultShippingContainer.style.display = 'block';
        }
    });
}
