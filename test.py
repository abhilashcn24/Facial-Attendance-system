import face_recognition
import cv2
import numpy as np
import pymongo

video_capture = cv2.VideoCapture(0)

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['attendence_system']
collections = db['students']

data = collections.find()

known_faces_data = []
for i in data:
    known_faces_data.append({
        "name":i['name'],
        "file":f"static/images/{i['img_file']}"
    })
known_face_encodings = []
known_face_names = []

# Load known faces using a loop
for face_data in known_faces_data:
    img = face_recognition.load_image_file(face_data["file"])
    
    # Check if any faces were found in the image
    face_encodings = face_recognition.face_encodings(img)
    
    if face_encodings:
        # Use the first detected face encoding
        face_encoding = face_encodings[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(face_data["name"])
    else:
        print(f"No face found in {face_data['file']}")


def generate(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    rame = buffer.tobytes()
    yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

while True:
    
    ret, frame = video_capture.read()
    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        print(best_match_index,matches)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
        generate(frame)

