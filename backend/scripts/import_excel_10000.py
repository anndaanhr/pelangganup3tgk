"""
Script import Excel untuk 10.000 data per tahun
Memastikan ID pelanggan konsisten antar tahun
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sqlalchemy import text
from database import engine
from models import Base
from dotenv import load_dotenv

load_dotenv()

# Mapping kolom bulanan
MONTH_MAP_2024 = {
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

def escape_sql(s):
    """Escape string untuk SQL"""
    if pd.isna(s) or s is None:
        return ''
    return str(s).replace("'", "''")

def get_month_values(row, year):
    """Ambil nilai bulanan dari row"""
    month_map = MONTH_MAP_2024 if year == 2024 else MONTH_MAP_2025
    month_values = {}
    
    for col in row.index:
        col_str = str(col)
        if col_str in month_map:
            val = row[col]
            if pd.notna(val):
                try:
                    month_values[month_map[col_str]] = float(val)
                except (ValueError, TypeError):
                    month_values[month_map[col_str]] = None
            else:
                month_values[month_map[col_str]] = None
        elif isinstance(col, pd.Timestamp):
            col_str_ts = str(col)
            if col_str_ts in month_map:
                val = row[col]
                if pd.notna(val):
                    try:
                        month_values[month_map[col_str_ts]] = float(val)
                    except (ValueError, TypeError):
                        month_values[month_map[col_str_ts]] = None
                else:
                    month_values[month_map[col_str_ts]] = None
    
    return month_values

def import_10000():
    """Import 10.000 data per tahun dengan konsistensi ID"""
    print("=" * 60)
    print("IMPORT DATA - 10.000 DATA PER TAHUN")
    print("=" * 60)
    
    project_root = Path(__file__).resolve().parent.parent.parent
    excel_2024 = project_root / "data" / "JUAL PERPELANGGAN 2024 BL.xlsx"
    excel_2025 = project_root / "data" / "JUAL PERPELANGGAN 2025 BL.xlsx"
    
    # Baca 10.000 baris pertama dari masing-masing file
    print("\n[1/5] Reading Excel files (10.000 rows each)...")
    print("Reading 2024 file...")
    df2024_all = pd.read_excel(excel_2024, nrows=10000, engine='openpyxl')
    print("Reading 2025 file...")
    df2025_all = pd.read_excel(excel_2025, nrows=10000, engine='openpyxl')
    
    # Ambil IDPEL yang valid
    print("\n[2/5] Finding common IDPELs...")
    idpel_2024 = set(df2024_all['IDPEL'].dropna().astype(int))
    idpel_2025 = set(df2025_all['IDPEL'].dropna().astype(int))
    
    # Cari IDPEL yang sama (existing customers)
    common_idpel = idpel_2024 & idpel_2025
    new_idpel = idpel_2025 - idpel_2024  # Ada di 2025 tapi tidak di 2024
    lost_idpel = idpel_2024 - idpel_2025  # Ada di 2024 tapi tidak di 2025
    
    print(f"  IDPELs in 2024: {len(idpel_2024):,}")
    print(f"  IDPELs in 2025: {len(idpel_2025):,}")
    print(f"  Common IDPELs (existing): {len(common_idpel):,}")
    print(f"  New IDPELs (only in 2025): {len(new_idpel):,}")
    print(f"  Lost IDPELs (only in 2024): {len(lost_idpel):,}")
    
    # Strategi: Ambil semua common IDPELs + sample dari new/lost untuk mencapai ~10.000
    target_total = 10000
    common_list = list(common_idpel)
    
    # Jika common kurang dari target, tambahkan dari new/lost
    remaining = target_total - len(common_list)
    if remaining > 0:
        new_sample = list(new_idpel)[:remaining//2] if len(new_idpel) > 0 else []
        lost_sample = list(lost_idpel)[:remaining - len(new_sample)] if len(lost_idpel) > 0 else []
        all_idpel = common_list + new_sample + lost_sample
    else:
        all_idpel = common_list[:target_total]
    
    print(f"\n[3/5] Selected {len(all_idpel):,} IDPELs for import")
    print(f"  - Existing: {len(common_list):,}")
    print(f"  - New: {len(new_sample) if remaining > 0 else 0}")
    print(f"  - Lost: {len(lost_sample) if remaining > 0 else 0}")
    
    # Filter data berdasarkan IDPEL yang dipilih
    df2024 = df2024_all[df2024_all['IDPEL'].astype(int).isin(all_idpel)]
    df2025 = df2025_all[df2025_all['IDPEL'].astype(int).isin(all_idpel)]
    
    print(f"\nFiltered to {len(df2024):,} rows from 2024")
    print(f"Filtered to {len(df2025):,} rows from 2025")
    
    # Create tables
    print("\n[4/5] Creating/updating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Insert dengan raw SQL untuk speed maksimal
    print("\n[5/5] Inserting data (raw SQL - FASTEST)...")
    
    conn = engine.connect()
    trans = conn.begin()
    
    try:
        # Insert 2024
        print("Inserting 2024 data...")
        idpel_list_2024 = set()
        for idx, row in df2024.iterrows():
            try:
                idpel = int(row['IDPEL']) if pd.notna(row['IDPEL']) else None
                if not idpel:
                    continue
                
                month_vals = get_month_values(row, 2024)
                
                # Build kolom dan values - termasuk CATER dan PENYULANG
                base_cols = ['idpel', 'unitup', 'nama', 'alamat', 'tarif', 'daya', 'kddk', 'cater', 'penyulang', 'gardu', 'jenis', 'layanan', 'kd_proses']
                base_vals = [
                    str(idpel),
                    str(int(row['UNITUP'])) if pd.notna(row['UNITUP']) else 'NULL',
                    f"'{escape_sql(row['NAMA'])}'" if pd.notna(row['NAMA']) else 'NULL',
                    f"'{escape_sql(row['ALAMAT'])}'" if pd.notna(row['ALAMAT']) else 'NULL',
                    f"'{escape_sql(row['TARIF'])}'" if pd.notna(row['TARIF']) else 'NULL',
                    str(int(row['DAYA'])) if pd.notna(row['DAYA']) else 'NULL',
                    f"'{escape_sql(row['KDDK'])}'" if pd.notna(row['KDDK']) else 'NULL',
                    f"'{escape_sql(row['CATER'])}'" if 'CATER' in row.index and pd.notna(row['CATER']) else 'NULL',
                    f"'{escape_sql(row['PENYULANG'])}'" if 'PENYULANG' in row.index and pd.notna(row['PENYULANG']) else 'NULL',
                    f"'{escape_sql(row['GARDU'])}'" if pd.notna(row['GARDU']) else 'NULL',
                    f"'{escape_sql(row['JENIS'])}'" if pd.notna(row['JENIS']) else 'NULL',
                    f"'{escape_sql(row['LAYANAN'])}'" if pd.notna(row['LAYANAN']) else 'NULL',
                    f"'{escape_sql(row['KD PROSES'])}'" if pd.notna(row['KD PROSES']) else 'NULL'
                ]
                
                # Tambahkan kolom bulanan
                month_cols_2024 = ['dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                                  'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024']
                month_vals_list = []
                for col in month_cols_2024:
                    if col in month_vals and month_vals[col] is not None:
                        month_vals_list.append(str(month_vals[col]))
                    else:
                        month_vals_list.append('NULL')
                
                all_cols = ', '.join(base_cols + month_cols_2024)
                all_vals = ', '.join(base_vals + month_vals_list)
                
                # Tambahkan MERK KWH untuk 2024
                if 'MERK KWH' in row.index and pd.notna(row['MERK KWH']):
                    all_cols += ', merk_kwh'
                    all_vals += f", '{escape_sql(row['MERK KWH'])}'"
                
                sql = f"INSERT INTO customers_2024 ({all_cols}) VALUES ({all_vals}) ON CONFLICT (idpel) DO UPDATE SET " + \
                      ", ".join([f"{col} = EXCLUDED.{col}" for col in base_cols[1:] + month_cols_2024 + (['merk_kwh'] if 'MERK KWH' in row.index and pd.notna(row['MERK KWH']) else [])]) + ";"
                try:
                    conn.execute(text(sql))
                    idpel_list_2024.add(idpel)
                except Exception as sql_err:
                    # Skip jika duplicate atau error lain, tapi jangan abort transaction
                    if 'duplicate key' not in str(sql_err).lower() and 'InFailedSqlTransaction' not in str(sql_err):
                        print(f"Warning row {idx}: {sql_err}")
                    continue
            except Exception as e:
                # Skip row jika ada error parsing
                if 'InFailedSqlTransaction' not in str(e):
                    print(f"Error parsing row {idx}: {e}")
                continue
        
        # Insert 2025
        print("Inserting 2025 data...")
        idpel_list_2025 = set()
        for idx, row in df2025.iterrows():
            try:
                idpel = int(row['IDPEL']) if pd.notna(row['IDPEL']) else None
                if not idpel:
                    continue
                
                month_vals = get_month_values(row, 2025)
                
                # Build kolom dan values - termasuk CATER dan PENYULANG
                base_cols = ['idpel', 'unitup', 'nama', 'alamat', 'tarif', 'daya', 'kddk', 'cater', 'penyulang', 'gardu', 'jenis', 'layanan', 'kd_proses']
                base_vals = [
                    str(idpel),
                    str(int(row['UNITUP'])) if pd.notna(row['UNITUP']) else 'NULL',
                    f"'{escape_sql(row['NAMA'])}'" if pd.notna(row['NAMA']) else 'NULL',
                    f"'{escape_sql(row['ALAMAT'])}'" if pd.notna(row['ALAMAT']) else 'NULL',
                    f"'{escape_sql(row['TARIF'])}'" if pd.notna(row['TARIF']) else 'NULL',
                    str(int(row['DAYA'])) if pd.notna(row['DAYA']) else 'NULL',
                    f"'{escape_sql(row['KDDK'])}'" if pd.notna(row['KDDK']) else 'NULL',
                    f"'{escape_sql(row['CATER'])}'" if 'CATER' in row.index and pd.notna(row['CATER']) else 'NULL',
                    f"'{escape_sql(row['PENYULANG'])}'" if 'PENYULANG' in row.index and pd.notna(row['PENYULANG']) else 'NULL',
                    f"'{escape_sql(row['GARDU'])}'" if pd.notna(row['GARDU']) else 'NULL',
                    f"'{escape_sql(row['JENIS'])}'" if pd.notna(row['JENIS']) else 'NULL',
                    f"'{escape_sql(row['LAYANAN'])}'" if pd.notna(row['LAYANAN']) else 'NULL',
                    f"'{escape_sql(row['KD PROSES'])}'" if pd.notna(row['KD PROSES']) else 'NULL'
                ]
                
                # Tambahkan kolom bulanan
                month_cols_2025 = ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                                  'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025']
                month_vals_list = []
                for col in month_cols_2025:
                    if col in month_vals and month_vals[col] is not None:
                        month_vals_list.append(str(month_vals[col]))
                    else:
                        month_vals_list.append('NULL')
                
                all_cols = ', '.join(base_cols + month_cols_2025)
                all_vals = ', '.join(base_vals + month_vals_list)
                
                sql = f"INSERT INTO customers_2025 ({all_cols}) VALUES ({all_vals}) ON CONFLICT (idpel) DO UPDATE SET " + \
                      ", ".join([f"{col} = EXCLUDED.{col}" for col in base_cols[1:] + month_cols_2025]) + ";"
                try:
                    conn.execute(text(sql))
                    idpel_list_2025.add(idpel)
                except Exception as sql_err:
                    # Skip jika duplicate atau error lain, tapi jangan abort transaction
                    if 'duplicate key' not in str(sql_err).lower() and 'InFailedSqlTransaction' not in str(sql_err):
                        print(f"Warning row {idx}: {sql_err}")
                    continue
            except Exception as e:
                # Skip row jika ada error parsing
                if 'InFailedSqlTransaction' not in str(e):
                    print(f"Error parsing row {idx}: {e}")
                continue
        
        print(f"\n[SUCCESS] Inserted {len(idpel_list_2024):,} records for 2024")
        print(f"[SUCCESS] Inserted {len(idpel_list_2025):,} records for 2025")
        
        # Verifikasi konsistensi
        print("\n" + "=" * 60)
        print("VERIFICATION")
        print("=" * 60)
        common_imported = idpel_list_2024 & idpel_list_2025
        new_imported = idpel_list_2025 - idpel_list_2024
        lost_imported = idpel_list_2024 - idpel_list_2025
        
        print(f"Existing customers (in both years): {len(common_imported):,}")
        print(f"New customers (only in 2025): {len(new_imported):,}")
        print(f"Lost customers (only in 2024): {len(lost_imported):,}")
        
        trans.commit()
        print("\n" + "=" * 60)
        print("[SUCCESS] IMPORT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Ready to use! Open http://localhost:3000")
        
    except Exception as e:
        trans.rollback()
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    import_10000()

