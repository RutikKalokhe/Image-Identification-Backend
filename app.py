import cv2
import numpy as np
from fastapi import FastAPI, File
from fastapi.middleware.cors import CORSMiddleware
from identify import identify_human_image

# Create a FastAPI application
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# # Define the paths to cascade classifier XML files
# fullbody_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
# frontalface_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# upperbody_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')

# # Define a route for image classification for path 
# @app.get('/identify')
# async def identify_image(image_path: str):
#     # Read the image from the provided path
#     cv_image = cv2.imread(image_path)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

#     # Detect humans using different cascade classifiers
#     fullbody_humans = fullbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#     frontalface_humans = frontalface_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
#     upperbody_humans = upperbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#     # Print the number of humans detected by each classifier
#     print("Full Body Humans: ", len(fullbody_humans))
#     print("Frontal Face Humans: ", len(frontalface_humans))
#     print("Upper Body Humans: ", len(upperbody_humans))


#      # Check if humans are detected using each cascade classifier
#     if ( len(fullbody_humans) > 0 and len(frontalface_humans) > 0 ) or (len(frontalface_humans) > 0 and len(upperbody_humans) > 0) or (len(upperbody_humans) > 0 and len(fullbody_humans) > 0):
#         class_label = 'Human'
#     else:
#         class_label = 'Non-Human'

#     # Prepare the response
#     response = {
#         'class_label': class_label,
#         'confidence': float(confidence)
#     }

#     return response

@app.post('/image')
async def identify_single_image(image: bytes = File(...)):

    return identify_human_image(image)


@app.post('/two_image')
async def identify_two_images(image1: bytes = File(...), image2: bytes = File(...)):

    resp1 = identify_human_image(image1)

    resp2 = identify_human_image(image2)

    response = {
        "image1" : resp1,
        "image2" : resp2
    }

    print(response)
    return response