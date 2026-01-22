import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load env variables
load_dotenv('backend/.env')

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL or "postgres" not in DB_URL:
    print("Warning: DATABASE_URL not found or invalid. Using default.")
    DB_URL = "postgresql://postgres:postgres@localhost:5432/pln_trend_db"

print(f"Connecting to: {DB_URL}")

try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        
        # List of indexes to create
        indexes = [
            # 2024 Tables
            "CREATE INDEX IF NOT EXISTS idx_customers_2024_idpel ON customers_2024 (idpel);",
            "CREATE INDEX IF NOT EXISTS idx_customers_2024_tarif ON customers_2024 (tarif);",
            "CREATE INDEX IF NOT EXISTS idx_customers_2024_layanan ON customers_2024 (layanan);",
            "CREATE INDEX IF NOT EXISTS idx_customers_2024_gardu ON customers_2024 (gardu);",
            
            # 2025 Tables
            "CREATE INDEX IF NOT EXISTS idx_customers_2025_idpel ON customers_2025 (idpel);",
            "CREATE INDEX IF NOT EXISTS idx_customers_2025_tarif ON customers_2025 (tarif);",
            "CREATE INDEX IF NOT EXISTS idx_customers_2025_layanan ON customers_2025 (layanan);",
            "CREATE INDEX IF NOT EXISTS idx_customers_2025_gardu ON customers_2025 (gardu);"
        ]
        
        print("Creating indexes... This might take a minute.")
        
        for sql in indexes:
            print(f"Executing: {sql}")
            try:
                conn.execute(text(sql))
                print("  -> Done.")
            except Exception as e:
                print(f"  -> Failed: {e}")
                
    print("\nSUCCESS: All indexes created/checked!")

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
