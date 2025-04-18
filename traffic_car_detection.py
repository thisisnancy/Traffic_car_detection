# -*- coding: utf-8 -*-
"""traffic car detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xPLEj_kZvsIEQlAa61gyasXH-cGyS3Cx
"""

!nvidia-smi

from google.colab import drive
drive.mount('/content/drive')

!pip install ultralytics

import torch
from ultralytics import YOLO
import matplotlib.pyplot as plt

# Device configuration (corrected from torch.dwider)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Model Initialization (YOLOv11)
model = YOLO('/content/drive/MyDrive/trafic_data/trafic_data/yolo11m.pt')  # Changed from .pdf to .pt

# Training Configuration (with your original paths)
config = {
    "data": "/content/drive/MyDrive/trafic_data/trafic_data/data_1.yaml",
    "epochs": 100,
    "batch": 10,
    "imgsz": 600,
    "device": device,
    "patience": 15,
    "optimizer": "Adam",
    "lr0": 0.001,  # Changed from 0.000
    "weight_decay": 0.0005,  # Added proper weight decay
    "project": "/content/drive/MyDrive/trafic_data/trafic_data",
    "name": "yolov11m_car",
    "save_period": 10,
    "val": True,
    "augment": True,
    "hsv_h": 0.015,  # Color augmentation (new_b → hsv_h)
    "hsv_s": 0.7,    # (box_s → hsv_s)
    "hsv_v": 0.4,    # (hazy → hsv_v)
    "flipud": 0.5    # Flip probability (flipb → flipud)
}

# Start Training (corrected from "towfig")
results = model.train(**config)

import cv2
from ultralytics import YOLO
from google.colab.patches import cv2_imshow  # Colab-compatible alternative to cv2.imshow

def detect_cars():
    # Load your custom YOLOv11 model
    model = YOLO('/content/drive/MyDrive/trafic_data/trafic_data/yolov11m_car3/weights/epoch90.pt')

    # Open video capture
    video_path = '/content/drive/MyDrive/trafic_data/trafic_data/2053100-uhd_3840_2160_30fps.mp4'
    cap = cv2.VideoCapture(video_path)

    # Get video properties for saving output (optional)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Optional: Create VideoWriter to save output
    # output_path = '/content/drive/MyDrive/trafic_data/output.mp4'
    # out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    frame_count = 0
    max_frames = 100  # Set limit for demo purposes

    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform detection
        results = model(frame)

        # Visualize results
        annotated_frame = results[0].plot()

        # Display the annotated frame (Colab compatible)
        cv2_imshow(annotated_frame)

        # Optional: Save frame to output video
        # out.write(annotated_frame)

        frame_count += 1

        # Break the loop if 'q' is pressed (won't work in Colab, use stop button)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cap.release()
    # out.release()  # If saving output
    print("Processing complete")

if __name__ == "__main__":
    detect_cars()

