import os
import cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Paths
training_dir = r"C:\Users\HP\Documents\ocular-disease-recognition-odir5k\ODIR-5K\ODIR-5K\Training Images"
data_file = r"C:\Users\HP\Documents\ocular-disease-recognition-odir5k\ODIR-5K\ODIR-5K\data.xlsx"
output_dir = r"C:\Users\HP\glaucoma_cataract_amd_detector\data\processed"

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load the dataset
print("Loading dataset...")
df = pd.read_excel(data_file)
print(f"Dataset loaded with {len(df)} entries.")

# Image preprocessing parameters
IMG_SIZE = 224

# Function to load and preprocess images
def load_and_preprocess_image(image_path):
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Warning: Unable to load image {image_path}")
            return None

        # Resize image
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

        # Normalize pixel values to [0, 1]
        img = img / 255.0

        return img
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

# Prepare data lists
images = []
labels = []

# Iterate through the dataset and load images
print("Processing images...")
for idx, row in df.iterrows():
    left_path = os.path.join(training_dir, row['Left-Fundus']) if pd.notna(row['Left-Fundus']) else None
    right_path = os.path.join(training_dir, row['Right-Fundus']) if pd.notna(row['Right-Fundus']) else None

    # Process left fundus image
    if left_path and os.path.exists(left_path):
        img = load_and_preprocess_image(left_path)
        if img is not None:
            images.append(img)
            # Combine both left and right labels as a tuple
            combined_label = (row['Left-Diagnostic Keywords'], row['Right-Diagnostic Keywords'])
            labels.append(combined_label)

    # Process right fundus image
    if right_path and os.path.exists(right_path):
        img = load_and_preprocess_image(right_path)
        if img is not None:
            images.append(img)
            # Combine both left and right labels as a tuple
            combined_label = (row['Left-Diagnostic Keywords'], row['Right-Diagnostic Keywords'])
            labels.append(combined_label)

    # Print progress every 1000 images processed
    if (idx + 1) % 1000 == 0:
        print(f"Processed {idx + 1} images...")

# Convert to numpy arrays
print(f"Converting data to numpy arrays...")
images = np.array(images)
labels = np.array(labels)

# Train-test split
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# Function to save the data in chunks
def save_in_chunks(filename, data, chunk_size=500):
    num_chunks = len(data) // chunk_size + (1 if len(data) % chunk_size != 0 else 0)
    for i in range(num_chunks):
        chunk = data[i*chunk_size:(i+1)*chunk_size]
        file_path = os.path.join(output_dir, f"{filename}_{i}.npy")
        np.save(file_path, chunk)
        print(f"Saved chunk {i + 1}/{num_chunks} to {file_path}")

# Save preprocessed data in chunks
print("Saving preprocessed data in chunks...")
save_in_chunks("X_train", X_train)
save_in_chunks("X_test", X_test)
save_in_chunks("y_train", y_train)
save_in_chunks("y_test", y_test)

print("Preprocessing complete. Data saved successfully.")
