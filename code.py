from ultralytics import YOLO
import cv2
import cvzone
import math
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def process_detections(model_path, class_names, img_path):
    # Load the YOLO model
    try:
        model = YOLO(model_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None, None

    # Read the image
    img = cv2.imread(img_path)

    if img is None:
        print(f"Error: Image at path {img_path} not found.")
        return None, None

    # Perform object detection on the image
    results = model(img)

    # Create a DataFrame to store the detections
    df = pd.DataFrame(columns=['Class', 'Confidence', 'X1', 'Y1', 'X2', 'Y2'])

    # Process the detections
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            
            # Class Name
            cls = int(box.cls[0])

            # Draw the class name and confidence on the image
            cvzone.putTextRect(img, f'{class_names[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            # Append the detection to the DataFrame
            new_row = pd.DataFrame({'Class': [class_names[cls]], 'Confidence': [conf], 'X1': [x1], 'Y1': [y1], 'X2': [x2], 'Y2': [y2]})
            if not new_row.isna().all().all():
                df = pd.concat([df, new_row], ignore_index=True)

    return img, df

# Define parameters for model 1
model_path1 = r"dataset\best8000.pt"
class_names1 = ['Tomate_maduro', 'Tomate_podre', 'Tomate_verde']
img_path1 = r"dataset\essai\depositphotos_415088056-stock-photo-red-rotten-tomatoes-plant-vegetable.jpg"

# Define parameters for model 2
model_path2 = r"dataset\best2000 (1).pt"
class_names2 = ['TomatoBad', 'TomatoGood']
img_path2 = r"dataset\essai\depositphotos_415088056-stock-photo-red-rotten-tomatoes-plant-vegetable.jpg"

def display_results(img1, df1, img2, df2):
    # Combine the results
    combined_img = img1.copy()
    combined_df = pd.concat([df1, df2])

    # Display combined results
    num_good_tomatoes_combined = combined_df[combined_df['Class'] == 'Tomate_maduro'].shape[0] + combined_df[combined_df['Class'] == 'TomatoGood'].shape[0]
    num_bad_tomatoes_combined = combined_df[combined_df['Class'] == 'Tomate_podre'].shape[0] + combined_df[combined_df['Class'] == 'TomatoBad'].shape[0]

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(cv2.cvtColor(combined_img, cv2.COLOR_BGR2RGB))
    axes[0].axis('off')
    axes[0].set_title('Tomato Detection')

    axes[1].bar(['Good Tomatoes', 'Bad Tomatoes', 'Total Tomatoes'], [num_good_tomatoes_combined, num_bad_tomatoes_combined, len(combined_df)], color=['green', 'red', 'blue'])
    axes[1].set_ylabel('Number of Tomatoes')
    axes[1].set_title('Number of Tomatoes Detected')
    for i, count in enumerate([num_good_tomatoes_combined, num_bad_tomatoes_combined, len(combined_df)]):
        axes[1].text(i, count + max([num_good_tomatoes_combined, num_bad_tomatoes_combined, len(combined_df)]) * 0.02, str(count), ha='center')

    plt.show()

# Function to open a file dialog and select an image
def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Function to process the image from the UI
def process_image():
    img_path = entry.get()
    if not img_path:
        messagebox.showerror("Input Error", "Please enter an image path!")
        return

    # Process detections for both models
    img1, df1 = process_detections(model_path1, class_names1, img_path)
    img2, df2 = process_detections(model_path2, class_names2, img_path)

    if img1 is not None and df1 is not None and img2 is not None and df2 is not None:
        display_results(img1, df1, img2, df2)

import tkinter as tk
from tkinter import PhotoImage

# Create the Tkinter UI
root = tk.Tk()
root.title("Tomato Detection")

# Set the window icon
root.iconbitmap("C:/Users/moham/Downloads/tomato.ico")

# Entry for image path
entry_label = tk.Label(root, text="Enter image path:")
entry_label.pack(padx=10, pady=5)

entry = tk.Entry(root, width=50)
entry.pack(padx=10, pady=5)

# Button to trigger the process
button = tk.Button(root, text="Process Image", command=process_image)
button.pack(padx=10, pady=20)

# Footer with "Powered by AOE" and logo
footer_frame = tk.Frame(root)
footer_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Load and display the logo image
try:
    logo_img = PhotoImage(file="C:/Users/moham/Downloads/logo.png")
    logo_label = tk.Label(footer_frame, image=logo_img)
    logo_label.pack(side=tk.LEFT, padx=5)
except tk.TclError:
    print("Error loading logo image.")

# Add "Powered by AOE" text
powered_by_label = tk.Label(footer_frame, text="Powered by AOE", font=("Arial", 10))
powered_by_label.pack(side=tk.LEFT, padx=5)

# Start the Tkinter event loop
root.mainloop()
