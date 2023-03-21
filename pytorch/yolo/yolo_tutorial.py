import ultralytics
from ultralytics import YOLO

if __name__ == "__main__":
    print(f"ultralytics: {ultralytics.checks()}")
    model = YOLO("yolov8n.pt")
    model.track(data="coco128.yaml")
    model.val()
    model.predict(source="https://ultralytics.com/images/bus.jpg")
    model.export(format="saved_model")