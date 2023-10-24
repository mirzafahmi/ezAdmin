function performAjaxAction() {
    $(document).ready(function () {
        // Function to set the readonly state based on a flag
        function setReadonlyState(flag) {
            $('#id_lot_number').prop('readonly', flag);
            $('#id_exp_date').prop('readonly', flag);
            $('#id_price_per_unit').prop('readonly', flag);
            $('#id_purchasing_doc').prop('readonly', flag);
        }

        // Check the local storage for the readonly flag
        var readonlyFlag = localStorage.getItem('readonlyFlag');
    
        // If the flag is set, apply readonly state
        if (readonlyFlag === 'true') {
            setReadonlyState(true);
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
    
        function fetchComponentOptions(identifierId, componentId, stockType) {
            var baseUrl = '{% url 'purchasing-raw-material-inventory-identifier-component-based-log-create-ajax' %}';
            var ajaxUrl = baseUrl + '?component_id=' + componentId + '&type=' + stockType;

            $.ajax({
                url: ajaxUrl,
                method: 'GET',
                data: {
                    identifier_id: identifierId,
                    component_id: componentId,
                    type: stockType
                },
                dataType: 'json',
                success: function (data) {
                    // Update component field with retrieved options
                    $('#id_component').val(data.component).prop('readonly', true);
                    
                    // Set readonly state and store the flag in local storage
                    if (stockType === '2') {
                        $.ajax({
                            url: ajaxUrl,  // Replace with your actual endpoint
                            method: 'GET',
                            data: {
                                identifier_id: identifierId,
                                component_id: componentId,
                                type: stockType
                            },
                            dataType: 'json',
                            success: function (data) {
                                // Update form fields with retrieved information
                                $('#id_lot_number').val(data.lot_number);
                                $('#id_exp_date').val(data.exp_date);
                                $('#id_price_per_unit').val(data.price_per_unit);
                                $('#id_purchasing_doc').val(data.purchasing_doc);
            
                                // Set readonly state and store the flag in local storage
                                setReadonlyState(true);
                                localStorage.setItem('readonlyFlag', 'true');

                                var availableQuantity = data.available_quantity;
                                var quantityField = $('#id_quantity');
                                var selectedQuantity = parseFloat(quantityField.val());
                                console.log(selectedQuantity)
                                /*if (selectedQuantity > availableQuantity) {
                                    // Raise an error and disable form submission
                                    quantityField.val('');  // Clear the field
                                    alert('Quantity exceeds available quantity.');
                                }*/
                            },
                            error: function () {
                                console.log('Error fetching FIFO information.');
                            }
                        });
                    } else {
                        // If the type is not '2', remove readonly attribute and clear the flag
                        setReadonlyState(false);
                        localStorage.removeItem('readonlyFlag');
                    }
                    
                },
                error: function () {
                    console.log('Error fetching component options.');
                }
            });
        }
        
        if (identifierId && componentId && stockType) {
            fetchComponentOptions(identifierId, componentId, stockType);
        }

        // Listen for changes in the component field
        $('#id_component').on('change', function () {
            var componentId = $(this).val();
            var type = $('#id_stock_type').val();  // Assuming stock_type has the ID id_stock_type

            var baseUrl = '{% url 'purchasing-raw-material-inventory-ajax' %}';
            var ajaxUrl = baseUrl + '?component_id=' + componentId + '&type=' + type;


            // Make AJAX request to fetch FIFO information
            if (type === '2') {
                $.ajax({
                    url: ajaxUrl,  // Replace with your actual endpoint
                    method: 'GET',
                    data: {
                        identifier_id: identifierId,
                        component_id: componentId,
                        type: type
                    },
                    dataType: 'json',
                    success: function (data) {
                        // Update form fields with retrieved information
                        $('#id_lot_number').val(data.lot_number);
                        $('#id_exp_date').val(data.exp_date);
                        $('#id_price_per_unit').val(data.price_per_unit);
                        $('#id_purchasing_doc').val(data.purchasing_doc);
    
                        // Set readonly state and store the flag in local storage
                        setReadonlyState(true);
                        localStorage.setItem('readonlyFlag', 'true');
                    },
                    error: function () {
                        console.log('Error fetching FIFO information.');
                    }
                });
            } else {
                // If the type is not '2', remove readonly attribute and clear the flag
                setReadonlyState(false);
                localStorage.removeItem('readonlyFlag');
            }
        });
        
        var checkboxField = $('#id_data_overide');

        checkboxField.on('change', function() {
            if (checkboxField.prop('checked')) {
                setReadonlyState(false);
            } else {
                setReadonlyState(true);
            }
        });

    });        
}