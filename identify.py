import cv2
import numpy as np
from fastapi import File, UploadFile 
from pymongo import MongoClient


# Connect to the MongoDB client on backend vm (sumit)
# client = MongoClient("mongodb:20.21.120.16:27017")
# db = client["imageidentification"]
# collection = db["test"]

# Define the paths to cascade classifier XML files
fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
frontalface_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
upperbody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')


eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
eyeglass_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
profileface_cascade = cv2.CascadeClassifier('haarcascade_profileface.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')


def identify_human_image( filename: str, image_bytes: bytes  = File(...)):

    # is_document_present = collection.find_one({"filename": filename})

    # print(is_document_present)

    # if(is_document_present):
    #     identity = is_document_present['identity']

    #      # Prepare the response
    #     response = {
    #         'identity': identity
    #     }

    #     return response
    # else:

        # Convert the image bytes to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Read the image from the NumPy array
        cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert the image to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Detect humans using different cascade classifiers
        fullbody_humans = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        frontalface_humans = frontalface_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        upperbody_humans = upperbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))


        eye_humans = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        eye_glass_humans = eyeglass_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        profileface_humans = profileface_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        smile_humans = smile_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Print the number of humans detected by each classifier
        print("Full Body Humans: ", len(fullbody_humans))
        print("Frontal Face Humans: ", len(frontalface_humans))
        print("Upper Body Humans: ", len(upperbody_humans))


        print("Eye Humans: ", len(eye_humans))
        print("Eye Glass Humans: ", len(eye_glass_humans))
        print("Profile Face Humans: ", len(profileface_humans))
        print("Smile Humans: ", len(smile_humans))


        # Check if humans are detected using each cascade classifier
        if ( len(fullbody_humans) > 0 and len(frontalface_humans) > 0 ) or (len(frontalface_humans) > 0 and len(upperbody_humans) > 0) or (len(upperbody_humans) > 0 and len(fullbody_humans) > 0):
            identity = 'Human'
        else:
            if(len(frontalface_humans) > 0 and len(eye_humans) > 0 and len(eye_glass_humans) > 0 and len(profileface_humans) > 0):
                identity = 'Human'
            else:
                identity = 'Non-Human'

        # Prepare the response
        response = {
            'identity': identity
        }

      #  inserting_data = {"filename": filename, "identity": identity}

       # collection.insert_one(inserting_data)

        return response


def change_identity(filename: str, new_identity: str):
    filter_query = {"filename": filename}

    query = {"$set": {"identity": new_identity}}

    collection.update_one(filter_query, query)

    return "changes updated"
