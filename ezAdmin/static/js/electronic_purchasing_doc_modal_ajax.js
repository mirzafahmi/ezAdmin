function generateElectronicInventoryModals(element) {
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

        function formatCustomDate(dateString) {
            if (dateString) {
                var date = new Date(dateString);
                var options = { month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
                return new Intl.DateTimeFormat('en-US', options).format(date);
            } else {
                return 'None';
            }
        }

        $(document).on('click', '.modal-link', function () {
            var element = this;
            var purchasingDoc = element.getAttribute('data-purchasing-doc-id');

            $.ajax({
                url: baseUrl,
                method: 'GET',
                data: {
                    purchasing_doc: purchasingDoc,
                },
                dataType: "json",
                success: function (data) {
                    $('#staticBackdropLabel').text('');
                    $('#staticBackdropLabel').append(`Purchasing Document Details For ${data[0].po_number}`);
                    data.forEach(function (log) {
                        var formattedCreateDate = formatCustomDate(log.create_date)
                        
                        var poDocUrl = '/media/' + log.po_doc;
                        var invoiceDocUrl = '/media/' + log.invoice_doc;
                    
                        $('#purchasingDocModal').empty();
                        $('#purchasingDocModal').append(
                            `<tr>
                                <td>${log.supplier}</td>
                                <td><a href=${poDocUrl} target="_blank">${log.po_number}</a></td>
                                <td><a href=${invoiceDocUrl} target="_blank">${log.invoice_number}</a></td>
                                <td>${formattedCreateDate}</td>
                            </tr>`
                        );
                    });
                },
                error: function (error) {
                    console.log('Error:', error);
                }
            });
        });
    })
}  