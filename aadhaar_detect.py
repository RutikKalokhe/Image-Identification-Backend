import cv2
import pytesseract
import numpy as np
import re
from fastapi import File, UploadFile 

# Path to Tesseract OCR executable (adjust this based on your system)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



def is_aadhaar_card( image_bytes: bytes  = File(...)):
    # Load the image
    # image_path = 'aadhaar2.jpg'
    # image = cv2.imread(image_path)

    # Convert the image bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Read the image from the NumPy array
    cv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(gray)

    # Print the original extracted text
    print("Original Extracted Text:")
    print(extracted_text)

    # Define regular expressions for name, birthdate, and Aadhaar number
    name_pattern = r"(?i)(?<!\S)[A-Z][a-z]+(?: [A-Z][a-z]+)*(?!\S)"
    birthdate_pattern = r"(?i)\b(?:0?[1-9]|[12][0-9]|3[01])/(?:0?[1-9]|1[0-2])/(?:19|20)\d{2}\b"
    aadhaar_pattern = r"(?i)\b\d{4}\s\d{4}\s\d{4}\b"
    birthyear_pattern = r"(?i)\b(?:19|20)\d{2}(?!\d)"

    # Extract relevant information using regular expressions
    name = re.findall(name_pattern, extracted_text)
    birthdate = re.findall(birthdate_pattern, extracted_text)
    aadhaar_number = re.findall(aadhaar_pattern, extracted_text)
    birthyear = re.findall(birthyear_pattern, extracted_text)

    # Print the extracted information
    print("Extracted Information:")
    print("Names:", name)
    print("Aadhaar Numbers:", aadhaar_number[0])
    if len(birthyear):
        print("Birth Year:", birthyear[0])
    if len(birthdate):
        print("Birthdates:", birthdate[0])
    


    if len(aadhaar_number) and len(birthdate) or len(aadhaar_number) and len(birthyear):
        print("Original Aadhaar")
        return {'message': "Original Aadhaar"}
    else:
        print("Duplicate Aadhaar/ Image is not clear")
        return {'message': "Duplicate Aadhaar/ Image is not clear"}
        
