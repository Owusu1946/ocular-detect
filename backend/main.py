from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
model = tf.keras.models.load_model("../models/trained_models/best_model.keras")
labels = ['Glaucoma', 'AMD', 'Cataract']

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read and preprocess the image
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Make prediction
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    confidence = float(predictions[0][predicted_class])
    
    # Determine confidence level
    confidence_level = "High" if confidence > 0.8 else "Moderate" if confidence > 0.5 else "Low"
    
    return {
        "success": True,
        "prediction": {
            "condition": labels[predicted_class],
            "confidence": confidence,
            "confidenceLevel": confidence_level
        }
    } 