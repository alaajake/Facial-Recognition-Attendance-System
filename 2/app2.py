import cv2
import pickle
import os
import face_recognition
import serial
import time
import pyttsx3

# Serial setup to communicate with Arduino
arduino = serial.Serial('COM14', 9600)  # Adjust COM port if needed
time.sleep(2)  # Allow time for Arduino to initialize

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speaking speed if necessary

# Load face encodings and names
data_directory = 'data/'
with open(os.path.join(data_directory, 'face_encodings.pkl'), 'rb') as f:
    face_encodings = pickle.load(f)
with open(os.path.join(data_directory, 'names.pkl'), 'rb') as f:
    names = pickle.load(f)

# Initialize video capture
video = cv2.VideoCapture(0)

# Load and prepare background image
background_image_path = 'background.png'
background = cv2.imread(background_image_path)
if background is None:
    print("Error: Background image could not be loaded.")
    video.release()
    cv2.destroyAllWindows()
    exit()

# Get the width and height of the camera frame
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Resize the background to match the screen size
screen_width = 1920
screen_height = 1080
background_resized = cv2.resize(background, (screen_width, screen_height))

# Create a fullscreen window
cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

attendance_taken = False
recognized_name = ""

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Unable to read from camera.")
        break

    x_offset = 200
    y_offset = 450

    # Overlay the background
    frame_with_background = background_resized.copy()
    frame_with_background[y_offset:y_offset + frame_height, x_offset:x_offset + frame_width] = frame

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings_frame = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_location, face_encoding in zip(face_locations, face_encodings_frame):
        matches = face_recognition.compare_faces(face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = names[first_match_index]
            recognized_name = name

        # Draw rectangle and label on the background frame
        (top, right, bottom, left) = face_location
        top += y_offset
        bottom += y_offset
        left += x_offset
        right += x_offset
        cv2.rectangle(frame_with_background, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame_with_background, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Frame", frame_with_background)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('i') and recognized_name:
        attendance_taken = True
        date_str = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Send name and date to Arduino
        arduino.write(f"{recognized_name}\n".encode())
        arduino.write(f"{date_str}\n".encode())
        
        # Text-to-speech for attendance confirmation
        engine.say(f"Attendance taken for {recognized_name}")
        engine.runAndWait()  # Blocks until the speech is done
        print(f"Attendance taken for {recognized_name} at {date_str}")

# Release video and close all windows
video.release()
cv2.destroyAllWindows()
