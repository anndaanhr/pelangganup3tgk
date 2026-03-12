
print("Checking Anomaly Logic...")
from database import SessionLocal
from services.advanced_analysis import AdvancedAnalysisService

try:
    db = SessionLocal()
    service = AdvancedAnalysisService(db)
    print("Calling get_anomalies_zero_usage...")
    results = service.get_anomalies_zero_usage(limit=10)
    print(f"Success. Found {len(results)} anomalies.")
    for r in results:
        print(r)
except Exception as e:
    print(f"Detailed Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
