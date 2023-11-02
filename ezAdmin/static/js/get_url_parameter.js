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

export { getUrlParameter };