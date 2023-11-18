function CustomAlert() {
    this.init = function () {
        // Create the dialog elements only once
        document.body.innerHTML += '<div id="dialogoverlay"></div><div id="dialogbox"><div><div id="dialogboxhead"></div><div id="dialogboxbody"></div><div id="dialogboxfoot"></div>';
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
        
        // Queue to store alert details
        this.alertQueue = [];
        console.log(this.alertQueue);
    };

    this.alert = function (message, title, redirectUrl) {
        // Add the alert details to the queue
        this.alertQueue.push({ message, title, redirectUrl });
        
        // Show the next alert
        this.showNextAlert();
    };

    this.showNextAlert = function () {
        if (this.alertQueue.length > 0) {
            // Show the dialog
            let dialogoverlay = document.getElementById('dialogoverlay');
            let dialogbox = document.getElementById('dialogbox');
            dialogoverlay.style.display = "block";
            dialogbox.style.display = "block";
            document.getElementById('dialogboxhead').style.display = 'block';

            // Get the next alert details from the queue
            let alertDetails = this.alertQueue.shift();
            let message = alertDetails.message;
            let title = alertDetails.title;
            let redirectUrl = alertDetails.redirectUrl;

            dialogbox.dataset.redirectUrl = redirectUrl;

            if (typeof title === 'undefined') {
                document.getElementById('dialogboxhead').style.display = 'none';
            } else {
                document.getElementById('dialogboxhead').innerHTML = '<i class="fa fa-exclamation-circle me-2" aria-hidden="true"></i> ' + title;
            }

            document.getElementById('dialogboxbody').innerHTML = message;
            

        }
    };

    this.ok = function () {
        // Hide the dialog
        let dialogbox = document.getElementById('dialogbox');
        let dialogoverlay = document.getElementById('dialogoverlay');
        dialogbox.style.display = "none";
        dialogoverlay.style.display = "none";
    
        // Check if it's the last alert and perform redirection
        console.log(this.alertQueue.length)

        let redirectUrl = dialogbox.dataset.redirectUrl;
        console.log(redirectUrl)
        if (this.alertQueue.length === 0 && redirectUrl != 'undefined') {
            window.location.href = redirectUrl;
        } else {
            // Show the next alert in the queue
            this.showNextAlert();
        }
    };
}


