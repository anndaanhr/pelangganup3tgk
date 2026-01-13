import pandas as pd
import numpy as np

# Baca data
import sys
from pathlib import Path

# Get project root from this script path (scripts/analyze_data.py -> ..)
project_root = Path(__file__).resolve().parent.parent
data_dir = project_root / "data"

print("Loading data...")
df2024 = pd.read_excel(data_dir / 'JUAL PERPELANGGAN 2024 BL.xlsx')
df2025 = pd.read_excel(data_dir / 'JUAL PERPELANGGAN 2025 BL.xlsx')

print("\n=== STATISTIK DATA ===")
print(f"Total records 2024: {len(df2024):,}")
print(f"Total records 2025: {len(df2025):,}")
print(f"\nUnique IDPEL 2024: {df2024['IDPEL'].nunique():,}")
print(f"Unique IDPEL 2025: {df2025['IDPEL'].nunique():,}")

# Cek kolom yang berbeda
print(f"\nKolom unik di 2024: {set(df2024.columns) - set(df2025.columns)}")
print(f"Kolom unik di 2025: {set(df2025.columns) - set(df2024.columns)}")

# Analisis kolom kategorikal
print("\n=== KOLOM KATEGORIKAL 2024 ===")
print("\nTARIF values:")
print(df2024['TARIF'].value_counts().head(10))
print("\nJENIS values:")
print(df2024['JENIS'].value_counts())
print("\nLAYANAN values:")
print(df2024['LAYANAN'].value_counts())
print("\nKD PROSES values:")
print(df2024['KD PROSES'].value_counts())

# Analisis kolom bulanan
month_cols_2024 = [c for c in df2024.columns if isinstance(c, pd.Timestamp)]
month_cols_2025 = [c for c in df2025.columns if isinstance(c, pd.Timestamp)]

print("\n=== KOLOM BULANAN ===")
print(f"Bulan 2024: {[str(c)[:7] for c in month_cols_2024]}")
print(f"Bulan 2025: {[str(c)[:7] for c in month_cols_2025]}")

# Sample perhitungan
print("\n=== SAMPLE PERHITUNGAN ===")
sample_2024 = df2024.iloc[0]
print(f"IDPEL: {sample_2024['IDPEL']}")
print(f"Nama: {sample_2024['NAMA']}")
print(f"Tarif: {sample_2024['TARIF']}")
print(f"Daya: {sample_2024['DAYA']}")
monthly_2024 = [sample_2024[c] for c in month_cols_2024 if isinstance(c, pd.Timestamp)]
total_2024 = sum([x for x in monthly_2024 if pd.notna(x)])
print(f"Data bulanan 2024: {monthly_2024}")
print(f"Total tahunan 2024: {total_2024:,.0f}")

# Cek pelanggan yang ada di kedua tahun
common_idpel = set(df2024['IDPEL']) & set(df2025['IDPEL'])
new_2025 = set(df2025['IDPEL']) - set(df2024['IDPEL'])
lost_2024 = set(df2024['IDPEL']) - set(df2025['IDPEL'])

print("\n=== PERBANDINGAN PELANGGAN ===")
print(f"Pelanggan di kedua tahun: {len(common_idpel):,}")
print(f"Pelanggan baru di 2025: {len(new_2025):,}")
print(f"Pelanggan hilang dari 2024: {len(lost_2024):,}")

# Analisis kolom JN
print("\n=== KOLOM JN (Jenis Nota?) ===")
jn_cols = [c for c in df2024.columns if 'JN' in str(c)]
for col in jn_cols:
    non_null = df2024[col].notna().sum()
    if non_null > 0:
        print(f"{col}: {non_null} non-null values")
        print(f"  Sample values: {df2024[col].dropna().head(5).tolist()}")

# Cek struktur GARDU dan PENYULANG
print("\n=== STRUKTUR JARINGAN ===")
print(f"Unique GARDU 2024: {df2024['GARDU'].nunique():,}")
print(f"Unique PENYULANG 2024: {df2024['PENYULANG'].notna().sum():,} non-null")
print(f"Unique CATER 2024: {df2024['CATER'].notna().sum():,} non-null")

