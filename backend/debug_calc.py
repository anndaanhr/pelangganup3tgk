
import sys
import os
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parent
sys.path.append(str(backend_path))

from database import SessionLocal
from services.analysis import AnalysisService
import json

def test_calc():
    print("Starting debug calculation...")
    db = SessionLocal()
    try:
        service = AnalysisService(db)
        
        # Force calculation (ignore cache handling in script, just call the logic or clear cache first)
        if os.path.exists("stats_cache.json"):
            os.remove("stats_cache.json")
            
        stats = service.get_dashboard_stats()
        
        print("\n--- RESULT ---")
        print(f"Total Revenue 2025: {stats.total_revenue_2025}")
        print(f"Total Energy 2025: {stats.total_energy_2025}")
        
        # Check if saved to cache
        if os.path.exists("stats_cache.json"):
            with open("stats_cache.json", 'r') as f:
                data = json.load(f)
                rev = data['dashboard_stats'].get('total_revenue_2025')
                print(f"Cache Total Revenue 2025: {rev}")
                if rev is not None:
                    print("SUCCESS: Cache contains new field.")
                else:
                    print("FAILURE: Cache missing new field.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_calc()
