from sklearn.neighbors import KNeighborsClassifier
import cv2
import face_recognition
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import subprocess

def speak(message):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(message)

# Initialize video capture
video = cv2.VideoCapture(0)

# Load known face encodings and labels
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/face_encodings.pkl', 'rb') as f:
    KNOWN_ENCODINGS = pickle.load(f)

# Check for data consistency
if len(KNOWN_ENCODINGS) != len(LABELS):
    print("Mismatch between known encodings and labels.")
    LABELS = LABELS[:len(KNOWN_ENCODINGS)]
    print(f"Truncated labels to match encodings. New label count: {len(LABELS)}")

# Prepare attendance tracking
imgBackground = cv2.imread("background.png")
COL_NAMES = ['NAME', 'TIME']
last_capture_time = 0
capture_interval = 5  # 5 seconds interval for attendance
last_attendance_file = ""

while True:
    ret, frame = video.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # Resize for faster processing
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations and encodings in the frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Match against known faces
        matches = face_recognition.compare_faces(KNOWN_ENCODINGS, face_encoding)
        face_distances = face_recognition.face_distance(KNOWN_ENCODINGS, face_encoding)
        
        # Find the closest match
        best_match_index = np.argmin(face_distances) if matches else None

        # Label the recognized face
        if best_match_index is not None and matches[best_match_index]:
            name = LABELS[best_match_index]
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            attendance = [name, timestamp]
            
            # Draw box and label on original frame
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            # Record attendance
            if (time.time() - last_capture_time) > capture_interval:
                speak(f"Attendance taken for {name}")
                last_capture_time = time.time()
                last_attendance_file = f"Attendance/Attendance_{date}.csv"

                if not os.path.isfile(last_attendance_file):
                    with open(last_attendance_file, "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(COL_NAMES)
                
                with open(last_attendance_file, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)

    # Display the video frame with face detection
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame", imgBackground)

    # Handle keypresses
    k = cv2.waitKey(1)
    if k == ord('f') and last_attendance_file:
        subprocess.Popen(['start', last_attendance_file], shell=True)
    if k == ord('e') or k == ord('q'):
        break

# Release video and close windows
video.release()
cv2.destroyAllWindows()
