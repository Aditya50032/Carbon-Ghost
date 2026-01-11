import cv2
import numpy as np
import requests
import time
import threading

# ===============================
# FIREBASE CONFIG
# ===============================
FIREBASE_URL = "https://carbon-ghost-default-rtdb.firebaseio.com"

def send_to_firebase_async(object_type):
    def task():
        try:
            requests.post(
                f"{FIREBASE_URL}/detections.json",
                json={
                    "object": object_type,
                    "timestamp": time.time()
                },
                timeout=1
            )
        except:
            pass
    threading.Thread(target=task, daemon=True).start()

# ===============================
# LOAD FACE DETECTOR
# ===============================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ===============================
# START CAMERA (macOS SAFE)
# ===============================
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
if not cap.isOpened():
    print("Camera not accessible")
    exit()

window_name = "Carbon Ghosts - Stable Demo"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

# ===============================
# GHOST STYLES (CLAMPED)
# ===============================
ghost_styles = {
    "ECO":    {"size": 60,  "intensity": 0.20, "color": (120, 220, 120)},
    "MEDIUM": {"size": 140, "intensity": 0.45, "color": (200, 200, 200)},
    "HIGH":   {"size": 200, "intensity": 0.65, "color": (40, 40, 40)},
    "HUMAN":  {"size": 0,   "intensity": 0.0,  "color": (0, 0, 0)}
}

# ===============================
# DRAW CARBON GHOST (FAST)
# ===============================
def draw_carbon_ghost(frame, center, style):
    if style["intensity"] == 0:
        return frame

    output = frame.copy()
    for i in range(4):  # reduced layers
        overlay = output.copy()
        radius = int(style["size"] + i * 25)
        alpha = max(0.05, style["intensity"] - i * 0.08)

        cv2.circle(overlay, center, radius, style["color"], -1)
        output = cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0)

    return output

# ===============================
# LIGHTWEIGHT OBJECT ANALYSIS
# ===============================
def analyze_object(frame):
    h, w, _ = frame.shape
    crop = frame[h//2-40:h//2+40, w//2-40:w//2+40]

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    avg_hue = np.mean(hsv[:, :, 0])
    avg_value = np.mean(hsv[:, :, 2])

    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.mean(edges)

    if 35 < avg_hue < 85 and avg_value > 80:
        return "ECO"
    elif avg_value > 170 and edge_density < 20:
        return "MEDIUM"
    else:
        return "HIGH"

# ===============================
# PERFORMANCE CONTROLS
# ===============================
frame_count = 0

DETECT_EVERY_N_FRAMES = 10      # object detection
FACE_DETECT_EVERY = 30          # face detection

cached_object_type = "MEDIUM"
cached_is_human = False
last_face_check = 0
last_object_sent = None

# ===============================
# MAIN LOOP
# ===============================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    center = (w // 2, h // 2)

    frame_count += 1

    # ---------- Resize once for detection ----------
    if frame_count % DETECT_EVERY_N_FRAMES == 0:
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        # ----- Face detection (rare) -----
        if frame_count - last_face_check >= FACE_DETECT_EVERY:
            gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.3,
                minNeighbors=6,
                minSize=(120, 120)
            )
            cached_is_human = len(faces) > 0
            last_face_check = frame_count

        # ----- Object analysis -----
        if not cached_is_human:
            cached_object_type = analyze_object(small_frame)
        else:
            cached_object_type = "HUMAN"

    object_type = cached_object_type
    style = ghost_styles[object_type]

    # ---------- Draw ghost ----------
    frame = draw_carbon_ghost(frame, center, style)

    # ---------- Send to Firebase ONLY on change ----------
    if object_type != last_object_sent:
        send_to_firebase_async(object_type)
        last_object_sent = object_type

    # ---------- UI ----------
    label = (
        "Human detected — no carbon ghost"
        if object_type == "HUMAN"
        else f"Impact: {object_type}"
    )

    cv2.putText(
        frame,
        label,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
        (255, 255, 255),
        3
    )

    cv2.rectangle(
        frame,
        (center[0]-40, center[1]-40),
        (center[0]+40, center[1]+40),
        (255, 255, 255),
        2
    )

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

    try:
        if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break
    except:
        break

# ===============================
# CLEANUP
# ===============================
cap.release()
cv2.destroyAllWindows()
print("Camera closed safely.")
