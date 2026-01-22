import os
from sqlalchemy import create_engine, text

# HARDCODED credentials to match what we think is correct
DB_URL = "postgresql://postgres:postgres@localhost:5432/pln_trend_db"

print(f"Connecting to: {DB_URL}")
try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        # Get ALL table names
        query = text("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        result = conn.execute(query).fetchall()
        print("\n--- TABLES FOUND ---")
        tables = [r[0] for r in result]
        for t in tables:
            # Count rows for each table
            try:
                count = conn.execute(text(f'SELECT count(*) FROM "{t}"')).scalar()
                print(f"{t}: {count} rows")
            except:
                print(f"{t}: (error counting)")
        print("--------------------\n")
except Exception as e:
    print(f"CONNECTION ERROR: {e}")
