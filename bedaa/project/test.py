from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import subprocess  # Import subprocess for opening files

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

# Fix inconsistency: Truncate LABELS to match the number of faces if needed
if FACES.shape[0] != len(LABELS):
    print(f"Inconsistent data: {FACES.shape[0]} faces but {len(LABELS)} labels.")
    LABELS = LABELS[:FACES.shape[0]]
    print(f"Truncated labels to match faces. New labels count: {len(LABELS)}")

print('Shape of Faces matrix --> ', FACES.shape)

# Fit the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background.png")

COL_NAMES = ['NAME', 'TIME']

# Initialize a variable to track the time of the last attendance capture
last_capture_time = 0
capture_interval = 5  # 5 seconds interval for taking attendance
last_attendance_file = ""  # Variable to store the last attendance file path

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
        
        # Draw the detection and the label on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        
        attendance = [str(output[0]), str(timestamp)]
    
    # Display the video frame with face detection
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)
    
    # Handle keypresses for attendance and exit
    k = cv2.waitKey(1)
    
    # Check if the time since the last capture is greater than the interval
    if k == ord('i') and (time.time() - last_capture_time) > capture_interval:
        # Speak the new message with the recognized person's name
        message = f"Attendance taken for {output[0]}."
        speak(message)  # Announce the name
        last_capture_time = time.time()  # Update the last capture time
        
        # Append to the CSV file
        last_attendance_file = "Attendance/Attendance_" + date + ".csv"  # Update the last attendance file path
        if exist:
            with open(last_attendance_file, "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            with open(last_attendance_file, "+a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
    
    # Open the last attendance file when 'F' is pressed
    if k == ord('f') and last_attendance_file:
        subprocess.Popen(['start', last_attendance_file], shell=True)  # Use 'start' to open the file
        time.sleep(1)  # Pause briefly to allow the command to execute

    # Quit the program by pressing 'E' or 'Q'
    if k == ord('e') or k == ord('q'):
        break

# Release video and destroy windows
video.release()
cv2.destroyAllWindows()
