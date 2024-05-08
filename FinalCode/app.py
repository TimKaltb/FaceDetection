# Import necessary libraries
import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template
import face_recognition

# Initialize Flask application
app = Flask(__name__)

# Dictionary to store registered user data
registered_data = {}

# Route to render the index page
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle registration process
@app.route("/register", methods=["POST"])
def register():
    # Retrieve name and photo from the request
    name = request.form.get("name")
    photo = request.files['photo']

    # Create folder to store uploads if it doesn't exist
    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    # Save the photo with the correct filename format and update registered_data dictionary
    registered_data[name] = f"{datetime.date.today()}_{name}.jpg"

    # Uncomment the code for validating the file type
    if photo.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
        return jsonify({"error": "Invalid file format. Only JPG, JPEG, and PNG files are allowed."}), 400

    # Save the photo to the uploads folder
    photo.save(os.path.join(uploads_folder, registered_data[name]))

    # Return success response
    response = {"success": True, 'name': name}
    return jsonify(response)

# Route to handle login process
@app.route("/login", methods=["POST"])
def login():
    # Retrieve photo from the request
    photo = request.files['photo']

    # Create folder to store uploads if it doesn't exist
    uploads_folder = os.path.join(os.getcwd(), "static", "uploads")
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    # Save the login photo to a file
    login_filename = os.path.join(uploads_folder, "login_photo.jpg")
    photo.save(login_filename)

    # Read the login image and convert to grayscale
    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

    # Initialize face cascade classifier and detect faces in the image
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        response = {"Login Successful": False}
        return jsonify(response)

    login_image = face_recognition.load_image_file(login_filename)

    login_face_encodings = face_recognition.face_encodings(login_image)

    for name, filename in registered_data.items():
        registered_face = os.path.join(uploads_folder, filename)
        registered_image = face_recognition.load_image_file(registered_face)

        registered_face_encodings = face_recognition.face_encodings(registered_image)

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            match = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])

            print("MATCH", match)
            if any(match):
                response = {"Login Successful": True, "name": name}
                return jsonify(response)
    response = {"Login Successful": False}
    return jsonify(response)


# Route to render success page
@app.route("/success")
def success():
    # Retrieve user name from request arguments
    user_name = request.args.get("user_name")
    return render_template("success.html", user_name=user_name)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
