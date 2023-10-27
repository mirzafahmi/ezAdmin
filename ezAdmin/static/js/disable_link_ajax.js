function disableLinkAjaxAction() {
    $(document).ready(function () {
        console.log('from ajax main')

        function disableLink() {
            $('#log-out-link')
                .removeClass('btn-primary')
                .addClass('btn-secondary')
                .off('click')
                .click(function (e) {
                    e.preventDefault(); // Prevent the default link behavior
                });
        }

        function getUrlParameter(name) {
            var regex = new RegExp(name + ':([^&;]+?)(&|#|;|$)');
            var results = regex.exec(window.location.href);
            if (!results) return null;
            if (!results[1]) return '';

            // Split the value by '/'
            var values = results[1].split('/');
            
            // Get the first value
            var desiredValue = values[0];
            
            return decodeURIComponent(desiredValue.replace(/\+/g, ' '));
        }

        var identifierId = getUrlParameter('identifier');
        var componentId = getUrlParameter('component');
        var stockType = getUrlParameter('type');

        const logLink = document.getElementById("log-link");
        var ajaxUrl = baseUrl + '?component_id=' + componentId

        $.ajax({
            url: ajaxUrl,  // Replace with your actual endpoint
            method: 'GET',
            data: {
                identifier_id: identifierId,
                component_id: componentId,
            },
            dataType: 'json',
            success: function (data) {
                var showAlert = data.alert
                var componentName = data.component_name
                var identifier = data.identifier_name
                console.log(showAlert)
                if (showAlert) {
                    disableLink()
                    $('#log-out-link').click(function () {
                        customAlert.alert(componentName + ' for ' + identifier + ' inventory is empty, please stock up the inventory.', 'No stock available');
                    });
                }
            },
            error: function () {
                console.log('Error fetching Alert information.');
            }
        });
    })
}