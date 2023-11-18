function performAjaxAction() {
  $(document).ready(function () {
    divCheckboxField = document.getElementById('div_id_data_overide');
    divCheckboxField.classList.add('form-switch');
    var checkboxField = $("#id_data_overide");
    var quantityField = $("#id_quantity");
    
    // Function to set the readonly state based on a flag
    function setReadonlyState(flag, stockType) {
      if (stockType === "2") {
        if (flag) {
          $("#id_purchasing_doc").addClass("disabled-dropdown");
          $("#id_lot_number").addClass("disabled-dropdown");
          $("#id_exp_date").addClass("disabled-dropdown");
          $("#id_price_per_unit").addClass("disabled-dropdown");
        } else {
          $("#id_lot_number").removeClass("disabled-dropdown");
        }
      }
    }

    // Check the local storage for the readonly flag
    var readonlyFlag = localStorage.getItem("readonlyFlag");

    // If the flag is set, apply readonly state
    if (readonlyFlag === "true") {
      setReadonlyState(true, stockType);
      checkboxField.prop("checked", false);
    }

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
    var inventory_log = getUrlParameter("log");
    console.log(inventory_log);
    function fetchDataBasedOnLotNumber() {
      var initialQuantity = $('#id_quantity').val();
      var initialLotNumber = $('#id_lot_number').val();

      $('#id_lot_number').change(function () {
      var lotNumber= $(this).val();  // Get the selected value
      
      // Make an AJAX request to get data based on the client's choice
      $.ajax({
          url: baseUrl,
          method: 'GET',
        data: {
            component_id: componentId,
            lot_number: lotNumber,
            type: stockType,
            inventory_log: inventory_log !== null ? inventory_log : null,
          }, 
          success: function (data) {
            $("#id_exp_date").val(data.exp_date);
            $("#id_price_per_unit").val(data.price_per_unit);
            $("#id_purchasing_doc").val(data.purchasing_doc);
            $('#id_stock_in_tag').val(data.stock_in_tag);

            setReadonlyState(false, stockType);
            localStorage.setItem("readonlyFlag", "false");

            
            if (action === "update" && initialLotNumber == lotNumber) {
              $('#id_quantity').attr('placeholder', 'Maximum quantity available is ' + data.available_quantity + ' pcs');
            } else {
              $('#id_quantity').attr('placeholder', 'Maximum quantity available is ' + parseInt(data.available_quantity) +' pcs');
            }
          },
        error: function () {
            console.log("Error fetching FIFO information for this lot number choice.");
          }
        });
      });
    }
    
    if (action === "create") {
      function fetchComponentOptions(identifierId, componentId, stockType) {

        // Set readonly state and store the flag in local storage
        if (stockType === "2") {
          $.ajax({
            url: baseUrl, // Replace with your actual endpoint
            method: "GET",
            data: {
              identifier_id: identifierId,
              component_id: componentId,
              type: stockType,
            },
            dataType: "json",
            success: function (data) {
              // Update form fields with retrieved information
              $("#id_lot_number").val(data.lot_number);
              $("#id_exp_date").val(data.exp_date);
              $("#id_price_per_unit").val(data.price_per_unit);
              $("#id_purchasing_doc").val(data.purchasing_doc);
              $('#id_stock_in_tag').val(data.stock_in_tag);

              // Set readonly state and store the flag in local storage
              setReadonlyState(true, stockType);
              localStorage.setItem("readonlyFlag", "true");

              var availableQuantity = data.available_quantity;
              var quantityField = $("#id_quantity");
              var selectedQuantity = parseFloat(quantityField.val());

            },
            error: function () {
              console.log("Error fetching FIFO information.");
            },
          });
        } else {
          // If the type is not '2', remove readonly attribute and clear the flag
          setReadonlyState(false, stockType);
          localStorage.removeItem("readonlyFlag");
        }
      }
      if (identifierId && componentId && stockType) {
        if (stockType == '2') {
          fetchComponentOptions(identifierId, componentId, stockType);
          fetchDataBasedOnLotNumber();
          console.log('from create')
        }
      }
    }

    // Listen for changes in the component field
    if (action === "update") {
      if (stockType === "2") {
        fetchDataBasedOnLotNumber();

        // Set readonly state and store the flag in local storage
        setReadonlyState(true, stockType);
        localStorage.setItem("readonlyFlag", "true");

        console.log('from update');
        console.log(localStorage.getItem("readonlyFlag"));
      } else {
        // If the type is not '2', remove readonly attribute and clear the flag
        setReadonlyState(false, stockType);
        localStorage.removeItem("readonlyFlag");
      }
    }

    var checkboxField = $("#id_data_overide");

    // Check if the checkbox is checked
    var isChecked = checkboxField.prop("checked");

    // If the checkbox is checked, uncheck it
    if (isChecked) {
        checkboxField.prop("checked", false);
    }

    checkboxField.on("change", function () {
      if (checkboxField.prop("checked")) {
        setReadonlyState(false, stockType);
      } else {
        setReadonlyState(true, stockType);
      }
    });
  });
}
