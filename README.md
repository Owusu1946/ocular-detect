# Eye Disease Detection System
A deep learning system for detecting Glaucoma, AMD (Age-related Macular Degeneration), and Cataracts from eye fundus images.

## Overview
This project uses a deep learning model (EfficientNetB0) to classify eye fundus images into three categories:
- Glaucoma
- AMD (Age-related Macular Degeneration)
- Cataracts

## Project Structure
```plaintext
glaucoma_cataract_amd_detector/
├── data/
│ └── processed/ # Processed image data
├── models/
│ └── trained_models/ # Saved model files
├── scripts/
│ ├── organise.py # Data organization script
│ ├── preprocess.py # Data preprocessing script
│ └── training_model.py # Model training script
└── streamlit_app/
└── app.py # Streamlit web application
```

## Setup Instructions

### 1. Environment Setup
Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate # On Windows: env\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install tensorflow
pip install opencv-python
pip install pandas
pip install numpy
pip install streamlit
pip install pillow
pip install scikit-learn
```

### 3. Data Preparation
1. Download the ODIR-5K dataset from [here](https://ieee-dataport.org/open-access/odir-5k-dataset-for-ocular-disease-detection-and-classification)
2. unzip it in the documents folder
3. preprocess the data using the preprocess.py script


### 4. Model Training
1. Run the training_model.py script

The training script will:
- Load preprocessed data
- Train the EfficientNetB0 model
- Save the best model during training
- Output training metrics

### 5. Running the Web Application
Start the Streamlit web interface:
```bash
cd streamlit_app
streamlit run app.py
```


The app will be available at `http://localhost:8501`

## Using the Web Application
1. Open your web browser and navigate to `http://localhost:8501`
2. Upload an eye fundus image using the file uploader
3. Click "Classify Image" to get predictions
4. View results including:
   - Predicted condition
   - Confidence score
   - Confidence level indicator (High/Moderate/Low)

## Model Architecture
- Base model: EfficientNetB0 (pretrained on ImageNet)
- Additional layers:
  - Global Average Pooling
  - Dropout (0.5)
  - Dense layer (128 units, ReLU)
  - Dropout (0.5)
  - Output layer (3 units, Softmax)

## Performance Considerations
- Images are processed in batches to manage memory usage
- Model checkpointing saves the best performing model
- Early stopping prevents overfitting
- Preprocessed data is saved in chunks for efficient loading

## Troubleshooting
1. Memory Issues:
   - Reduce batch size in training_model.py
   - Process images in smaller chunks in preprocess.py

2. Model Loading Errors:
   - Ensure all preprocessing steps are completed
   - Check model file exists in correct location

3. Image Loading Issues:
   - Verify image format (jpg, png, jpeg)
   - Check image file permissions

## License
[MIT](LICENSE)

## Contributors
[Owusu Kenneth](https://github.com/Owusu1946)

