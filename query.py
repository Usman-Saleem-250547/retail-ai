#!/usr/bin/env python3
"""Query store_data.db for insights."""

import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

DB_FILE = "store_data.db"

def get_db_stats():
    """Print overall database statistics."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM zone_logs")
    total_records = c.fetchone()[0]
    print(f"Total records in DB: {total_records}")

    if total_records == 0:
        print("No data yet. Run tracker.py to collect data.")
        conn.close()
        return

    c.execute("SELECT MIN(timestamp), MAX(timestamp) FROM zone_logs")
    min_ts, max_ts = c.fetchone()
    print(f"Data range: {min_ts} → {max_ts}")

    c.execute("SELECT DISTINCT zone_name FROM zone_logs ORDER BY zone_name")
    zones = [row[0] for row in c.fetchall()]
    print(f"Zones: {', '.join(zones)}")

def get_busiest_zone_last_hour():
    """Find busiest zone in the last hour."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    cutoff = datetime.now() - timedelta(hours=1)
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        SELECT zone_name, SUM(count) as total
        FROM zone_logs
        WHERE timestamp > ?
        GROUP BY zone_name
        ORDER BY total DESC
    """, (cutoff_str,))

    results = c.fetchall()
    print(f"\nBusiest zones (last hour):")
    if results:
        for zone, total in results:
            print(f"  {zone}: {total} people-seconds")
    else:
        print("  No data in last hour.")
    conn.close()

def get_weekly_summary():
    """Generate a weekly summary."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        SELECT zone_name, SUM(count) as total, AVG(count) as avg, MAX(count) as peak
        FROM zone_logs
        GROUP BY zone_name
        ORDER BY total DESC
    """)

    results = c.fetchall()
    print(f"\nWeekly summary (all-time):")
    if results:
        for zone, total, avg, peak in results:
            print(f"  {zone}:")
            print(f"    Total footfall: {total}")
            print(f"    Average per log: {avg:.1f}")
            print(f"    Peak: {peak}")
    else:
        print("  No data.")
    conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Retail AI — Database Query Tool")
    print("=" * 50)
    get_db_stats()
    get_busiest_zone_last_hour()
    get_weekly_summary()
