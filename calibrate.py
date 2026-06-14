#!/usr/bin/env python3
"""Interactive zone calibration tool — draw zones with your mouse."""

import cv2
import json
import os
from datetime import datetime

CAMERA_URL = "http://192.168.100.4:8080/video"
CONFIG_FILE = "zones_config.json"

class ZoneCalibrator:
    def __init__(self):
        self.frame = None
        self.drawing = False
        self.zones = []
        self.current_zone = {"name": "", "x1": 0, "y1": 0, "x2": 0, "y2": 0}
        self.zone_names = []

    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events for zone drawing."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.current_zone["x1"] = x
            self.current_zone["y1"] = y
            print(f"Starting zone at ({x}, {y})")

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.current_zone["x2"] = x
                self.current_zone["y2"] = y

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.current_zone["x2"] = x
            self.current_zone["y2"] = y
            print(f"Zone box defined: ({self.current_zone['x1']}, {self.current_zone['y1']}) to ({x}, {y})")
            print("Type zone name (e.g., 'Entrance') and press ENTER (or just ENTER to skip):")

    def render_frame(self):
        """Draw zones on frame."""
        display = self.frame.copy()
        
        # Draw completed zones
        for i, zone in enumerate(self.zones):
            x1, y1, x2, y2 = zone["x1"], zone["y1"], zone["x2"], zone["y2"]
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(display, zone["name"], (x1 + 6, y1 - 6),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Draw current zone being drawn
        if self.drawing:
            x1, y1, x2, y2 = self.current_zone["x1"], self.current_zone["y1"], \
                             self.current_zone["x2"], self.current_zone["y2"]
            cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 255), 2)

        # Instructions
        cv2.rectangle(display, (0, 0), (400, 100), (0, 0, 0), -1)
        cv2.putText(display, "Draw zones (click + drag)", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(display, "Press 'S' to save, 'C' to clear, 'Q' to quit", (10, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(display, f"Zones defined: {len(self.zones)}", (10, 75),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        return display

    def save_config(self):
        """Save zones to JSON."""
        config = {"frame_width": 640, "frame_height": 480, "zones": self.zones}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
        print(f"✓ Saved {len(self.zones)} zones to {CONFIG_FILE}")

    def run(self):
        """Main calibration loop."""
        print(f"Connecting to {CAMERA_URL}...")
        cap = cv2.VideoCapture(CAMERA_URL)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            print("ERROR: Could not connect to camera.")
            return

        print("Reading first frame...")
        ret, frame = cap.read()
        if not ret:
            print("ERROR: Could not read frame.")
            return

        self.frame = cv2.resize(frame, (640, 480))
        cv2.namedWindow("Zone Calibrator")
        cv2.setMouseCallback("Zone Calibrator", self.mouse_callback)

        print("\nInstructions:")
        print("1. Click and drag to draw a zone rectangle")
        print("2. Type the zone name and press ENTER")
        print("3. Repeat for each zone")
        print("4. Press 'S' to save, 'Q' to quit")

        while True:
            display = self.render_frame()
            cv2.imshow("Zone Calibrator", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Quitting...")
                break
            elif key == ord('s'):
                if self.zones:
                    self.save_config()
                else:
                    print("No zones to save.")
            elif key == ord('c'):
                self.zones = []
                print("Cleared all zones.")

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    calibrator = ZoneCalibrator()
    calibrator.run()
