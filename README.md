# SADLT - (S)emi (A)utomated (D)ata (L)abeling (T)ool

## Project Overview
The Semi-Automated Data Labeling Tool (SADLT) is a Python-based application built using Tkinter and OpenCV, designed to facilitate the annotation of bounding boxes in images for object detection tasks. This tool provides a set of core functions for working in computer vision applications, allowing users to create, manipulate, and save labels. 
It provides a graphical user interface (GUI) for loading images, creating bounding boxes, selecting visual elements on a canvas and saving labeled data. This tool incorporates the "You Only Look Once" YOLOv5 model, a real time instance segmentation model deployed by Ultralytics, pretrained on COCO, a large-scale object detection, segmentation, and captioning dataset, for semi-automated annotation.
![Image Description](demo.png)


## Features
*   **User-Friendly Interface:** An intuitive GUI allows users to load images, create bounding boxes, and manipulate annotations easily.
*   **Detection Model Integration:** The tool integrates the COCO object detection model (yolov5s) to assist users in automating the initial annotation process.
*   **BBox Creation and Manipulation:** Easily create bounding boxes by clicking and dragging on the canvas. Users can adjust the dimensions, position, and labels of bounding boxes dynamically within the application using intuitive controls.
*   **Labeling Tool:** Assign labels to bounding boxes using a user-friendly interface. Supports the creation, modification, and deletion of labels.
*   **Label Persistence:** The tool saves and loads annotations, enabling users to resume labeling tasks seamlessly.

     
## Installation and Setup
### Prerequisites

*   [Python](https://www.python.org/) (3.6 or later)
*   [Anaconda](https://www.anaconda.com/) or Miniconda

### Running the Application

To install and set up the project on your local machine, follow these steps:

1. Clone the repository: `git clone https://github.com/Bangulli/Semi-Automated-Data-Labeling-Tool.git`
2. Navigate into the project directory: `cd Semi-Automated-Data-Labeling-Tool`
3. Install the dependencies: `pip install -r requirements.txt`
4. Run the application: `python main/SADLT.py`

## Usage

1.  **Loading Images:**
    
*   Click the "Browse" button to select the working directory containing images (PNG, JPG, JPEG).
*   Click on an image in the list to load it into the canvas.

2.  **Manual Annotation:**
    
*   Left-click and drag to draw bounding boxes manually.
*   Adjust box dimensions and labels using the provided controls.
*   To modify the position of an existing bounding box:
    *   Click on the desired bounding box in the "Detected Frames" list.
    *   Utilize the "Control Bounding Box Position" section to move the selected bounding box horizontally or vertically.

3.  **COCO Detection:**
    
*   Click "COCO Detection" to run the object detection model on the current image.
*   Detected objects will be displayed as bounding boxes on the canvas.

4.  **Saving Annotations:**
    
*   Click "Save" to save the annotations in a text file corresponding to the image.

## Contributors
, , , 	Quan Huy Tran, 
1. [Jose Andres Herrera](https://github.com/joanhermo)
2. [Sirada Kittipaisarnkul](https://github.com/99ffx)
3. [Paola Vasquez](https://github.com/paolavasquez98)
4. [Lorenz Achim Kuhn](https://github.com/Bangulli)
5. [Quang Huy Tran](https://github.com/huytrq-em)

## Acknowledgments
*   The COCO object detection model used in this tool is based on [yolov5](https://pytorch.org/hub/ultralytics_yolov5/).

