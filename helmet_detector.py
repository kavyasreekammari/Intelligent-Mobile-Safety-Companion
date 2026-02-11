import cv2
from ultralytics import YOLO

MODEL_PATH = "../runs/detect/train2/weights/best.pt"

REQUIRED_PPE = {
    "helmet": False,
    "gloves": False,
    "safety_shoes": False,
    "goggles": False
}

def check_ppe_ai():
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(0)

    # ---------- FULLSCREEN WINDOW ----------
    window_name = "PPE Safety Scan - Press Q to Finish"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(
        window_name,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )
    # --------------------------------------

    detected = REQUIRED_PPE.copy()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.5)

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = model.names[cls].lower()

                for key in detected:
                    if key in label:
                        detected[key] = True

        # ---------- SMALL TEXT DISPLAY ----------
        y = 35
        for item, status in detected.items():
            color = (0, 255, 0) if status else (0, 0, 255)
            text = f"{item.replace('_', ' ').title()}: {'YES' if status else 'NO'}"

            cv2.putText(
                frame,
                text,
                (30, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,      # 👈 smaller font
                color,
                2         # 👈 thinner text
            )
            y += 30
        # ---------------------------------------

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if all(detected.values()):
            break

    cap.release()
    cv2.destroyAllWindows()

    missing = [item for item, ok in detected.items() if not ok]
    return detected, missing
