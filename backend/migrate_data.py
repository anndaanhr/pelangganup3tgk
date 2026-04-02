import sys
import psycopg2
import requests
import json
from decimal import Decimal

local_url = "postgresql://postgres:postgres@localhost:5432/pln_trend_db"
SUPABASE_URL = "https://xitfkephwdhxgeyjicmz.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhpdGZrZXBod2RoeGdleWppY216Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMzMzI0NDgsImV4cCI6MjA4ODkwODQ0OH0.cWNxfTGFkxiCffIsACQ05Dz82Z5UXL43RGXw8ti5VO8"

headers = {
    "apikey": ANON_KEY,
    "Authorization": f"Bearer {ANON_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def migrate_table(table_name):
    try:
        conn = psycopg2.connect(local_url)
        cur = conn.cursor()
        cur.itersize = 2000
        cur.execute(f"SELECT * FROM {table_name}")
    except Exception as e:
        print(f"Cannot connect or read {table_name}:", e)
        return

    colnames = [desc[0] for desc in cur.description]
    BATCH_SIZE = 2000
    total_inserted = 0

    print(f"Starting migration of {table_name}...")

    while True:
        rows = cur.fetchmany(BATCH_SIZE)
        if not rows:
            break
        
        payload = []
        for row in rows:
            d = {}
            for idx, col in enumerate(colnames):
                val = row[idx]
                if isinstance(val, Decimal):
                    d[col] = float(val)
                else:
                    d[col] = val
            payload.append(d)
            
        req_url = f"{SUPABASE_URL}/rest/v1/{table_name}"
        response = requests.post(req_url, headers=headers, json=payload)
        
        if response.status_code >= 300:
            print(f"Error inserting batch in {table_name}: {response.text}")
            break
        else:
            total_inserted += len(payload)
            print(f"Inserted {total_inserted} rows into {table_name}")

    print(f"Finished. Total inserted into {table_name}: {total_inserted}")
    cur.close()
    conn.close()

if __name__ == "__main__":
    # customers_2025 done. Now migrate 2024 data.
    migrate_table("customers_2024")
