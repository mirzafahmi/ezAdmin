function CustomAlert() {
    this.init = function () {
        // Create the dialog elements only once
        document.body.innerHTML += '<div id="dialogoverlay"></div><div id="dialogbox" "><div><div id="dialogboxhead"></div><div id="dialogboxbody"></div><div id="dialogboxfoot"></div></div></div>';
        let dialogoverlay = document.getElementById('dialogoverlay');
        let dialogbox = document.getElementById('dialogbox');

        // Set initial styles and hide the dialog
        let winH = window.innerHeight;
        dialogoverlay.style.height = winH + "px";
        dialogbox.style.top = "100px";
        dialogoverlay.style.display = "none";
        dialogbox.style.display = "none";
        document.getElementById('dialogboxhead').style.display = 'none';

        // Add the event handler for the OK button
        document.getElementById('dialogboxfoot').innerHTML = '<button class="pure-material-button-contained active" onclick="customAlert.ok()">OK</button>';
    };

    this.alert = function (message, title) {
        // Show the dialog
        let dialogoverlay = document.getElementById('dialogoverlay');
        let dialogbox = document.getElementById('dialogbox');
        dialogoverlay.style.display = "block";
        dialogbox.style.display = "block";
        document.getElementById('dialogboxhead').style.display = 'block';

        if (typeof title === 'undefined') {
            document.getElementById('dialogboxhead').style.display = 'none';
        } else {
            document.getElementById('dialogboxhead').innerHTML = '<i class="fa fa-exclamation-circle" aria-hidden="true"></i> ' + title;
        }

        document.getElementById('dialogboxbody').innerHTML = message;
    };

    this.ok = function () {
        // Hide the dialog
        let dialogbox = document.getElementById('dialogbox');
        let dialogoverlay = document.getElementById('dialogoverlay');
        dialogbox.style.display = "none";
        dialogoverlay.style.display = "none";
    };
}

