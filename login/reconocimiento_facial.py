import cv2
import face_recognition
import numpy as np
from django.conf import settings


import os

MEDIA_DIR = settings.MEDIA_DIR

def load_known_faces():
    known_faces = []
    known_names = []

    known_faces_dir = os.path.join(MEDIA_DIR, "profiles")
    for file_name in os.listdir(known_faces_dir):
        if file_name.endswith(".jpg"):
            image_path = os.path.join(known_faces_dir, file_name)
            face_image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face_image)[0]
            known_faces.append(face_encoding)
            known_names.append(os.path.splitext(file_name)[0])

    return known_faces, known_names

def pipeline_model():
    known_faces, known_names = load_known_faces()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        img = frame.copy()
        face_locations = face_recognition.face_locations(img, model="hog")

        for (starty, endx, endy, startx) in face_locations:
            cv2.rectangle(img, (startx, starty), (endx, endy), (0, 0, 255), 2)
            face_roi = img[starty:endy, startx:endx]
            face_encodings = face_recognition.face_encodings(img, [(starty, endx, endy, startx)])[0]

            matches = face_recognition.compare_faces(known_faces, face_encodings)
            
            face_name = "Unknown"
            face_score = 0.0

            if True in matches:
                first_match_index = matches.index(True)
                face_name = known_names[first_match_index]
                face_score = 1.0

            text_face = "{}:{:.0f}%".format(face_name, 100*face_score)
            cv2.putText(img, text_face, (startx, starty), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

            cv2.imwrite(os.path.join(settings.MEDIA_ROOT, "ml_output/process.jpg"), img)

        # Devuelve los resultados
        machinelearning_results = dict(
            face_detect_score=[],
            face_name=[face_name],
            face_name_score=[face_score],
            emotion_name=[],
            emotion_name_score=[],
            count=[]
        )

        # Detén el bucle para que no sea infinito (puedes ajustar esto según tus necesidades)
        break

    cap.release()
    return machinelearning_results

