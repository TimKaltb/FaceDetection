// Declare variables to store references to video, canvas, and name input elements
let video;
let canvas;
let nameInput;

// Function to initialize the application
function init() {
    // Get references to video, canvas, and name input elements
    video = document.getElementById("video");
    canvas = document.getElementById("canvas");
    nameInput = document.getElementById("name");

    // Access user's webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            // Set the video element's source to the stream from the webcam
            video.srcObject = stream;
        })
        .catch(error => {
            // Log error and show alert if access to webcam is denied
            console.log("error accessing webcam", error);
            alert("Can't Access Webcam");
        });
}

// Function to capture an image from the video feed
function capture() {
    const context = canvas.getContext("2d");
    // Draw the current frame from the video onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    // Show the canvas and hide the video element
    canvas.style.display = "block";
    video.style.display = "none";
}

// Function to register user with name and photo
function register() {
    // Get the user's name and photo data from input elements
    const name = nameInput.value;
    const photo = dataURItoBlob(canvas.toDataURL());

    // Validate input
    if (!name || !photo) {
        alert("Please provide your name and photo");
        return;
    }

    // Create FormData object to send name and photo data to server
    const formData = new FormData();
    formData.append("name", name);
    formData.append("photo", photo, `${name}.jpg`);

    // Send registration data to server
    fetch("/register", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Show success or failure message based on server response
            if (data.success) {
                alert("Information Successfully Registered");
                // Redirect to homepage
                window.location.href = "/";
            } else {
                alert("Failed to Register");
            }
        })
        .catch(error => {
            // Log any errors that occur during registration process
            console.log("error", error);
        });
}

// Function to log in user using captured photo
function login() {
    const context = canvas.getContext("2d");
    // Capture the current frame from video and convert to photo data
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const photo = dataURItoBlob(canvas.toDataURL());

    // Validate input
    if (!photo) {
        alert("Please provide a photo");
        return;
    }

    // Create FormData object to send photo data to server for login
    const formData = new FormData();
    formData.append("photo", photo, "login.jpg");

    // Send login photo data to server
    fetch("/login", {
        method: "POST",
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Show success message and redirect to homepage if login successful
            console.log(data);
            if (data["Login Successful"]) {
                alert("Login Successful"); // Add an alert when login is successful
                // Redirect to success page
                window.location.href = "/success?user_name=" + data["name"];
            } else {
                alert("Login Unsuccessful"); // Add an alert when login is unsuccessful
            }
        })
        .catch(error => {
            // Log any errors that occur during login process
            console.log("error", error);
            alert("An error occurred during login"); // Add an alert for errors
        });
}


// Function to convert data URI to Blob
function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(",")[1]);
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];

    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
}

// Call init function when DOM content is loaded
document.addEventListener("DOMContentLoaded", function() {
    init();

    // Attach event listeners to buttons and trigger alerts
    document.getElementById("captureBtn").addEventListener("click", function() {
        alert("Capture button clicked");
        capture();
    });

    document.getElementById("registerBtn").addEventListener("click", function() {
        alert("Register button clicked");
        register();
    });

    document.getElementById("loginBtn").addEventListener("click", function() {
        alert("Login button clicked");
        login();
    });
});

