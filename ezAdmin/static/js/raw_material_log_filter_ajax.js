function rawMaterialLogFilter(){
    $(document).ready(function () {
        function getUrlParameter(name) {
            var regex = new RegExp(name + ":([^&;]+?)(&|#|;|$|-)");
            var results = regex.exec(window.location.href);
            if (!results) return null;
            if (!results[1]) return "";
      
            // Split the value by '/', '-', or any combination of them
            var values = results[1].split(/[/|-]+/);
      
            // Get the first value
            var desiredValue = values[0];
          
            desiredValue = desiredValue.split('-')[0];
          
            return decodeURIComponent(desiredValue.replace(/\+/g, " "));
        }

        var identifierId = getUrlParameter("identifier");
        var componentId = getUrlParameter("component");
        var stockType = getUrlParameter("type");

        // Function to generate dynamic buttons for filter based on stock_in_tag
        function generateFilterButtonsAndLoadLogs(data) {

            data.forEach(function (log) {
                var radioId = 'vbtn-radio-' + log.lot.replace(/\s+/g, '-').toLowerCase();
                $('#filter-label').append(
                    `<input type="radio" class="btn-check" name="vbtn-radio" id="${radioId}" data-identifier="${log.identifier}" data-component="${log.component}" data-stock-in-tag="${log.stock_in_tag}">` +
                    `<label class="btn btn-outline-primary me-1" for="${radioId}" data-identifier="${log.identifier}" data-component="${log.component}" data-stock-in-tag="${log.stock_in_tag}">${log.lot === '-'? log.purchasing_document: log.lot}</label>`
                );
            });
    
            // Event listener for label clicks to load logs when the associated radio button is triggered
            $('#filter-label').on('change', 'label', function () {
                var identifier = $(this).data('identifier');
                var component = $(this).data('component');
                var stockInTag = $(this).data('stock-in-tag');
                loadLogs(identifier, component, stockInTag);
            });
    
            // Event listener for radio button clicks, you might still use it independently if needed
            $('#filter-label').on('change', 'input[type="radio"]', function () {
                var identifier = $(this).data('identifier');
                var component = $(this).data('component');
                var stockInTag = $(this).data('stock-in-tag');
                loadLogs(identifier, component, stockInTag);
            });
        }

        // Function to load logs based on stock_in_tag when a button is clicked
        function loadLogs(identifier, component, stockInTag) {
        $.ajax({
            url: baseUrl,
            method: 'GET',
            data: {
                identifier_id: identifier,
                component_id: component,
                stock_in_tag: stockInTag,
            },
            dataType: "json",
            success: function (data) {
                function formatCustomDate(dateString) {
                    if (dateString) {
                        var date = new Date(dateString);
                        var options = { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
                        return new Intl.DateTimeFormat('en-US', options).format(date);
                    } else {
                        return 'None';
                    }
                }

                $('#logs-table-body').empty();
                data.forEach(function (log) {
                    var formattedStockInDate = formatCustomDate(log.stock_in_date);
                    var formattedStockOutDate = formatCustomDate(log.stock_out_date);

                    var editUrl = `/production_main/raw_material_inventory_identifier_based_main/identifier:${log.identifier_id}-component-main/component:${log.component_id}-list/inventory_log_create_main/stock_type:${log.stock_type}-log:${log.log_id}-update`
                    var deleteUrl = `/production_main/raw_material_inventory_identifier_based_main/identifier:${log.identifier_id}-component-main/component:${log.component_id}-list/inventory_log_create_main/stock_type:${log.stock_type}-log:${log.log_id}-delete`

                    $('#logs-table-body').append(`
                            <tr>
                                <td>${log.identifier}</td>
                                <td>${log.component} for ${log.identifier}</td>
                                <td>${log.quantity}</td>
                                <td>${log.lot}</td>
                                <td>${log.expiry_date}</td>
                                <td>${formattedStockInDate}</td>
                                <td>${formattedStockOutDate}</td>
                                <td>${log.price_per_unit}</td>
                                <td>${log.purchasing_document}(${log.company_name})</td>
                                <td>
                                    <div class="d-grid">
                                        <a class="btn btn-outline-primary btn-sm btn-block" href="${editUrl}">
                                            Edit
                                        </a>
                                        <a class="btn btn-outline-success btn-sm btn-block" href="">
                                            Validate
                                        </a>
                                        <a class="btn btn-outline-danger btn-sm btn-block" href="${deleteUrl}">
                                            Delete
                                        </a>
                                    </div>
                                </td>
                            </tr>
                        `);
                });
                $('#table-footer').empty();
                $('#table-footer').append(`
                        <tr class="table-group-divider">
                            <td colspan="2" class="fw-bold">BALANCE</td>
                            <td>${data[0].balance}</td>
                        </tr>
                    `);
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    };

    // Initial AJAX call to generate filter buttons
        $.ajax({
            url: baseUrl,
            method: 'GET',
            data: {
                identifier_id: identifierId,
                component_id: componentId,
            },
            dataType: "json",
            success: function (data) {
                generateFilterButtonsAndLoadLogs(data);
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });    
}