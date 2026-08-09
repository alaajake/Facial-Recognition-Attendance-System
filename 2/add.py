import cv2
import pickle
import numpy as np
import os
import face_recognition

# Create data directory if it doesn't exist
data_directory = 'data/'
os.makedirs(data_directory, exist_ok=True)  # This will create the directory if it doesn't exist

# Initialize video capture
video = cv2.VideoCapture(0)

# Prepare a list to hold face encodings and names
face_encodings = []
names = []

# Get the user’s name
name = input("Enter Your Name: ")

# Capture frames and detect faces
print("Press 'q' to exit and save faces.")
while True:
    ret, frame = video.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for face_recognition
    face_locations = face_recognition.face_locations(rgb_frame)
    
    for face_location in face_locations:
        top, right, bottom, left = face_location
        # Encode the face
        face_encoding = face_recognition.face_encodings(rgb_frame, [face_location])[0]
        face_encodings.append(face_encoding)
        names.append(name)

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (left, top), (right, bottom), (50, 50, 255), 2)

    # Show the number of faces captured and the frame
    cv2.putText(frame, f'Faces captured: {len(face_encodings)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q') or len(face_encodings) >= 100:
        break

# Release video capture and close windows
video.release()
cv2.destroyAllWindows()

# Save the encodings and names
with open(os.path.join(data_directory, 'face_encodings.pkl'), 'wb') as f:
    pickle.dump(face_encodings, f)

with open(os.path.join(data_directory, 'names.pkl'), 'wb') as f:
    pickle.dump(names, f)

print("Face data saved successfully.")
