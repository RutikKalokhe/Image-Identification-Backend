import cv2
import numpy as np
from fastapi import FastAPI, File, Request, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from identify import identify_human_image, change_identity, identify_aadhaar_photo
from aadhaar_detect import is_aadhaar_card
from typing import List

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

    try:
        image_bytes = await image.read()
        filename = image.filename
        return identify_human_image(filename, image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/two_image')
async def identify_two_images(image1: UploadFile = File(...), image2: UploadFile = File(...)):

    try:
        image_bytes1 = await image1.read()

        image_bytes2 = await image2.read()

        resp1 = identify_human_image(image1.filename, image_bytes1)

        resp2 = identify_human_image(image2.filename, image_bytes2)

        response = {
            "image1" : resp1,
            "image2" : resp2
        }

        print(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/multiple_images')
async def identify_multiple_images(images: List[UploadFile] = File(...)):
    try:    
        results = []
        for image in images:
            contents = await image.read()
            resp = identify_human_image(image.filename, contents)
            print(resp)
            results.append(resp)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def feedback(file: str, identity: str):
    try:
        return change_identity(file, identity) 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@app.post('/aadhaar')
async def identify_aadhaarcard_image(image: UploadFile = File(...)):

    try:
        image_bytes = await image.read()
        filename = image.filename

        is_aadhaar = is_aadhaar_card(image_bytes)
        is_aadhaarcard_photo = identify_aadhaar_photo(filename, image_bytes)
        
        print(is_aadhaarcard_photo['identity'])
        print(is_aadhaar['message'])
        
        if is_aadhaarcard_photo['identity'] == 'Human' and is_aadhaar['message'] == "Original Aadhaar":
            return {'message': "Original Aadhaar"}

        else:
            return {'message': "Duplicate Aadhaar/ Image is not clear"}
    except Exception as e:
        return {'message': "Duplicate Aadhaar/ Image is not clearrr"}
        # return {'message': str(e)}

