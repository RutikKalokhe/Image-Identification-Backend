import cv2
import numpy as np
from fastapi import FastAPI, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from identify import identify_human_image, change_identity

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

@app.get('/')
async def home():
    return "Home Page"

@app.post('/image')
async def identify_single_image(image: UploadFile = File(...)):

    image_bytes = await image.read()

    filename = image.filename

    return identify_human_image(filename, image_bytes)


@app.post('/two_image')
async def identify_two_images(image1: bytes = File(...), image2: bytes = File(...)):

    resp1 = identify_human_image("aaaa", image1)

    resp2 = identify_human_image( "aaaa", image2)

    response = {
        "image1" : resp1,
        "image2" : resp2
    }

    print(response)
    return response


@app.post("/feedback")
async def feedback(file: str, new_identity: str):
    
    return change_identity(file, new_identity) 

