import cv2
import pickle
import os
import face_recognition
import pandas as pd
import pyttsx3

# Load face encodings and names
data_directory = 'data/'
with open(os.path.join(data_directory, 'face_encodings.pkl'), 'rb') as f:
    face_encodings = pickle.load(f)
with open(os.path.join(data_directory, 'names.pkl'), 'rb') as f:
    names = pickle.load(f)

# Initialize video capture
video = cv2.VideoCapture(0)

# Load and prepare background image
background_image_path = r"C:\Users\alaaj\Desktop\reserch\bedaa\3\background.png"
background = cv2.imread(background_image_path)
if background is None:
    print("Error: Background image could not be loaded.")
    video.release()
    cv2.destroyAllWindows()
    exit()

# Initialize attendance DataFrame
attendance_df = pd.DataFrame(columns=["Name", "Time"])

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to take attendance
def take_attendance(name):
    current_time = pd.Timestamp.now()
    attendance_df.loc[len(attendance_df)] = [name, current_time]

# Function to announce attendance
def announce_attendance(recognized_names):
    if recognized_names:
        names_list = ', '.join(recognized_names)
        engine.say(f"Attendance taken for {names_list}.")
        engine.runAndWait()

# Function to show attendance log
def show_attendance_log():
    print(attendance_df)
    # Save to Excel file
    attendance_df.to_excel("attendance_log.xlsx", index=False)
    # Open the Excel file
    os.startfile("attendance_log.xlsx")

# Get the width and height of the camera frame
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Resize the background to match the screen size
screen_width = 1920  # Set your screen width here
screen_height = 1080  # Set your screen height here
background_resized = cv2.resize(background, (screen_width, screen_height))

# Create a fullscreen window
cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

recognized_names = []  # List to hold recognized names for attendance

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Unable to read from camera.")
        break

    # Position the frame at the bottom-right corner
    x_offset = 200
    y_offset = 450

    # Overlay the background
    frame_with_background = background_resized.copy()

    # Place the current frame at the bottom-right corner of the background
    frame_with_background[y_offset:y_offset + frame_height, x_offset:x_offset + frame_width] = frame

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for face_recognition
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings_frame = face_recognition.face_encodings(rgb_frame, face_locations)

    # Reset recognized names for the current frame
    recognized_names.clear()

    for face_location, face_encoding in zip(face_locations, face_encodings_frame):
        matches = face_recognition.compare_faces(face_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = names[first_match_index]

            # Add the recognized name to the list
            recognized_names.append(name)

        # Draw rectangle and label on the background frame
        (top, right, bottom, left) = face_location
        top = top + y_offset  # Adjust for y offset
        bottom = bottom + y_offset  # Adjust for y offset
        left = left + x_offset  # Adjust for x offset
        right = right + x_offset  # Adjust for x offset
        
        cv2.rectangle(frame_with_background, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame_with_background, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Frame", frame_with_background)

    # Check for key presses
    key = cv2.waitKey(1) & 0xFF
    if key == ord('i'):  # Press 'i' to take attendance
        for name in recognized_names:
            take_attendance(name)
        announce_attendance(recognized_names)  # Announce after taking attendance
    
    if key == ord('f'):  # Press 'f' to show attendance log
        show_attendance_log()

    if key == ord('q') or key == ord('e'):  # Press 'q' or 'e' to exit
        break

# Release video and destroy windows
video.release()
cv2.destroyAllWindows()
