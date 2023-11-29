
function componentLogFilter() {
    $(document).ready(function () {
        $.ajax({
            url: baseUrl,
            method: 'GET',
            dataType: "json",
            success: function (data) {
                console.log(data);
                data.forEach(function (log) {
                    logWithUnderScore = log.replace(/ /g, '-');
                    $('#filter-label').append(
                        `<input type="radio" class="btn-check" id="${logWithUnderScore}-identifier" name="vbtn-radio" data-identifier="${log}">` +
                        `<label class="btn btn-outline-primary me-1" for="${logWithUnderScore}-identifier"><a class="no-decoration">${log}</a></label>`
                    );
                });
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });

        function loadLogs(identifier) {
            $.ajax({
                url: baseUrl,
                method: 'GET',
                data: {
                    identifier_name: identifier,
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

                    $('#table-footer').empty();
                    if (data.length <= 0) {
                        $('#table-footer').empty();
                        $('#table-footer').append(`
                            <tr class="table-group-divider">
                                <td colspan="6" class="fw-bold">
                                    <hr>
                                    No Components available, please add in
                                    <hr>
                                </td>
                            </tr>
                        `);
                    }
                    
                    $('#logs-table-body').empty();
                    data.forEach(function (log, index) {
                        var formattedCreateDate = formatCustomDate(log.create_date);
                        

                        var editUrl = `raw_material_component_list/${log.component_id}-update/`
                        var deleteUrl = `raw_material_component_list/${log.component_id}-delete/`

                        var logIndex = index + 1;

                        $('#logs-table-body').append(`
                                <tr>
                                    <td>${logIndex}</td>
                                    <td>${log.identifier}</td>
                                    <td>${log.component}</td>
                                    <td>${log.specifications == null? 'None': log.specifications}</td>
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
            var identifier = $(this).data('identifier');

            // Remove the icon from all labels
            $('#filter-label label .fa-filter').remove();

            if ($(this).prop('checked')) {
                // Find the label by the "for" attribute related to the clicked radio button
                var label = $('label[for="' + $(this).attr('id') + '"]');
                
                // Append the icon to the specific label
                label.prepend('<i class="fa-solid fa-filter me-1"></i>');
            }

            loadLogs(identifier);
        });

        // Event listener for radio button clicks, you might still use it independently if needed
        $('#filter-label').on('change', 'input[type="radio"]', function () {
            var identifier = $(this).data('identifier');
            
            // Remove the icon from all labels
            $('#filter-label label .fa-filter').remove();

            if ($(this).prop('checked')) {
                // Find the label by the "for" attribute related to the clicked radio button
                var label = $('label[for="' + $(this).attr('id') + '"]');
                
                // Append the icon to the specific label
                label.prepend('<i class="fa-solid fa-filter me-1"></i>');
            }

            loadLogs(identifier);
        });
    })
}
