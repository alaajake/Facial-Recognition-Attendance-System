import cv2
import numpy as np
import os
import pickle
import face_recognition

# Create directories if they don't exist
data_directory = 'data/'
os.makedirs(data_directory, exist_ok=True)

# Initialize video capture
video = cv2.VideoCapture(0)
face_encodings = []
names = []

# Get user input for the name
name = input("Enter Your Name: ")

# Set the target number of frames to capture
target_frames = 100
frames_captured = 0

print("Capturing faces... Press 'q' to quit early.")

while frames_captured < target_frames:
    ret, frame = video.read()
    if not ret:
        print("Error: Unable to read from camera.")
        break

    # Convert the image from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings_frame = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_encodings_frame) > 0:  # If faces are detected
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_frame):
            # Draw rectangle around detected face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # Append the face encoding and name to their respective lists
            face_encodings.append(face_encoding)
            names.append(name)
            frames_captured += 1  # Increment the captured frames counter
            print(f"Captured face for {name}! {frames_captured}/{target_frames} frames.")

            # Show progress percentage
            percentage = (frames_captured / target_frames) * 100
            cv2.putText(frame, f"Progress: {percentage:.2f}%", (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Display the frame with rectangles and labels
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video and close windows
video.release()
cv2.destroyAllWindows()

# Check if faces were captured
if len(face_encodings) == 0:
    print("No faces were captured. Exiting...")
else:
    # Save face encodings and names
    face_encodings = np.array(face_encodings)  # Convert to numpy array
    print("Saving captured face data...")

    # Load existing encodings if they exist
    if os.path.exists(os.path.join(data_directory, 'face_encodings.pkl')):
        with open(os.path.join(data_directory, 'face_encodings.pkl'), 'rb') as f:
            existing_encodings = pickle.load(f)
        face_encodings = np.concatenate((existing_encodings, face_encodings))

    # Load existing names if they exist
    if os.path.exists(os.path.join(data_directory, 'names.pkl')):
        with open(os.path.join(data_directory, 'names.pkl'), 'rb') as f:
            existing_names = pickle.load(f)
        names = existing_names + names

    # Save the updated encodings and names
    with open(os.path.join(data_directory, 'face_encodings.pkl'), 'wb') as f:
        pickle.dump(face_encodings, f)

    with open(os.path.join(data_directory, 'names.pkl'), 'wb') as f:
        pickle.dump(names, f)

    print("Face data saved successfully!")
