import cv2
from ultralytics import YOLO
import time
import sqlite3
from datetime import datetime
import json
import logging
logging.disable(logging.WARNING)
import os
os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"] = "1"
import warnings
warnings.filterwarnings("ignore")

# ─── CONFIG ───────────────────────────────────────────────
CAMERA_URL = "http://192.168.100.4:8080/video"
DB_FILE    = "store_data.db"
CONFIG_FILE = "zones_config.json"
LOG_EVERY  = 5   # seconds between database logs

# ─── DEFAULT ZONES (used if no config file exists) ────────
DEFAULT_ZONES = [
    ("Entrance",  0,   0,   320, 240),
    ("Aisle_1",   320, 0,   640, 240),
    ("Checkout",  0,   240, 320, 480),
    ("Aisle_2",   320, 240, 640, 480),
]

# ─── LOAD ZONES ────────────────────────────────────────────
def load_zones():
    """Load zones from config file or use defaults."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                zones = []
                for z in config.get("zones", []):
                    zones.append((z["name"], z["x1"], z["y1"], z["x2"], z["y2"]))
                print(f"✓ Loaded {len(zones)} zones from {CONFIG_FILE}")
                return zones
        except Exception as e:
            print(f"⚠ Error reading {CONFIG_FILE}: {e}")
            print(f"Using default zones...")
    
    print(f"Using default zones. Run 'calibrate.py' to customize.")
    return DEFAULT_ZONES

ZONES = load_zones()

# ─── DATABASE SETUP ───────────────────────────────────────
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS zone_logs (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            zone_name TEXT,
            count     INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def log_to_db(zone_counts):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for zone, count in zone_counts.items():
        c.execute(
            "INSERT INTO zone_logs (timestamp, zone_name, count) VALUES (?, ?, ?)",
            (ts, zone, count)
        )
    conn.commit()
    conn.close()

# ─── ZONE HELPER ──────────────────────────────────────────
def get_zone(cx, cy):
    for name, x1, y1, x2, y2 in ZONES:
        if x1 <= cx <= x2 and y1 <= cy <= y2:
            return name
    return None

def draw_zones(frame):
    for name, x1, y1, x2, y2 in ZONES:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(frame, name, (x1 + 6, y1 + 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

# ─── MAIN ─────────────────────────────────────────────────
def main():
    init_db()
    model = YOLO("yolov8n.pt")

    print(f"Connecting to camera: {CAMERA_URL}")
    cap = cv2.VideoCapture(CAMERA_URL)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("ERROR: Could not open camera stream.")
        print("Make sure IP Webcam is running and the URL is correct.")
        print(f"Test: Open {CAMERA_URL} in your browser.")
        return

    print("✓ Camera connected. Press Q to quit.")
    last_log_time = time.time()

    while True:
        # Flush stale frames to get fresh data
        for _ in range(3):
            cap.grab()
        ret, frame = cap.read()
        if not ret:
            print("Lost camera feed, retrying...")
            time.sleep(1)
            continue

        # Resize to 640x480 for consistent YOLO and zone detection
        frame = cv2.resize(frame, (640, 480))

        # Run YOLO — only detect people (class 0)
        results = model(frame, classes=[0], verbose=False)[0]

        # Count people per zone
        zone_counts = {z[0]: 0 for z in ZONES}
        total = 0

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = (x1 + x2) // 2  # center x
            cy = (y1 + y2) // 2  # center y

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

            zone = get_zone(cx, cy)
            if zone:
                zone_counts[zone] += 1
            total += 1

        # Draw zones on frame
        draw_zones(frame)

        # HUD — top left info panel
        cv2.rectangle(frame, (0, 0), (220, 30 + len(ZONES) * 24), (0, 0, 0), -1)
        cv2.putText(frame, f"Total: {total}", (8, 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
        for i, (zone, count) in enumerate(zone_counts.items()):
            cv2.putText(frame, f"  {zone}: {count}", (8, 46 + i * 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

        # Log to DB every N seconds
        if time.time() - last_log_time >= LOG_EVERY:
            log_to_db(zone_counts)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged — {zone_counts}")
            last_log_time = time.time()

        cv2.imshow("Retail AI — Zone Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Stopped.")

if __name__ == "__main__":
    main()
