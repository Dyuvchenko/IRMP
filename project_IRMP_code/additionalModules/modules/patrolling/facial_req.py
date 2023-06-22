from datetime import datetime

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

import ProjectConsts
from core.cameras.camController import CamerasController

camera = CamerasController.camera

# Determine faces from encodings.pickle file model created from train_model.py
encodingsP = "additionalModules/modules/patrolling/encodings.pickle"

# load the known faces and embeddings along with OpenCV's Haar
# cascade for face detection
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

kol_vo_unknow = 0


def show_facial_recognition():
    # Initialize 'currentname' to trigger only when a new person is identified.
    current_name = "unknown"
    # grab the frame from the threaded video stream and resize it
    # to 500px (to speedup processing)
    # frame = vs.read()
    frame = camera.get_frame(_bytes=False)
    frame = imutils.resize(frame, width=500)
    # Detect the fce boxes
    boxes = face_recognition.face_locations(frame)
    # compute the facial embeddings for each face bounding box
    encodings = face_recognition.face_encodings(frame, boxes)
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        name = "Unknown"  # if face is not recognized, then print Unknown

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # determine the recognized face with the largest number
            # of votes (note: in the event of an unlikely tie Python
            # will select first entry in the dictionary)
            name = max(counts, key=counts.get)

            # If someone in your dataset is identified, print their name on the screen
            if current_name != name:
                current_name = name
                global kol_vo_unknow
                if name == "Unknown":
                    if kol_vo_unknow > 3:
                        ProjectConsts.Core.voiceGuidanceController.play_sound(
                            "Внимание! Обнаружен  посторонний человек! Срочно покиньте территорию!")
                        ProjectConsts.Core.voiceGuidanceController.play_sound(
                            "Внимание! Обнаружен  посторонний человек! Срочно покиньте территорию!")
                        ProjectConsts.Core.voiceGuidanceController.play_sound(
                            "Внимание! Обнаружен  посторонний человек! Срочно покиньте территорию!")

                    kol_vo_unknow += 1
                    ProjectConsts.Core.voiceGuidanceController.play_sound(
                        "Внимание! Обнаружен посторонний! Остановитесь и посмотрите на меня!")
                kol_vo_unknow = 0
                print(current_name)

        # update the list of names
        names.append(name)

    # loop over the recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # draw the predicted face name on the image - color is in BGR
        cv2.rectangle(frame, (left, top), (right, bottom),
                      (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (0, 255, 255), 2)

    # display the image to our screen
    time_now = datetime.now().__str__().replace(" ", "__").replace(":", "-")
    file_name = "additionalModules/modules/patrolling/save_img/" + time_now + ".jpg"
    # file_name = "additionalModules/modules/patrolling/save_img/test1.jpg"
    cv2.imwrite(file_name, frame)
