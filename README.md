# Retail AI — Week 1 Setup Complete ✓

**Performance Implications:**
- YOLOv8n runs on **CPU only** 
---

## Files Created

### 1. `tracker.py` — Main perception engine
**What it does:**
- Connects to IP Webcam at `http://192.168.100.4:8080/video`
- Resizes frames to 640×480 for YOLO
- Detects people (YOLO class 0) every frame
- Groups detections into **4 zones** (Entrance, Aisle_1, Checkout, Aisle_2)
- Logs zone counts to SQLite every 5 seconds
- Displays live video with:
  - Yellow zone rectangles
  - Green bounding boxes around people
  - Red center dots for tracking
  - Text HUD showing zone counts

**Run:**
```bash
python3 tracker.py
```
**Exit:** Press `Q` in the window

**Troubleshooting:**
- **Black screen**: Make sure IP Webcam is running on your phone at `http://192.168.100.4:8080`
- **No people detected**: Ensure good lighting and person is >100px tall in frame
- **Slow**: Normal on CPU — your i5-3317U can handle YOLOv8n at ~5-10 FPS

---

### 2. `query.py` — Data insights
**What it does:**
- Reads `store_data.db` and prints stats
- Shows busiest zones (last hour)
- Generates weekly summary

**Run (after tracker.py has collected some data):**
```bash
python3 query.py
```

**Example output:**
```
==================================================
Retail AI — Database Query Tool
==================================================
Total records in DB: 120
Data range: 2026-06-13 12:00:00 → 2026-06-13 12:10:00
Zones: Aisle_1, Aisle_2, Checkout, Entrance

Busiest zones (last hour):
  Aisle_1: 45 people-seconds
  Entrance: 38 people-seconds
  ...
```

---

### 3. `calibrate.py` — Interactive zone definition
**What it does:**
- Connects to IP Webcam
- Reads first frame
- You **click and drag** to draw zone rectangles on screen
- Type zone name for each rectangle
- Saves zones to `zones_config.json`

**Run:**
```bash
python3 calibrate.py
```

**Usage:**
1. Click and drag to draw a rectangle
2. Type zone name (e.g., `Electronics`, `Frozen`, `Checkout`)
3. Press ENTER
4. Repeat for each zone
5. Press `S` to save, `Q` to quit

**Output:** `zones_config.json`
```json
{
  "frame_width": 640,
  "frame_height": 480,
  "zones": [
    {"name": "Electronics", "x1": 0, "y1": 0, "x2": 320, "y2": 240},
    ...
  ]
}
```

---

## Next Steps (Week 1 remaining)

### Immediate (now):
1. **Test tracker.py** with IP Webcam running
2. **Collect 10–15 minutes** of sample data
3. **Run query.py** to confirm pipeline works

### This week:
1. **Calibrate zones** using `calibrate.py` for your actual store layout
2. **Add dwell time tracking** (foundation for Week 2)
3. **Build basic query dashboard** (Flask + Chart.js showing zone trends)

---

## Database Schema

### `zone_logs` table:
```sql
id        | timestamp           | zone_name | count
1         | 2026-06-13 12:00:05 | Entrance  | 3
2         | 2026-06-13 12:00:05 | Aisle_1   | 5
3         | 2026-06-13 12:00:05 | Checkout  | 1
...
```

Each row = one zone's count at one timestamp (logged every 5 seconds)

---

## Stack Confirmation
| Layer | Technology |
|-------|------------|
| Camera | IP Webcam (Android app) |
| People detection | YOLOv8n (CPU inference) |
| Data storage | SQLite |
| Backend | Flask (Week 4) |
| Frontend | React + Chart.js (Week 4) |
| AI engine | Claude API (Week 3) |

---

## Recommended Workflow

**Day 1–2:** Get tracker running, verify data flows end-to-end
```bash
# Terminal 1
python3 tracker.py

# Terminal 2 (after 1–2 min of data collection)
watch -n 5 python3 query.py
```

**Day 3:** Calibrate zones for real store layout
```bash
python3 calibrate.py
# Update tracker.py to read zones_config.json
```

**Day 4–5:** Add dwell time per person (prepare for Week 2)

**Day 6–7:** Build basic Flask dashboard showing live zone counts

---

## Resources
- [YOLOv8 Docs](https://github.com/ultralytics/ultralytics)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [OpenCV Python Docs](https://docs.opencv.org/)

**Questions?** Check the project export at `/home/usman-saleem/Downloads/retail_ai_project_export.md`

Good luck! 🚀
