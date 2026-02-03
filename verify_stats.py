import sys
import os

# Add backend directory to path
sys.path.append(os.path.abspath("backend"))

from database import SessionLocal
from services.analysis import AnalysisService

def verify_stats():
    db = SessionLocal()
    try:
        service = AnalysisService(db)
        print("Calculating stats...")
        stats = service.get_dashboard_stats()
        print("\n--- STATS RESULT ---")
        print(f"Total Energy 2024: {stats.total_energy_2024}")
        print(f"Total Energy 2025: {stats.total_energy_2025}")
        print(f"Total Customers 2025: {stats.total_customers_2025}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_stats()
