function darkModeFunction(urlDarkMode) {
    $(document).ready(function () {
      const darkModeToggle = $('#dark-mode-toggle');
      const csrfToken = $('meta[name="csrf-token"]').attr('content');

      $.ajax({
        type: 'GET',
        url: urlDarkMode,  // Replace with the actual endpoint to get user's dark mode preference
        success: function (response) {
          console.log(response)
            // Set the initial state of the toggle based on the response
            const initialDarkModeState = response.dark_mode;  // Assuming the response has a 'dark_mode' property
            darkModeToggle.prop('checked', initialDarkModeState);
            $('body').toggleClass('dark-mode', initialDarkModeState);
            $('#dark-mode-styles').prop('disabled', !initialDarkModeState);
        },
        error: function () {
            console.error('Failed to retrieve dark mode preference.');
        }
      });
  
      darkModeToggle.change(function () {
        const isChecked = darkModeToggle.prop('checked');
        $('body').toggleClass('dark-mode', isChecked);
        $('#dark-mode-styles').prop('disabled', !isChecked);

        //console.log(isChecked.toUpperCase().charAt(0) + isChecked.slice(1))
          $.ajax({
            type: 'POST',
            url: urlDarkMode,  // Update this URL with your actual endpoint
            data: { dark_mode: isChecked.toString().charAt(0).toUpperCase() + isChecked.toString().slice(1) },
            headers: { 'X-CSRFToken': csrfToken },
            success: function () {
                // Optionally, you can update the styles dynamically here
                document.body.classList.toggle('dark-mode', isChecked);
            },
            error: function () {
                console.error('Failed to update dark mode preference.');
            }
        });
      });
    });
  }