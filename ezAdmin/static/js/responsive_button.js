function responsiveButtonText(buttonId) {
    function updateButton(originalContent) {
        var screenWidth = $(window).width();
        var button = $('#' + buttonId);
        var icon = button.find('i');
    
        if (screenWidth < 973) {
            button.contents().filter(function() {
                return this.nodeType === 3; // Node.TEXT_NODE
            }).remove();
            icon.removeClass('me-1');
        } else {
            // Restore the original content
            button.html(originalContent);
        }
    }
    
    $(document).ready(function () {
        console.log('responsive button');
    
        // Store the original content when the page loads
        var originalContent = $('#' + buttonId).html();
    
        // Initial update on page load
        updateButton();
    
        // Update on window resize
        $(window).resize(function() {
            updateButton(originalContent);
        });
    });
}
