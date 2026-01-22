import os
import requests
import psycopg2
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Force load Env
load_dotenv('backend/.env')

LOG_FILE = "debug_output.txt"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a") as f:
        f.write(str(msg) + "\n")

# Clear log
with open(LOG_FILE, "w") as f:
    f.write("Map started\n")

# 1. Check Database
log("\n--- 1. DATABASE CHECK ---")
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    DB_URL = "postgresql://postgres:postgres@localhost:5432/pln_trend_db"
log(f"Connecting to: {DB_URL}")

try:
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        log("✅ Connection Successful!")
        
        # Check Tables
        tables = conn.execute(text("SELECT text(tablename) FROM pg_tables WHERE schemaname = 'public';")).fetchall()
        table_names = [t[0] for t in tables]
        log(f"Tables found: {table_names}")
        
        for table in ['customers_2024', 'customers_2025']:
            if table in table_names:
                count = conn.execute(text(f"SELECT count(*) FROM {table}")).scalar()
                log(f"   -> {table}: {count} rows")
            else:
                log(f"   ❌ {table}: MISSING!")
except Exception as e:
    log(f"❌ Database Error: {e}")

# 2. Check API
log("\n--- 2. API CHECK ---")
API_URL = "http://localhost:8000"
try:
    # Root
    r = requests.get(f"{API_URL}/", timeout=5)
    log(f"Root (/): {r.status_code}")
    
    # Dashboard
    r = requests.get(f"{API_URL}/api/customers/dashboard", timeout=5)
    log(f"Dashboard (/api/customers/dashboard): {r.status_code}")
    if r.status_code == 200:
        log("   -> Data: " + str(r.json())[:100] + "...")
    else:
        log("   -> Error: " + r.text)

except Exception as e:
    log(f"❌ API Error: {e}")
