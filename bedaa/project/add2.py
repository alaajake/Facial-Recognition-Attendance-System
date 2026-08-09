import cv2
import pickle
import numpy as np
import os

# Initialize video capture and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0
name = input("Enter Your Name: ")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50))

        # Collect face data every 10 frames until reaching 100 samples
        if len(faces_data) < 100 and i % 10 == 0:
            faces_data.append(resized_img)

        i += 1

        # Display the number of faces collected
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1)
    if k == ord('q') or len(faces_data) >= 100:
        break

video.release()
cv2.destroyAllWindows()

# Convert collected face data to a NumPy array and reshape
faces_data = np.asarray(faces_data).reshape(100, -1)

# Function to save names
def save_names(name):
    if os.path.exists('data/names.pkl'):
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        names += [name] * 100
    else:
        names = [name] * 100

    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

# Function to save face data
def save_faces_data(faces_data):
    if os.path.exists('data/faces_data.pkl'):
        with open('data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        faces = np.append(faces, faces_data, axis=0)
    else:
        faces = faces_data

    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

# Save names and face data
save_names(name)
save_faces_data(faces_data)
