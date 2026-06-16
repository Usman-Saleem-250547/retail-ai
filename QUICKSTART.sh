#!/usr/bin/env bash
# QUICKSTART — Week 1 Phase 1 Complete ✓

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         Retail AI — Week 1 Setup Complete ✓               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "📁 FILES CREATED:"
echo "  ✓ tracker.py .......... Main perception engine (zone detection)"
echo "  ✓ query.py ............ Database insights tool"
echo "  ✓ calibrate.py ........ Interactive zone definition"
echo "  ✓ README.md ........... Full documentation"
echo "  ✓ store_data.db ....... SQLite database (auto-created)"
echo ""

echo "🚀 NEXT STEPS:"
echo ""
echo "1. START TRACKER (requires IP Webcam running on your phone)"
echo "   $ python3 tracker.py"
echo "   • Press Q to quit"
echo "   • Displays live camera with zone detection"
echo "   • Logs to store_data.db every 5 seconds"
echo ""

echo "2. QUERY RESULTS (in another terminal after 1-2 min of data)"
echo "   $ python3 query.py"
echo "   • Shows total records, time range, busiest zones"
echo "   • Confirms end-to-end data pipeline works"
echo ""

echo "3. CALIBRATE ZONES (customize for your store)"
echo "   $ python3 calibrate.py"
echo "   • Click + drag to draw zone rectangles"
echo "   • Type zone names (e.g., 'Electronics', 'Frozen')"
echo "   • Saves to zones_config.json"
echo "   • tracker.py will auto-load these zones next time"
echo ""

echo "🔧 TROUBLESHOOTING:"
echo ""
echo "Q: Black screen in tracker window?"
echo "A: Ensure IP Webcam is running on your phone at:"
echo "   http://192.168.100.4:8080/video"
echo "   Test in browser first!"
echo ""

echo "Q: No people detected?"
echo "A: Check lighting. Person must be ~100px+ tall in frame."
echo "   YOLOv8n is good but not perfect on old CPU."
echo ""

echo "Q: Very slow / laggy?"
echo "A: Normal for i5-3317U. You're getting 5-10 FPS."
echo "   For production → get Jetson Nano (USD 99) or NVIDIA GPU."
echo ""

echo "Q: Database file looks empty?"
echo "A: Run tracker.py for 30+ seconds, then run query.py"
echo ""

echo "📚 FULL DOCS:"
echo "   Read README.md in this folder"
echo ""

echo "✨ That's it! You're ready to test Week 1."
echo "   Report back when tracker.py is running smoothly."
echo ""
