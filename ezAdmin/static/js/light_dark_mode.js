function darkModeFunction(urlDarkMode) {
    $(document).ready(function () {
      const darkModeToggle = $('#dark-mode-toggle');
      const csrfToken = $('meta[name="csrf-token"]').attr('content');

      $.ajax({
        type: 'GET',
        url: urlDarkMode,  
        success: function (response) {
          const initialDarkModeState = response.dark_mode; 
          
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
        const isAuthenticated = darkModeToggle.data('is-authenticated') == true;
        console.log(isAuthenticated)
        if (isAuthenticated) {
          $.ajax({
            type: 'POST',
            url: urlDarkMode,  // Update this URL with your actual endpoint
            data: { dark_mode: isChecked.toString().charAt(0).toUpperCase() + isChecked.toString().slice(1) },
            headers: { 'X-CSRFToken': csrfToken },
            success: function () {
              document.body.classList.toggle('dark-mode', isChecked);
            },
            error: function () {
              console.error('Failed to update dark mode preference.');
            }
          });
        }
      });
    });
  }