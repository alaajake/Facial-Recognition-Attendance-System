import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
import face_recognition

def speak(message):
    """Use TTS to speak the provided message."""
    speaker = Dispatch(("SAPI.SpVoice"))
    speaker.Speak(message)

# Create directories if they don't exist
data_directory = 'data/'
attendance_directory = 'Attendance/'
os.makedirs(data_directory, exist_ok=True)  # Ensure data directory exists
os.makedirs(attendance_directory, exist_ok=True)  # Ensure attendance directory exists

# Load face encodings and names
with open(os.path.join(data_directory, 'face_encodings.pkl'), 'rb') as f:
    face_encodings = pickle.load(f)
with open(os.path.join(data_directory, 'names.pkl'), 'rb') as f:
    names = pickle.load(f)

# Initialize video capture
video = cv2.VideoCapture(0)

# Load background image using the full path
background_image_path = r"C:\Users\alaaj\Desktop\reserch\bedaa\2\background.png"
imgBackground = cv2.imread(background_image_path)
if imgBackground is None:
    print("Error: Background image not found.")
    exit()

# Set video capture resolution
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables to track attendance capture timing
last_capture_time = 0
capture_interval = 5  # seconds
col_names = ['NAME', 'TIME']
frame_skip = 2  # Process every nth frame
frame_count = 0

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Unable to read from camera.")
        break

    frame_count += 1
    if frame_count % frame_skip != 0:  # Skip processing for most frames
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for face_recognition
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings_frame = face_recognition.face_encodings(rgb_frame, face_locations)

    attendance_record = None  # Reset the attendance record each frame

    for face_location, face_encoding in zip(face_locations, face_encodings_frame):
        top, right, bottom, left = face_location

        # Set minimum face size to filter out smaller detections
        if (right - left) < 50 or (bottom - top) < 50:  # Adjust this value based on your requirements
            continue  # Skip if the detected area is too small to be a face
        
        # Compare to known faces
        matches = face_recognition.compare_faces(face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(face_encodings, face_encoding)
        name = "Unknown"
        
        # Use a threshold for confidence
        threshold = 0.6  # Adjust this value based on your testing
        if any(matches):
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] < threshold:
                name = names[best_match_index]

        # Draw rectangles and label on the frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        # Prepare attendance record
        current_time = datetime.now()
        date_str = current_time.strftime("%d-%m-%Y")
        timestamp_str = current_time.strftime("%H:%M:%S")
        attendance_record = [name, timestamp_str]

    # Overlay the frame on the background at a specified position
    imgBackground[162:162 + 480, 55:55 + 640] = frame

    cv2.imshow("Frame", imgBackground)

    # Handle keypresses for attendance capture and exit
    k = cv2.waitKey(1)

    # Check if 'i' is pressed and enough time has passed since the last capture
    if k == ord('i') and (time.time() - last_capture_time) > capture_interval and attendance_record:
        speak(f"Attendance taken for {attendance_record[0]}.")
        last_capture_time = time.time()

        # Prepare to save attendance data
        last_attendance_file = os.path.join(attendance_directory, f"Attendance_{date_str}.csv")
        file_exists = os.path.isfile(last_attendance_file)

        with open(last_attendance_file, "a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(col_names)  # Write header if the file is new
            writer.writerow(attendance_record)  # Write attendance record

    # Quit the program by pressing 'E' or 'Q'
    if k == ord('e') or k == ord('q'):
        break

# Release video and destroy windows
video.release()
cv2.destroyAllWindows()
