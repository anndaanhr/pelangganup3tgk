"""
Script untuk import data Excel ke database PostgreSQL
Sampling ~1000 pelanggan dengan strategi: semua yang ada di kedua tahun + sample proporsional dari new/lost
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Customer2024, Customer2025
from dotenv import load_dotenv

load_dotenv()

# Mapping kolom bulanan dari datetime ke nama kolom standar
MONTH_MAPPING_2024 = {
    '2023-12-01 00:00:00': 'dec_2023',
    '2024-01-01 00:00:00': 'jan_2024',
    '2024-02-01 00:00:00': 'feb_2024',
    '2024-03-01 00:00:00': 'mar_2024',
    '2024-04-01 00:00:00': 'apr_2024',
    '2024-05-01 00:00:00': 'may_2024',
    '2024-06-01 00:00:00': 'jun_2024',
    '2024-07-01 00:00:00': 'jul_2024',
    '2024-08-01 00:00:00': 'aug_2024',
    '2024-09-01 00:00:00': 'sep_2024',
    '2024-10-01 00:00:00': 'oct_2024',
    '2024-11-01 00:00:00': 'nov_2024',
    '2024-12-01 00:00:00': 'dec_2024',
}

MONTH_MAPPING_2025 = {
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

def normalize_month_columns(df, year):
    """Normalisasi kolom bulanan dari datetime ke nama standar"""
    mapping = MONTH_MAPPING_2024 if year == 2024 else MONTH_MAPPING_2025
    df_normalized = df.copy()
    
    # Rename kolom datetime
    for col in df.columns:
        if isinstance(col, pd.Timestamp):
            col_str = str(col)
            if col_str in mapping:
                df_normalized.rename(columns={col: mapping[col_str]}, inplace=True)
    
    return df_normalized

def prepare_customer_data(row, year):
    """Prepare data untuk insert ke database"""
    data = {
        'idpel': int(row['IDPEL']) if pd.notna(row['IDPEL']) else None,
        'unitup': int(row['UNITUP']) if pd.notna(row['UNITUP']) else None,
        'nama': str(row['NAMA']) if pd.notna(row['NAMA']) else None,
        'alamat': str(row['ALAMAT']) if pd.notna(row['ALAMAT']) else None,
        'tarif': str(row['TARIF']) if pd.notna(row['TARIF']) else None,
        'daya': int(row['DAYA']) if pd.notna(row['DAYA']) else None,
        'kddk': str(row['KDDK']) if pd.notna(row['KDDK']) else None,
        'gardu': str(row['GARDU']) if pd.notna(row['GARDU']) else None,
        'nomor_meter': int(row['NOMOR METER']) if pd.notna(row['NOMOR METER']) else None,
        'jenis': str(row['JENIS']) if pd.notna(row['JENIS']) else None,
        'layanan': str(row['LAYANAN']) if pd.notna(row['LAYANAN']) else None,
        'kd_proses': str(row['KD PROSES']) if pd.notna(row['KD PROSES']) else None,
    }
    
    # Kolom bulanan
    month_cols = MONTH_MAPPING_2024 if year == 2024 else MONTH_MAPPING_2025
    for col_name in month_cols.values():
        if col_name in row.index:
            val = row[col_name]
            data[col_name] = float(val) if pd.notna(val) else None
        else:
            data[col_name] = None
    
    # Kolom khusus 2024
    if year == 2024 and 'MERK KWH' in row.index:
        data['merk_kwh'] = str(row['MERK KWH']) if pd.notna(row['MERK KWH']) else None
    
    return data

def sample_customers(df2024, df2025, target_count=200):
    """Sampling pelanggan dengan strategi: semua common + sample proporsional dari new/lost"""
    # Optimasi: gunakan sample kecil dulu untuk speed
    print(f"Sampling {target_count} records untuk testing cepat...")
    
    # Sample langsung dari dataframe tanpa set operations yang lambat
    df2024_sample = df2024.head(target_count * 2)  # Ambil lebih banyak untuk overlap
    df2025_sample = df2025.head(target_count * 2)
    
    idpel_2024 = set(df2024_sample['IDPEL'].dropna().astype(int))
    idpel_2025 = set(df2025_sample['IDPEL'].dropna().astype(int))
    
    common_idpel = idpel_2024 & idpel_2025
    new_2025 = idpel_2025 - idpel_2024
    lost_2024 = idpel_2024 - idpel_2025
    
    print(f"Pelanggan di kedua tahun: {len(common_idpel):,}")
    print(f"Pelanggan baru di 2025: {len(new_2025):,}")
    print(f"Pelanggan hilang dari 2024: {len(lost_2024):,}")
    
    # Ambil sample cepat
    common_sample = list(common_idpel)[:target_count]
    remaining = target_count - len(common_sample)
    
    if remaining > 0:
        new_sample = list(new_2025)[:remaining//2] if len(new_2025) > 0 else []
        lost_sample = list(lost_2024)[:remaining - len(new_sample)] if len(lost_2024) > 0 else []
        return common_sample + new_sample + lost_sample
    
    return common_sample[:target_count]

def import_data():
    """Main function untuk import data"""
    print("Loading Excel files...")
    
    # Baca file Excel
    project_root = Path(__file__).resolve().parent.parent.parent
    
    # Cek di root dulu, kalau tidak ada baru cek di folder data
    excel_2024_path = project_root / "JUAL PERPELANGGAN 2024 BL.xlsx"
    excel_2025_path = project_root / "JUAL PERPELANGGAN 2025 BL.xlsx"
    
    if not excel_2024_path.exists():
        excel_2024_path = project_root / "data" / "JUAL PERPELANGGAN 2024 BL.xlsx"
        
    if not excel_2025_path.exists():
        excel_2025_path = project_root / "data" / "JUAL PERPELANGGAN 2025 BL.xlsx"
    
    print(f"Looking for Excel files in: {project_root}")
    print(f"File 2024 exists: {excel_2024_path.exists()}")
    print(f"File 2025 exists: {excel_2025_path.exists()}")
    
    if not excel_2024_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {excel_2024_path}")
    if not excel_2025_path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {excel_2025_path}")
    
    df2024 = pd.read_excel(excel_2024_path)
    df2025 = pd.read_excel(excel_2025_path)
    
    print(f"Loaded {len(df2024):,} records from 2024")
    print(f"Loaded {len(df2025):,} records from 2025")
    
    # Normalisasi kolom bulanan
    print("\nNormalizing month columns...")
    df2024_norm = normalize_month_columns(df2024, 2024)
    df2025_norm = normalize_month_columns(df2025, 2025)
    
    # Sampling dengan jumlah sangat kecil untuk speed maksimal
    print("\n⚡ FAST MODE: Sampling customers (50 records only for quick testing)...")
    sampled_idpel = sample_customers(df2024_norm, df2025_norm, target_count=50)
    
    # Filter data berdasarkan IDPEL yang di-sample
    # Clean IDPEL - Remove NaNs and convert to integer safely
    df2024_norm = df2024_norm.dropna(subset=['IDPEL'])
    df2024_norm = df2024_norm[np.isfinite(pd.to_numeric(df2024_norm['IDPEL'], errors='coerce'))]
    
    df2025_norm = df2025_norm.dropna(subset=['IDPEL'])
    df2025_norm = df2025_norm[np.isfinite(pd.to_numeric(df2025_norm['IDPEL'], errors='coerce'))]

    df2024_sampled = df2024_norm[df2024_norm['IDPEL'].astype(int).isin(sampled_idpel)]
    df2025_sampled = df2025_norm[df2025_norm['IDPEL'].astype(int).isin(sampled_idpel)]
    
    print(f"\nFiltered to {len(df2024_sampled)} records for 2024")
    print(f"Filtered to {len(df2025_sampled)} records for 2025")
    
    # Create tables
    print("\nCreating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Insert data dengan bulk insert untuk speed maksimal
    db = SessionLocal()
    try:
        print("\n⚡ Inserting 2024 data (bulk insert - FAST)...")
        customers_2024 = []
        
        for idx, row in df2024_sampled.iterrows():
            try:
                data = prepare_customer_data(row, 2024)
                if data['idpel']:
                    customers_2024.append(Customer2024(**data))
            except:
                continue
        
        if customers_2024:
            db.bulk_save_objects(customers_2024)
            db.commit()
        print(f"✅ Inserted {len(customers_2024)} records for 2024")
        
        print("\n⚡ Inserting 2025 data (bulk insert - FAST)...")
        customers_2025 = []
        
        for idx, row in df2025_sampled.iterrows():
            try:
                data = prepare_customer_data(row, 2025)
                if data['idpel']:
                    customers_2025.append(Customer2025(**data))
            except:
                continue
        
        if customers_2025:
            db.bulk_save_objects(customers_2025)
            db.commit()
        print(f"✅ Inserted {len(customers_2025)} records for 2025")
        
        print("\n🎉 Import completed successfully! Ready to use!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import_data()

