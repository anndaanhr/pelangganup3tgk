from sqlalchemy import create_engine, text
import sys

# Explicitly use the credentials the user confirmed
DB_URL = "postgresql://postgres:postgres@localhost:5432/pln_trend_db"

print(f"Connecting to: {DB_URL}")

try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        print("Connection Successful!")
        
        # Check Tables
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"Tables: {tables}")
        
        # Check Counts
        if 'customers_2024' in tables:
            count = conn.execute(text("SELECT COUNT(*) FROM customers_2024")).scalar()
            print(f"Count 2024: {count}")
        
        if 'customers_2025' in tables:
            count = conn.execute(text("SELECT COUNT(*) FROM customers_2025")).scalar()
            print(f"Count 2025: {count}")
            
except Exception as e:
    print(f"ERROR: {e}")
