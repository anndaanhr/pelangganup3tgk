import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.analysis import AnalysisService
from database import Base
from dotenv import load_dotenv

load_dotenv('backend/.env')
DB_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/pln_trend_db"

print(f"Connecting to {DB_URL}...")
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()
service = AnalysisService(session)

print("\n--- TEST 1: DISTRIBUTION STATS ---")
try:
    dist = service.get_distribution_stats()
    print("SUCCESS!")
    print(dist)
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\n--- TEST 2: AGGREGATE TRENDS ---")
try:
    trends = service.get_aggregate_trends()
    print("SUCCESS!")
    # print first 2 items
    print(trends[:2])
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

session.close()
