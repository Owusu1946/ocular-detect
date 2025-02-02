import os
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Paths to the processed data
data_dir = r"C:\Users\HP\glaucoma_cataract_amd_detector\data\processed"
X_train_files = [os.path.join(data_dir, f"X_train_{i}.npy") for i in range(12)]
X_test_files = [os.path.join(data_dir, f"X_test_{i}.npy") for i in range(3)]
y_train_files = [os.path.join(data_dir, f"y_train_{i}.npy") for i in range(12)]
y_test_files = [os.path.join(data_dir, f"y_test_{i}.npy") for i in range(3)]

# Load the data
print("Loading data...")
X_train = np.concatenate([np.load(file) for file in X_train_files], axis=0)
X_test = np.concatenate([np.load(file) for file in X_test_files], axis=0)
y_train = np.concatenate([np.load(file) for file in y_train_files], axis=0)
y_test = np.concatenate([np.load(file) for file in y_test_files], axis=0)

# Check data types and shapes
print("X_train dtype:", X_train.dtype)
print("y_train dtype:", y_train.dtype)
print("X_test dtype:", X_test.dtype)
print("y_test dtype:", y_test.dtype)
print("y_train shape:", y_train.shape)
print("y_test shape:", y_test.shape)

# If y_train and y_test are one-hot encoded (2D), we need to convert them to integer labels (1D)
if y_train.ndim == 2:
    y_train = np.argmax(y_train, axis=1)  # Convert one-hot encoded labels to integer labels
    y_test = np.argmax(y_test, axis=1)

# Check the transformed labels
print("Encoded y_train:", y_train[:5])
print("Encoded y_test:", y_test[:5])

# Convert to the correct types if necessary
X_train = X_train.astype(np.float32)
X_test = X_test.astype(np.float32)
y_train = y_train.astype(np.int32)  # For classification labels, make sure they are integers
y_test = y_test.astype(np.int32)

print(f"Training data shape: {X_train.shape}")
print(f"Testing data shape: {X_test.shape}")

# Number of output classes
num_classes = len(np.unique(y_train))

# Pre-trained model (EfficientNetB0)
print("Building model...")
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model
base_model.trainable = False

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.5)(x)  # Regularization
x = Dense(128, activation='relu')(x)
x = Dropout(0.5)(x)
outputs = Dense(num_classes, activation='softmax')(x)

# Define the model
model = Model(inputs=base_model.input, outputs=outputs)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Callbacks
output_model_path = r"models/trained_models/best_model.keras"  # Updated file extension
callbacks = [
    ModelCheckpoint(output_model_path, monitor='val_accuracy', save_best_only=True, verbose=1),
    EarlyStopping(monitor='val_accuracy', patience=5, verbose=1)
]

# Training
print("Training the model...")
history = model.fit(X_train, y_train,
                    validation_data=(X_test, y_test),
                    epochs=20,
                    batch_size=32,
                    callbacks=callbacks)

# Save the final model
final_model_path = r"models/trained_models/final_model.keras"  # Updated file extension
model.save(final_model_path)
print(f"Model saved to {final_model_path}")
