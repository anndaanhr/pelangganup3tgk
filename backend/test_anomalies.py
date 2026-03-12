import sys
sys.path.append("d:\\pln2juta\\backend")
from database import SessionLocal
from services.advanced_analysis import AdvancedAnalysisService
from models import Customer2025

db = SessionLocal()
svc = AdvancedAnalysisService(db)
res = svc.get_anomalies_high_variance(limit=5)
print("Total Anomalies:", res['total'])

ids = [r['idpel'] for r in res['data']]
customers = db.query(Customer2025).filter(Customer2025.idpel.in_(ids)).all()

for c in customers:
    vals = [c.jan_2025, c.feb_2025, c.mar_2025, c.apr_2025, c.may_2025, c.jun_2025, 
            c.jul_2025, c.aug_2025, c.sep_2025, c.oct_2025, c.nov_2025, c.dec_2025]
    vals = [float(v or 0) for v in vals]
    print(f"ID: {c.idpel}, Zeros: {vals.count(0)}, Values: {vals}")
