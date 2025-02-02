import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image
import time
import os

# Create model directory if it doesn't exist
model_dir = "models/trained_models"
os.makedirs(model_dir, exist_ok=True)

# Load the trained model
model = tf.keras.models.load_model(r"models/trained_models/best_model.keras")

# Define the labels for Glaucoma, AMD, and Cataracts
labels = ['Glaucoma', 'AMD', 'Cataract']

# Streamlit app title and description with CSS
st.markdown("""
    <style>
        .title {
            font-size: 30px;
            color: #FF6347;
            text-align: center;
            font-weight: bold;
        }
        .description {
            font-size: 16px;
            color: #808080;
            text-align: center;
        }
        .button {
            background-color: #FF6347;
            border-radius: 5px;
            padding: 10px 20px;
            color: white;
            font-weight: bold;
            font-size: 16px;
            border: none;
        }
        .result {
            font-size: 20px;
            font-weight: bold;
            text-align: center;
        }
        .confidence {
            font-size: 16px;
            text-align: center;
        }
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 50px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title and description
st.markdown('<p class="title">Glaucoma, Cataract, and AMD Detection</p>', unsafe_allow_html=True)
st.markdown('<p class="description">Upload an image of the eye, and the app will predict whether the image shows signs of **Glaucoma**, **AMD (Age-related Macular Degeneration)**, or **Cataracts**.</p>', unsafe_allow_html=True)

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Button to start prediction
    if st.button('Classify Image', key='classify', help="Click to classify the image"):
        
        # Show loading spinner while processing
        with st.spinner("Processing image... This may take a moment..."):
            time.sleep(2)  # Simulate delay for processing
            
            # Open and preprocess the image
            img = Image.open(uploaded_file)
            img = img.resize((224, 224))  # Resize the image to (224, 224)
            img_array = np.array(img)  # Convert image to numpy array
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array = preprocess_input(img_array)  # Preprocess image (EfficientNetB0 specific)

            # Make predictions
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)

            # Display results with more polished feedback
            st.markdown(f'<p class="result">Prediction: <span style="color: #FF6347;">{labels[predicted_class[0]]}</span></p>', unsafe_allow_html=True)
            st.markdown(f'<p class="confidence">Confidence: {predictions[0][predicted_class[0]]*100:.2f}%</p>', unsafe_allow_html=True)

            # Add some color based on confidence level
            if predictions[0][predicted_class[0]] > 0.8:
                st.markdown('<p class="confidence" style="color: green;">High Confidence</p>', unsafe_allow_html=True)
            elif predictions[0][predicted_class[0]] > 0.5:
                st.markdown('<p class="confidence" style="color: orange;">Moderate Confidence</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="confidence" style="color: red;">Low Confidence</p>', unsafe_allow_html=True)

        # Add a little spacing before allowing new uploads or predictions
        st.markdown('<div class="loading"></div>', unsafe_allow_html=True)
