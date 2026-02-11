from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Train the model
model.train(
    data="mine_ppe_dataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=8
)
