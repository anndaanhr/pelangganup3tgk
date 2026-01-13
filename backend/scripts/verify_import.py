"""
Script untuk verifikasi data yang diimport
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import SessionLocal
from models import Customer2024, Customer2025
from services.analysis import AnalysisService

def verify_import():
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("VERIFICATION REPORT - Data Import")
        print("=" * 60)
        
        # Check 2024 data
        print("\n[2024 Data]")
        total_2024 = db.query(Customer2024).count()
        print(f"  Total records: {total_2024}")
        
        records_with_data = 0
        for c in db.query(Customer2024).all():
            months = sum(1 for m in [
                c.dec_2023, c.jan_2024, c.feb_2024, c.mar_2024, c.apr_2024,
                c.may_2024, c.jun_2024, c.jul_2024, c.aug_2024, c.sep_2024,
                c.oct_2024, c.nov_2024, c.dec_2024
            ] if m is not None)
            if months > 0:
                records_with_data += 1
        
        print(f"  Records with monthly data: {records_with_data}/{total_2024}")
        
        # Check 2025 data
        print("\n[2025 Data]")
        total_2025 = db.query(Customer2025).count()
        print(f"  Total records: {total_2025}")
        
        records_with_data_2025 = 0
        for c in db.query(Customer2025).all():
            months = sum(1 for m in [
                c.dec_2024, c.jan_2025, c.feb_2025, c.mar_2025, c.apr_2025,
                c.may_2025, c.jun_2025, c.jul_2025, c.aug_2025, c.sep_2025,
                c.oct_2025, c.nov_2025, c.dec_2025
            ] if m is not None)
            if months > 0:
                records_with_data_2025 += 1
        
        print(f"  Records with monthly data: {records_with_data_2025}/{total_2025}")
        
        # Sample complete record
        print("\n" + "=" * 60)
        print("Sample Complete Record (2024)")
        print("=" * 60)
        sample = db.query(Customer2024).first()
        if sample:
            print(f"IDPEL: {sample.idpel}")
            print(f"Nama: {sample.nama}")
            print(f"Alamat: {sample.alamat[:60] if sample.alamat else 'NULL'}...")
            print(f"TARIF: {sample.tarif}")
            print(f"DAYA: {sample.daya} VA")
            print(f"JENIS: {sample.jenis}")
            print(f"LAYANAN: {sample.layanan}")
            print(f"GARDU: {sample.gardu}")
            print("\nMonthly Consumption:")
            months_data = [
                ('Dec 2023', sample.dec_2023),
                ('Jan 2024', sample.jan_2024),
                ('Feb 2024', sample.feb_2024),
                ('Mar 2024', sample.mar_2024),
                ('Apr 2024', sample.apr_2024),
                ('May 2024', sample.may_2024),
                ('Jun 2024', sample.jun_2024),
                ('Jul 2024', sample.jul_2024),
                ('Aug 2024', sample.aug_2024),
                ('Sep 2024', sample.sep_2024),
                ('Oct 2024', sample.oct_2024),
                ('Nov 2024', sample.nov_2024),
                ('Dec 2024', sample.dec_2024)
            ]
            for month, val in months_data:
                print(f"  {month:12s}: {val if val else 'NULL':>15}")
            
            # Test calculation
            service = AnalysisService(db)
            total = service._calculate_total(sample, 2024)
            print(f"\nTotal Consumption 2024: {total}")
        
        # Check common IDPELs
        print("\n" + "=" * 60)
        print("Common IDPELs (for analysis)")
        print("=" * 60)
        idpel_2024 = {row[0] for row in db.query(Customer2024.idpel).all()}
        idpel_2025 = {row[0] for row in db.query(Customer2025.idpel).all()}
        common = idpel_2024 & idpel_2025
        print(f"  IDPELs in 2024: {len(idpel_2024)}")
        print(f"  IDPELs in 2025: {len(idpel_2025)}")
        print(f"  Common IDPELs: {len(common)}")
        print(f"  New customers (2025 only): {len(idpel_2025 - idpel_2024)}")
        print(f"  Lost customers (2024 only): {len(idpel_2024 - idpel_2025)}")
        
        print("\n" + "=" * 60)
        print("VERIFICATION COMPLETE!")
        print("=" * 60)
        
    finally:
        db.close()

if __name__ == "__main__":
    verify_import()

