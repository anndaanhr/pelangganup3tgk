import sys
import os
import requests
import psycopg2
from sqlalchemy import create_engine, text

# Configuration
DB_URL = "postgresql://postgres:postgres@localhost:5432/pln_trend_db"
API_URL = "http://localhost:8000/api/customers/dashboard"

def check_database():
    print("\n[1] Checking Database Connection & Content...")
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Check tables
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
        tables = [t[0] for t in cur.fetchall()]
        print(f"    Tables found: {tables}")
        
        if 'customers_2024' in tables:
            cur.execute("SELECT COUNT(*) FROM customers_2024;")
            count24 = cur.fetchone()[0]
            print(f"    Rows in customers_2024: {count24}")
        else:
            print("    ! customers_2024 table MISSING")
            
        if 'customers_2025' in tables:
            cur.execute("SELECT COUNT(*) FROM customers_2025;")
            count25 = cur.fetchone()[0]
            print(f"    Rows in customers_2025: {count25}")
        else:
            print("    ! customers_2025 table MISSING")
            
        conn.close()
        return True
    except Exception as e:
        print(f"    ! Database Connection FAILED: {e}")
        return False

def check_backend_api():
    print("\n[2] Checking Backend API...")
    try:
        response = requests.get(API_URL, timeout=5)
        print(f"    Status Code: {response.status_code}")
        if response.status_code == 200:
            print("    API Response Content (First 100 chars):")
            print(f"    {str(response.json())[:100]}")
            return True
        else:
            print(f"    ! API Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("    ! Connection Refused. Is the backend running? (python -m uvicorn main:app)")
        return False
    except Exception as e:
        print(f"    ! API Check Failed: {e}")
        return False

def check_files():
    print("\n[3] Checking Critical Files...")
    files = [
        "backend/.env",
        "backend/main.py",
        "backend/database.py",
        "backend/models.py",
        "backend/services/analysis.py",
        "frontend/src/services/api.ts"
    ]
    for f in files:
        if os.path.exists(f):
            print(f"    [OK] {f}")
        else:
            print(f"    [MISSING] {f}")

if __name__ == "__main__":
    print("=== SYSTEM DIAGNOSTIC TOOL ===")
    
    db_ok = check_database()
    api_ok = check_backend_api()
    check_files()
    
    print("\n=== DIAGNOSIS SUMMARY ===")
    if not db_ok:
        print("CRITICAL: Database connection failed or empty. Check credentials and run import.")
    if not api_ok:
        print("CRITICAL: Backend API is not accessible. Make sure 'uvicorn' is running.")
    if db_ok and api_ok:
        print("SUCCESS: Database and API seem healthy. Issues might be in Frontend code or Browser Cache.")
