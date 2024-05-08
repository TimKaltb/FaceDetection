import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template
import face_recognition

app = Flask(__name__)

registered_data = {}

# Route to render the index page
@app.route("/")
def index():
    return render_template("website.html")

# Route to handle registration process
@app.route("/register", methods=["POST"])
def register():
    # Get name and face image from the request
    name = request.form.get("name")
    face = request.files['face']
    # Define the folder to save registered faces
    faces_folder = os.path.join(os.getcwd(), "static", "faces")
    if not os.path.exists(faces_folder):
        os.makedirs(faces_folder)

    # Save the registered face image
    face.save(os.path.join(faces_folder, f'{datetime.date.today()}_{name}.jpg'))
    # Store the registration data in a dictionary
    registered_data[name] = f"{datetime.date.today()}_{name}.jpg"

    # Return JSON response indicating successful registration
    message = {"Login Succesful": True, 'name': name}
    return jsonify(message)

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
        # If no face detected, return login failure response
        response = {"Login Successful": False}
        return jsonify(response)

    # Load the login image for face recognition
    login_image = face_recognition.load_image_file(login_filename)
    # Encode the faces in the login image
    login_face_encodings = face_recognition.face_encodings(login_image)

    # Iterate through registered faces for comparison
    for name, filename in registered_data.items():
        registered_face = os.path.join(uploads_folder, filename)
        registered_image = face_recognition.load_image_file(registered_face)

        registered_face_encodings = face_recognition.face_encodings(registered_image)

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            # Compare face encodings to determine if there's a match
            match = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])

            if any(match):
                # If match found, return login success response with the name
                response = {"Login Successful": True, "name": name}
                return jsonify(response)
    # If no match found, return login failure response
    response = {"Login Successful": False}
    return jsonify(response)

# Route to render success page after login
@app.route("/Login Succesful")
def success():
    user_name = request.args.get("user_name")
    return render_template("loginsuccess.html", user_name=user_name)

if __name__ == "__main__":
    app.run(debug=True)
