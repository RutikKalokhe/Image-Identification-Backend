# Use the official Python base image
FROM python:3.8

# Install system dependencies for OpenCV
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx tesseract-ocr
   
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY . .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose the port that the FastAPI application will listen on
EXPOSE 8000

# Start the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
