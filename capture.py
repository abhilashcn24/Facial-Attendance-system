# import face_recognition
# import cv2
# import numpy as np
# import pymongo
# from datetime import datetime



# video_capture = cv2.VideoCapture(0)

# client = pymongo.MongoClient('mongodb://localhost:27017')
# db = client['attendence_system']
# collections = db['students']

# data = collections.find()

# known_faces_data = []
# for i in data:
#     known_faces_data.append({
#         "name":i['name'],
#         "file":f"static/images/{i['img_file']}"
#     })
# known_face_encodings = []
# known_face_names = []

# # Load known faces using a loop
# for face_data in known_faces_data:
#     img = face_recognition.load_image_file(face_data["file"])
    
#     # Check if any faces were found in the image
#     face_encodings = face_recognition.face_encodings(img)
    
#     if face_encodings:
#         # Use the first detected face encoding
#         face_encoding = face_encodings[0]
#         known_face_encodings.append(face_encoding)
#         known_face_names.append(face_data["name"])
#     else:
#         print(f"No face found in {face_data['file']}")


# # Get the current date and time
# current_datetime = datetime.now()
# formatted_datetime = current_datetime.strftime("%d-%m-%Y,%H:%M:%S")

# date = formatted_datetime.split(',')
# # Print the formatted date and time
# print("Formatted Date and Time:", formatted_datetime)

# attendece_list = []
# collection2 = db['attendence']
# def mark_attendence(name):
#     if name in attendece_list:
#        print(f"{name} already present")
    
#     else:
#         res = collections.find()
#         data =None
#         for i in res:
#             if i['name'] == name:
#                 data = {
#                     "name":i['name'],
#                     "usn":i['usn'],
#                     "date":date[0],
#                     "time":date[1],
#                     "status":'present'
#                 }
#         print(data)
#         collection2.insert_one(data)
#         attendece_list.append(name)


# def Capture_image():

#     while True:
        
#         _, frame = video_capture.read()
#         rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])

#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

#             name = "Unknown"

#             face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
#             best_match_index = np.argmin(face_distances)
#             print(best_match_index,matches)
#             if matches[best_match_index]:
#                 name = known_face_names[best_match_index]
#                 mark_attendence(name)
#             # Draw a box around the face
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#             # Draw a label with a name below the face
#             cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

#         # Display the resulting image
#         cv2.imshow('Idt Project', frame)

#         # Hit 'q' on the keyboard to quit!
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release handle to the webcam
#     video_capture.release()
#     cv2.destroyAllWindows()

# Capture_image()


import face_recognition
import cv2
import numpy as np
import pymongo
from datetime import datetime

video_capture = cv2.VideoCapture(0)

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['attendence_system']
collections = db['students']

data = collections.find()

known_faces_data = []
for i in data:
    print(i)
    known_faces_data.append({
        "name": i['name'],
        "file": f"static/images/{i['img_file']}"
    })

known_face_encodings = []
known_face_names = []

for face_data in known_faces_data:
    img = face_recognition.load_image_file(face_data["file"])
    face_encodings = face_recognition.face_encodings(img)
    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(face_data["name"])

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%d-%m-%Y,%H:%M:%S")
date = formatted_datetime.split(',')

attendece_list = []
collection2 = db['attendence']

def mark_attendence(name):
    if name in attendece_list:
        return
    res = collections.find()
    data = None
    for i in res:
        if i['name'] == name:
            data = {
                "name": i['name'],
                "usn": i['usn'],
                "date": date[0],
                "time": date[1],
                "status": 'present'
            }
    if data:
        collection2.insert_one(data)
        attendece_list.append(name)

def Capture_image():
    while True:
        _, frame = video_capture.read()
        rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            if face_distances.size == 0:
                continue
            best_match_index = np.argmin(face_distances)
            if matches and matches[best_match_index]:
                name = known_face_names[best_match_index]
                mark_attendence(name)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        cv2.imshow('Idt Project', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

Capture_image()
