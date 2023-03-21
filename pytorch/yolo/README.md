# Yolo Tutorial
https://docs.ultralytics.com/
- YOLO as a real-time object detector.
- In machine learning terms, we can say all objects are detected via a single algorithm run. It's done by dividing
an image into a grid and predicting bounding boxes and class probabilities for each cell in a grid.
- a non-maximum suppression algorithm is applied to select the best bounding box for a given object.
- two stage object detectors: find interest parts, then classify. However, yolo is one stage object detector.
- One key feature of YOLOv8 is its extensibility. It is designed as a framework that supports all previous versions of YOLO,
making it easy to switch between different versions and compare their performance.

## YOLOv8 Modes
### Train: 
For training a YOLOv8 model on a custom dataset
```python
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.ymal') # build a new model from YMAL
model = YOLO('yolov8n.pt') # load a pretrained model (recommended for training)
model = YOLO('yolov8n.ymal').load('yolov8n.pt') # build from YAML and transfer weights

# Train the model
model.train(data='coco128.yaml', epochs=100, imgsz=640)
```
### Val: 
For validating a YOLOv8 model after it has been trained. It is important to carefully tune and experiment with
these settings to ensure that the model is performing well on the validation dataset and to detect and prevent 
overfitting.
```python
metrics = model.val()
metrics.box.map
metrics.box.map50
metrics.box.map75
metrics.box.maps
```
### Predict:
```python
inputs = [img, img] # list of np arrays
results = model(inputs) # List of Results objects or
results = model(inputs, stream=True) # generator of Results objects
```
### Export:
```python
from ultralytics import YOLO
# Load a model
model = YOLO('yolov8n.pt') # load an official model
model = YOLO('path/to/best.pt') # load a custom trained

# Export the model
model.export(format='onnx')
```
### Track:
Object tracking is a task that involves identifying the location and class of objects, then assigning a unique ID to
that detection in video streams. 
The output of tracker is the same as detection with an added object ID. 
```python
from ultralytics import YOLO
# Load a model
model = YOLO('yolov8n.pt') # load an official detection model
model = YOLO('yolov8n-seg.pt') # load an official segmentation model
model = YOLO('path/to/best.pt') # load a custom model

# Track with the model
results = model.track(source="https://youtu.be/xxxxxx", show=True)
results = model.track(source="https://youtu.be/xxxxxx", show=True, tracker="bytetrack.yaml")
```
### Benchmark:
```python
from ultralytics.yolo.utils.benchmarks import benchmark
# Benchmark
benchmark(model='yolov8n.pt', imgsz=640, half=False, device=0)
```

## YOLOv8 Tasks
YOLOv8 is an AI framework that supports multiple computer vision tasks. The framework can be used to perform
detection, segmentation, classification, and keypoints detection. 