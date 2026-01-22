import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv('backend/.env')
DB_URL = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/pln_trend_db"

print(f"Connecting to {DB_URL}...")
try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        for t in ['customers_2024', 'customers_2025']:
            try:
                c = conn.execute(text(f"SELECT count(*) FROM {t}")).scalar()
                print(f"TABLE {t}: {c} rows")
            except Exception as e:
                print(f"TABLE {t}: ERROR {e}")
except Exception as e:
    print(f"CONNECTION ERROR: {e}")
