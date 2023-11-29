function BOMComponentListFilter() {
    $(document).ready(function () {
        $.ajax({
            url: baseUrl,
            method: 'GET',
            dataType: "json",
            success: function (data) {
                data.forEach(function (itemCode) {
                    itemCodeWithUnderScore = itemCode.replace(/ /g, '-');
                    $('#filter-label').append(
                        `<input type="radio" class="btn-check" id="${itemCodeWithUnderScore}-item-code" name="vbtn-radio" data-itemcode="${itemCode}">` +
                        `<label class="btn btn-outline-primary me-1" for="${itemCodeWithUnderScore}-item-code"><a class="no-decoration">${itemCode}</a></label>`
                    );
                });
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });

        function loadItemCode(itemCode) {
            $.ajax({
                url: baseUrl,
                method: 'GET',
                data: {
                    item_code: itemCode,
                },
                dataType: "json",
                success: function (data) {
                    console.log(data)
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
                    $('#table-footer').empty();
                    if (data.length <= 0) {
                        $('#table-footer').empty();
                        $('#table-footer').append(`
                            <tr class="table-group-divider">
                                <td colspan="6" class="fw-bold">
                                    <hr>
                                    No BOMComponents available, please add in
                                    <hr>
                                </td>
                            </tr>
                        `);
                    }
                    
                    data.forEach(function (log, index) {
                        var formattedCreateDate = formatCustomDate(log.create_date);
                        

                        var editUrl = `BOM_component_list/${log.BOMComponent_id}-update/`
                        var deleteUrl = `BOM_component_list/${log.BOMComponent_id}-delete/`

                        var logIndex = index + 1;

                        $('#logs-table-body').append(`
                                <tr>
                                    <td>${logIndex}</td>
                                    <td>${log.product}</td>
                                    <td>${log.raw_material_component}</td>
                                    <td>${log.quantity_used}</td>
                                    <td>${formattedCreateDate}</td>
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
                        $('#logs-table-body a.modal-link').css('cursor', 'pointer');

                    });
                },
                error: function (error) {
                    console.log('Error:', error);
                }
            });
        };

        $('#filter-label').on('change', 'label', function () {
            var itemCode = $(this).data('itemcode');

            // Remove the icon from all labels
            $('#filter-label label .fa-filter').remove();

            if ($(this).prop('checked')) {
                // Find the label by the "for" attribute related to the clicked radio button
                var label = $('label[for="' + $(this).attr('id') + '"]');
                
                // Append the icon to the specific label
                label.prepend('<i class="fa-solid fa-filter me-1"></i>');
            }

            loadItemCode(itemCode);
        });

        // Event listener for radio button clicks, you might still use it independently if needed
        $('#filter-label').on('change', 'input[type="radio"]', function () {
            var itemCode = $(this).data('itemcode');
            
            // Remove the icon from all labels
            $('#filter-label label .fa-filter').remove();

            if ($(this).prop('checked')) {
                // Find the label by the "for" attribute related to the clicked radio button
                var label = $('label[for="' + $(this).attr('id') + '"]');
                
                // Append the icon to the specific label
                label.prepend('<i class="fa-solid fa-filter me-1"></i>');
            }

            loadItemCode(itemCode);
        });
    });
}