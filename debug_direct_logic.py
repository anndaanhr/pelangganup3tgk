import sys
import os
# Add backend to path so we can import modules as if we were in backend/
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# Import directly as top-level modules
from models import Customer2024, Customer2025
from services.analysis import AnalysisService
from database import Base
from dotenv import load_dotenv

# Load env from backend/.env
load_dotenv('backend/.env')

DB_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/pln_trend_db"
print(f"DEBUG: Connecting to {DB_URL}")

try:
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # 1. Raw SQL Count
    print("\n--- 1. RAW SQL COUNTS ---")
    try:
        c24 = session.execute(text("SELECT count(*) FROM customers_2024")).scalar()
        c25 = session.execute(text("SELECT count(*) FROM customers_2025")).scalar()
        print(f"Raw customers_2024: {c24}")
        print(f"Raw customers_2025: {c25}")
    except Exception as e:
        print(f"Raw SQL Failed: {e}")

    # 2. ORM Count
    print("\n--- 2. ORM MODEL COUNTS ---")
    try:
        orm24 = session.query(Customer2024).count()
        orm25 = session.query(Customer2025).count()
        print(f"ORM Customer2024: {orm24}")
        print(f"ORM Customer2025: {orm25}")
    except Exception as e:
        print(f"ORM Failed: {e}")

    # 3. Service Logic
    print("\n--- 3. SERVICE LOGIC CHECK ---")
    try:
        service = AnalysisService(session)
        stats = service.get_dashboard_stats()
        print("AnalysisService.get_dashboard_stats() result:")
        print(stats.model_dump() if hasattr(stats, 'model_dump') else stats.dict())
    except Exception as e:
        print(f"Service Logic Failed: {e}")
        import traceback
        traceback.print_exc()

    session.close()

except Exception as e:
    print(f"FATAL ERROR: {e}")
