"""
Script import Excel KHUSUS untuk data 2025 (Full Replace) - OPTIMIZED
Target File: JUAL PERPELANGGAN 2025 BL2.xlsx
Uses Pandas to_sql for speed. 
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sqlalchemy import text
from database import engine
from dotenv import load_dotenv
import time
import datetime

load_dotenv()

# Mapping kolom bulanan (Keys match str(datetime object))
# Note: Pandas automatically converts Excel dates to datetime objects
MONTH_MAP_2025 = {
    '2024-12-01 00:00:00': 'dec_2024',
    '2025-01-01 00:00:00': 'jan_2025',
    '2025-02-01 00:00:00': 'feb_2025',
    '2025-03-01 00:00:00': 'mar_2025',
    '2025-04-01 00:00:00': 'apr_2025',
    '2025-05-01 00:00:00': 'may_2025',
    '2025-06-01 00:00:00': 'jun_2025',
    '2025-07-01 00:00:00': 'jul_2025',
    '2025-08-01 00:00:00': 'aug_2025',
    '2025-09-01 00:00:00': 'sep_2025',
    '2025-10-01 00:00:00': 'oct_2025',
    '2025-11-01 00:00:00': 'nov_2025',
    '2025-12-01 00:00:00': 'dec_2025',
}

COLUMN_MAPPING = {
    'UNITUP': 'unitup',
    'IDPEL': 'idpel',
    'NAMA': 'nama',
    'ALAMAT': 'alamat',
    'TARIF': 'tarif',
    'DAYA': 'daya',
    'KDDK': 'kddk',
    'CATER': 'cater',
    'PENYULANG': 'penyulang',
    'GARDU': 'gardu',
    'NOMOR METER': 'nomor_meter',
    'JENIS': 'jenis',
    'LAYANAN': 'layanan',
    'KD PROSES': 'kd_proses'
}

BATCH_SIZE = 10000 

def import_2025_full():
    print("=" * 70)
    print("IMPORT DATA FULL 2025 (REPLACE) - OPTIMIZED")
    print("File: JUAL PERPELANGGAN 2025 BL2.xlsx")
    print("=" * 70)
    
    project_root = Path(__file__).resolve().parent.parent.parent
    excel_file = project_root / "JUAL PERPELANGGAN 2025 BL2.xlsx"
    
    if not excel_file.exists():
        print(f"[ERROR] File not found: {excel_file}")
        return

    # 1. Truncate Table
    print("\n[1/4] Truncating 'customers_2025'...")
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE customers_2025 RESTART IDENTITY;"))
        conn.commit()
    print("  Table truncated.")

    # 2. Count Rows (Optional fast approximate check, or skip)
    # Skipping row count for speed, we'll see progress by chunks.

    # 3. Import Data
    print("\n[2/4] Importing data (Reading full file into memory)...")
    
    start_time = time.time()
    
    try:
        # Read entire file
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        print(f"  File read successfully. Total rows: {len(df):,}")
        
        # 1. Rename Standard Columns
        df.rename(columns=COLUMN_MAPPING, inplace=True)
        
        # 2. Rename Date Columns
        date_col_map = {}
        for col in df.columns:
            col_str = str(col)
            if col_str in MONTH_MAP_2025:
                date_col_map[col] = MONTH_MAP_2025[col_str]
        df.rename(columns=date_col_map, inplace=True)
        
        # 3. Clean IDPEL
        df = df.dropna(subset=['idpel'])
        df['idpel'] = pd.to_numeric(df['idpel'], errors='coerce')
        df = df.dropna(subset=['idpel'])
        df['idpel'] = df['idpel'].astype('int64')

        # Clean Other Numerics
        numeric_cols = ['unitup', 'daya', 'nomor_meter']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int64')

        # Clean Monthly Consumption (Float)
        monthly_cols = list(MONTH_MAP_2025.values())
        for col in monthly_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

        # 4. Remove Duplicates
        initial_len = len(df)
        df = df.drop_duplicates(subset=['idpel'])
        if len(df) < initial_len:
            print(f"  Removed {initial_len - len(df):,} duplicate IDPELs.")
            
        # 5. Filter columns
        allowed_cols = list(COLUMN_MAPPING.values()) + list(MONTH_MAP_2025.values())
        cols_to_keep = [c for c in df.columns if c in allowed_cols]
        df = df[cols_to_keep]
        
        print(f"  Inserting {len(df):,} rows into database...")
        
        # 6. Insert with Chunksize (handling transaction in chunks)
        # Use simple method (None) which uses execute_many, safer for larger batches than 'multi' if params exceed limit
        # 'multi' is faster but limited by max_params (65535). 
        # Rows * Cols <= 65535. 
        # We have ~27 columns. 65535 / 27 ~= 2400 rows max per batch for 'multi'.
        # So chunksize=2000 with method='multi' is safe.
        
        df.to_sql(
            'customers_2025', 
            engine, 
            if_exists='append', 
            index=False, 
            chunksize=2000, 
            method='multi' 
        )
        
        total_inserted = len(df)

    except Exception as e:
        print(f"\n[ERROR] Import failed: {e}")
        import traceback
        traceback.print_exc()
        return

    elapsed = time.time() - start_time
    print(f"\n  [SUCCESS] Total inserted: {total_inserted:,} rows in {elapsed:.1f}s")

    # 4. Verification
    print("\n[3/4] Final Database Verification")
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM customers_2025")).scalar()
        print(f"  Total records in 'customers_2025': {count:,}")

if __name__ == "__main__":
    import_2025_full()
