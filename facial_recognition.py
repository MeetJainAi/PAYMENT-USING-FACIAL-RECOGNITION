import face_recognition
import os
from details_db import *

# Algorithm to recognize face from a set of known faces


def recognize_face():
    match_image_index = None
    known_encodings = []
    images_to_compare = os.listdir('customer_faces')
    try:
        for i, image in enumerate(images_to_compare):
            known_image = face_recognition.load_image_file(
                'customer_faces/'+image, mode='RGB')
            known_image_encoding = face_recognition.face_encodings(known_image)[
                0]
            print('customer_faces/'+image)
            known_encodings.append(known_image_encoding)

        test_image = face_recognition.load_image_file(
            'test_image.jpg', mode='RGB')
        test_image_encoding = face_recognition.face_encodings(test_image)[0]

        face_distances = face_recognition.face_distance(
            known_encodings, test_image_encoding)
    # Handle the exception of not detecting a face
    except IndexError as error:
        print(error)
        return 'Detection Error'

    for i, face_distance in enumerate(face_distances):

        print('Image '+str(i)+' has a eucledian distance of ' +
              str(face_distance)+' from test image')
        print()
        if face_distance < 0.7:
            match_image_index = i
        print('Match = '+str(face_distance < 0.7))
        print()
    # Return image name if match is found
    if match_image_index != None:
        return images_to_compare[match_image_index]
    # Return -1 if no match is found
    else:
        print('Match not found......')
        return -1
