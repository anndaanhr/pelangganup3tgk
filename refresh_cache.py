import os
import sys
import time

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from database import SessionLocal
from services.analysis import AnalysisService, save_cache_to_disk

print("=== GENERATING DASHBOARD CACHE (FULL) ===")
print("Connecting to database...")
db = SessionLocal()
service = AnalysisService(db)

start_time = time.time()

# 1. Dashboard Stats
print("\n[1/3] Calculating Dashboard Summary Stats...")
stats = service.get_dashboard_stats()
print("  -> Done!")

# 2. Trends
print("\n[2/3] Calculating Aggregate Trends...")
trends = service.get_aggregate_trends()
print(f"  -> Done! ({len(trends)} months)")

# 3. Distribution
print("\n[3/3] Calculating Distribution Stats...")
dist = service.get_distribution_stats()
print("  -> Done!")

end_time = time.time()
print("\n=== CACHE GENERATION COMPLETE ===")
print(f"Total Time: {round(end_time - start_time, 2)} seconds")
print("All data has been saved to 'stats_cache.json'.")
print("Restart backend and refresh NOW!")
