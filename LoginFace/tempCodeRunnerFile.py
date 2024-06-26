import os
import datetime
import cv2
from flask import Flask, jsonify, request, render_template
import face_recognition

app = Flask(__name__)

registered_data = {}

@app.route("/")
def index():
    return render_template("website.html")

@app.route("/register",methods=["POST"])
def register():
    name = request.form.get("name")
    face = request.files['face']
    faces_folder = os.path.join(os.getcwd(),"static", "faces")
    if not os.path.exists(faces_folder):
        os.makedirs(faces_folder)

    face.save(os.path.join(faces_folder,f'{datetime.date.today()}_{name}.jpg'))
    registered_data[name] = f"{datetime.date.today()}_{name}.jpg"

    message = {"Login Succesful":True,'name':name}

@app.route("/login",methods=["POST"])
def login():
    face = request.files['face']

    faces_folder = os.pathjoin(os.getcwd(),"static", "faces")
    if not os.path.exists(faces_folder):
        os.makedirs(faces_folder)

    login_filename = os.path.join(faces_folder,"login_face.jpg")
    face.save(login_filename)

    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(cv2.data.harcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image,scaleFactor=1.1,minNeighbors=5, minSize=(30,30))

    if len(faces) ==0:
        message = {"Login Succesful": False}
        return jsonify(message)
    
    login_image = face_recognition.load_image_file(login_filename)

    login_face_encodings = face_recognition.face_encodings(login_image)
    
    for name,filename in registered_data.items():
        registered_face = os.path.join(faces_folder, filename)
        registered_image = face_recognition.load_image_file(registered_face)

        registered_face_encodings = face_recognition.face_encodings(registered_image)

        if len(registered_face_encodings) >0 and len(login_face_encodings) >0:
            match = face_recognition.compare_faces(registered_face_encodings, login_face_encodings[0])
            
            print("MATCH", match)
            if any(match):
                message = {"Login Succesful":True, "name": name}
                return jsonify(message)
    message = {"Login Succesful":False}
    return jsonify(message)

@app.route("/Login Succesful")
def success():
    user_name = request.args.get("user_name")
    return render_template("loginsuccess.html", user_name=user_name)
if __name__ == "__main__":
    app.run(debug=True)


    









