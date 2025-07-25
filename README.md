# 🍅 Tomato Disease Detection and Classification

![Tomato Banner](images/banner.png)

This repository contains a **Python application** for detecting and classifying tomatoes into **Good** and **Bad** categories using a custom-trained **YOLOv8** model. It is built to help identify healthy vs. rotten tomatoes through computer vision, and it supports **dual datasets** to enhance detection accuracy.

## 📌 Description

This project aims to automate the classification of tomatoes using deep learning techniques. By leveraging **YOLOv5**, the system can detect tomatoes in an image and classify each tomato as:

- ✅ `TomatoGood` – Healthy tomato
- ❌ `TomatoBad` – Rotten, diseased, or moldy tomato

The application is useful for:
- Farmers and food industries
- Quality inspection in sorting lines
- Smart agriculture solutions



> 📝 Images are saved automatically to the `runs/detect/` directory after detection.

## 🧠 Model Details

- Framework: **YOLOv5**
- Libraries: `PyTorch`, `OpenCV`, `Matplotlib`
- Training datasets:
  - `Dataset 1`: Tomato images (Good/Bad)
  - `Dataset 2`: Custom augmented tomato data

## 🚀 Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/Hemriti/Tomato_Disease_Detection.git
cd Tomato_Disease_Detection
