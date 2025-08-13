import schedule
import time
import subprocess
from datetime import datetime
import os

# ----------------------------------------
# Paths relative to backend folder
# ----------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

YOUTUBE_SCRIPT = os.path.join(BASE_DIR, "..", "youtube", "filter_ideas.py")
REDDIT_SCRIPT = os.path.join(BASE_DIR, "..", "reddit_scraper", "reddit_scraper.py")
COMBINED_SCRIPT = os.path.join(BASE_DIR, "..", "combined", "combined.py")

def run_refresh():
    print(f"\n⏱ Refresh started at {datetime.now()}\n")
    
    # Run YouTube ideas generation
    try:
        subprocess.run(["python", YOUTUBE_SCRIPT], check=True)
        print("✅ YouTube ideas refreshed.")
    except Exception as e:
        print(f"❌ YouTube script failed: {e}")
    
    # Run Reddit scraper + classification
    try:
        subprocess.run(["python", REDDIT_SCRIPT], check=True)
        print("✅ Reddit posts refreshed.")
    except Exception as e:
        print(f"❌ Reddit script failed: {e}")
    
    # Run combined generation
    try:
        subprocess.run(["python", COMBINED_SCRIPT], check=True)
        print("✅ Combined topics refreshed.")
    except Exception as e:
        print(f"❌ Combined script failed: {e}")

    print(f"⏱ Refresh completed at {datetime.now()}\n")

# ----------------------------------------
# Schedule the job (every 6 hours)
# ----------------------------------------
schedule.every(6).hours.do(run_refresh)

print("📅 Auto-refresh scheduler started. Press Ctrl+C to exit.")

# Initial run
run_refresh()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
