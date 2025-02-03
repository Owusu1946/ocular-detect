import os
import shutil
import pandas as pd

# Paths
source_dir = r"C:\Users\HP\Documents\ocular-disease-recognition-odir5k\ODIR-5K\ODIR-5K"
training_dir = os.path.join(source_dir, "Training Images")
testing_dir = os.path.join(source_dir, "Testing Images")
data_file = os.path.join(source_dir, "data.xlsx")

# Create target directories if they don't exist
os.makedirs(training_dir, exist_ok=True)
os.makedirs(testing_dir, exist_ok=True)

# Load the Excel file
df = pd.read_excel(data_file)

# Function to move images
def move_images(file_column, target_dir):
    missing_files = []
    for file_name in df[file_column]:
        if pd.notna(file_name):
            source_path = os.path.join(source_dir, file_name)
            target_path = os.path.join(target_dir, file_name)

            # Check if the source file exists
            if os.path.exists(source_path):
                shutil.move(source_path, target_path)
            else:
                missing_files.append(file_name)
    return missing_files

# Move left and right fundus images to the Training Images folder
missing_left = move_images("Left-Fundus", training_dir)
missing_right = move_images("Right-Fundus", training_dir)

# Print results
if missing_left:
    print(f"Missing Left-Fundus images: {missing_left}")
if missing_right:
    print(f"Missing Right-Fundus images: {missing_right}")

print("Image organization complete.")
