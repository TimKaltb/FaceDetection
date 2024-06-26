import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template
import face_recognition

app = Flask(__name__)

registered_data = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register",methods=["POST"])
def register():
    name = request.form.get("name")
    photo = request.files['photo']
    uploads_folder = os.path.join(os.getcwd(),"static", "uploads")
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    photo.save(os.path.join(uploads_folder,f'{datetime.date.today()}_{name}.jpg'))
    registered_data[name] = f"{datetime.date.today()}_name{name}.jpg"

    response = {"success":True,'name':name}
    return jsonify(response)


    # Validating file type
    #if photo.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
     #   return jsonify({"error": "Invalid file format. Only JPG, JPEG, and PNG files are allowed."}), 400

    #filename = f'{datetime.date.today()}_{name}.jpg'
    #file_path = os.path.join(uploads_folder, filename)
    #photo.save(file_path)

    #registered_data[name] = filename

    #response = {"Registration successful": True, 'name': name}
    #return jsonify(response)

@app.route("/login",methods=["POST"])
def login():
    photo = request.files['photo']

    uploads_folder = os.path.join(os.getcwd(),"static", "uploads")
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    login_filename = os.path.join(uploads_folder,"login_photo.jpg")
    photo.save(login_filename)

    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalphoto_default.xml")
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

    if len(faces) == 0:
        response = {"success": False}
        return jsonify(response)

    login_image = face_recognition.load_image_file(login_filename)

    login_face_encodings = face_recognition.face_encodings(login_image)

    for name, filename in registered_data.items():
        registered_photo = os.path.join(uploads_folder, filename)
        
        registered_image = face_recognition.load_image_file(registered_photo)

        registered_face_encodings = face_recognition.face_encodings(registered_image)

        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            matches = face_recognition.compare_uploads(registered_face_encodings, login_face_encodings[0])

            print("matches", matches)
            if any(matches):
                response = {"success": True, "name": name}
                return jsonify(response)
    response = {"success": False}
    return jsonify(response)

@app.route("/success")
def success():
    # Change user_name to name
    user_name = request.args.get("user_name")
    return render_template("success.html", user_name=user_name)

if __name__ == "__main__":
    app.run(debug=True)
