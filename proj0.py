import librosa
import noisereduce as nr
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Confirm script is running
print("Starting feature extraction...")

# Set dataset path
dataset_path = "C:/Users/user/Downloads/archive/cat"

# Initialize list for features
all_features = []

# Iterate over audio files
for file_name in os.listdir(dataset_path):
    if file_name.endswith(".wav"):
        file_path = os.path.join(dataset_path, file_name)
        print(f"Processing: {file_path}")

        # Load audio
        y, sr = librosa.load(file_path, sr=None)

        # Reduce noise
        y_denoised = nr.reduce_noise(y=y, sr=sr)

        # Extract MFCCs
        mfcc = librosa.feature.mfcc(y=y_denoised, sr=sr, n_mfcc=13)
        mfcc = mfcc.T  # Shape: (frames, 13)

        # Add to list
        all_features.append(mfcc)

# Stack all features into one array
if all_features:
    features = np.vstack(all_features)

    # Standardize features
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    print("Feature extraction completed.")
    print("Final feature shape:", features.shape)

    # Optional: plot MFCCs from one sample
    plt.figure(figsize=(10, 4))
    plt.imshow(mfcc.T, aspect='auto', origin='lower')
    plt.title('MFCC (Last Processed File)')
    plt.xlabel('Frame Index')
    plt.ylabel('MFCC Coefficients')
    plt.colorbar()
    plt.tight_layout()
    plt.show()

else:
    print("No .wav files found in the specified directory.")
