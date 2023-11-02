
function componentLogFilter() { 
    $(document).ready(function () { 
        $('#filter-label').on('change', 'label', function () {
            var component = $(this).data('component');
            loadLogs(component);
        });

        // Event listener for radio button clicks, you might still use it independently if needed
        $('#filter-label').on('change', 'input[type="radio"]', function () {
            var component = $(this).data('component');
            loadLogs(component);
        });
            

        function loadLogs(component) {
            $.ajax({
                url: baseUrl,
                method: 'GET',
                data: {
                    component_name: component,
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
                    data.forEach(function (log, index) {
                        var formattedCreateDate = formatCustomDate(log.create_date);
                        

                        var editUrl = `production_main/raw_material_component_list/${log.component_id}-update/`
                        var deleteUrl = `production_main/raw_material_component_list/${log.component_id}-delete/`
                

                        var logIndex = index + 1;

                        $('#logs-table-body').append(`
                                <tr>
                                    <td>${logIndex}</td>
                                    <td>${log.identifier}</td>
                                    <td>${log.component}</td>
                                    <td>${log.specifications}</td>
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
    })
}
