function generateModals(element) {
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
            console.log(purchasingDoc)

            $.ajax({
                url: baseUrl,
                method: 'GET',
                data: {
                    identifier_id: identifierId,
                    component_id: componentId,
                    purchasing_doc: purchasingDoc,
                },
                dataType: "json",
                success: function (data) {
                    data.forEach(function (log) {
                        var formattedCreateDate = formatCustomDate(log.create_date)
                        
                        var poDocUrl = '/media/' + log.po_doc;
                        var invoiceDocUrl = '/media/' + log.invoice_doc;
                        var plDocUrl = '/media/' + log.pl_doc;
                        var k1DocUrl = '/media/' + log.k1_doc;
                        var awbDocUrl = '/media/' + log.AWB_doc;

                        console.log(awbDocUrl);
                        $('#staticBackdropLabel').append(`Purchasing Document Details For ${log.po_number}`);
                        $('#purchasingDocModal').empty();
                        $('#purchasingDocModal').append(
                            `<tr>
                                <td>${log.supplier}</td>
                                <td><a href=${poDocUrl} target="_blank">${log.po_number}</a></td>
                                <td><a href=${invoiceDocUrl} target="_blank">${log.invoice_number}</a></td>
                                <td><a href=${plDocUrl} target="_blank">${log.packing_list}</a></td>
                                <td><a href=${k1DocUrl} target="_blank">${log.k1_form}</a></td>
                                <td><a href=${awbDocUrl} target="_blank">${log.AWB_number}</a></td>
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

    