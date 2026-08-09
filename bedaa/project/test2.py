from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
import face_recognition  # Requires dlib and face_recognition libraries
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import subprocess

def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

# Initialize video capture and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load face data and labels
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Dimensionality reduction with PCA
pca = PCA(n_components=50)  # Adjust based on the dataset and desired accuracy
FACES_pca = pca.fit_transform(FACES)

# Fit the KNN classifier with reduced dimensions
knn = KNeighborsClassifier(n_neighbors=3)  # Try lower k if confusion persists
knn.fit(FACES_pca, LABELS)

imgBackground = cv2.imread("background.png")
COL_NAMES = ['NAME', 'TIME']

last_capture_time = 0
capture_interval = 5
last_attendance_file = ""

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        
        # Convert to RGB and use face_recognition for embedding
        rgb_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_img)

        if encodings:
            face_encoding = encodings[0]
            face_pca = pca.transform([face_encoding])  # Reduce dimensions for KNN

            output = knn.predict(face_pca)
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
            cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
            cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

            attendance = [str(output[0]), str(timestamp)]

    # Display the video frame with face detection
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)

    if k == ord('i') and (time.time() - last_capture_time) > capture_interval:
        message = f"Attendance taken for {output[0]}."
        speak(message)
        last_capture_time = time.time()
        
        last_attendance_file = "Attendance/Attendance_" + date + ".csv"
        with open(last_attendance_file, "+a") as csvfile:
            writer = csv.writer(csvfile)
            if not exist:
                writer.writerow(COL_NAMES)
            writer.writerow(attendance)
    
    if k == ord('f') and last_attendance_file:
        subprocess.Popen(['start', last_attendance_file], shell=True)
        time.sleep(1)

    if k == ord('e') or k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
