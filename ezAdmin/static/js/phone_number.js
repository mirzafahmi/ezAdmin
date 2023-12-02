function phoneNumberWidget(fieldName) {
    $(document).ready(function($) {
        $('#div_id_' + fieldName).addClass('d-flex flex-column')
        var input = $("#id_" + fieldName);

        // Save the initial value
        var initialValue = input.val();

        // Check if the initial value contains the country code
        var hasCountryCode = initialValue.startsWith("+");

        if (hasCountryCode) {
            // Remove the country code
            initialValue = initialValue.replace(/\D/g, '');
        }
        
        input.intlTelInput({
            preferredCountries: ["my","id", "sg", "th", "bn", "vn", "ph", "mm", "la", "kh"],  
            nationalMode: true,
            separateDialCode: true,
        });

        // Save the initial value
        var initialValue = input.val();

        // Remove the country code from the initial value
        var numericValue = initialValue.replace(/\D/g, '');
        initialValue = "+" + numericValue;

        // Set the initial value without the country code
        input.val(numericValue);

        // Add the country code back on form submission
        $("form").submit(function() {
            // Get the current input value
            var currentValue = input.val();

            // Add the country code back to the value
            var countryCode = input.intlTelInput("getSelectedCountryData").dialCode;
            input.val("+" + countryCode + " " + currentValue);
        });
    });
}