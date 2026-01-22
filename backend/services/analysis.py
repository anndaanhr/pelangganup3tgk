"""
Service untuk analisis data pelanggan
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, select
from typing import Optional, List, Dict
from models import Customer2024, Customer2025
from schemas import CustomerAnalysis, MonthlyData, PaginatedResponse, Customer2024Response, Customer2025Response
from decimal import Decimal

import json
import os
from datetime import datetime

CACHE_FILE = "stats_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache_to_disk(key, data):
    cache = load_cache()
    cache[key] = data
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, default=str)

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
    
    # ... (analyze_customer and other methods) ...
    
    # ... (analyze_customer) ...
    
    def _calculate_total(self, customer, year: int) -> Optional[Decimal]:
        """Hitung total konsumsi tahunan"""
        if not customer:
            return None
        
        month_cols = []
        if year == 2024:
            month_cols = ['dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                          'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024']
        else:
            month_cols = ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                          'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025']
        
        total = Decimal(0)
        for col in month_cols:
            val = getattr(customer, col, None)
            if val is not None:
                total += Decimal(str(val))
        
        return total if total > 0 else None

    def get_dashboard_stats(self):
        """Get dashboard overview statistics"""
        # Try Disk Cache First
        cache = load_cache()
        if 'dashboard_stats' in cache:
            print("DISK CACHE HIT: Dashboard Stats")
            # Reconstruct Pydantic model from JSON dict
            from schemas import SummaryStats
            return SummaryStats(**cache['dashboard_stats'])

        print("CALCULATING: Dashboard Stats (This may take a while)...")
        from schemas import SummaryStats
        from sqlalchemy import func
        
        # 1. Total Customers
        total_2024 = self.db.query(Customer2024).count()
        total_2025 = self.db.query(Customer2025).count()
        
        # 2. Customer Migration
        active_customers = self.db.query(func.count(Customer2025.idpel))\
            .join(Customer2024, Customer2025.idpel == Customer2024.idpel)\
            .scalar() or 0
        
        new_customers = total_2025 - active_customers
        lost_customers = total_2024 - active_customers
        
        # 3. Total Consumption
        months_2024 = ['dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                       'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024']
        
        months_2025 = ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                       'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025']

        # TARIFF MAP (Approximate 2024/2025 rates per kWh)
        # Using simplified average for common tariffs if not exact
        TARIFF_MAP = {
            'R1': 1352.00,
            'R1M': 1352.00,
            'R2': 1699.53,
            'R3': 1699.53,
            'B1': 1352.00,
            'B2': 1444.70,
            'B3': 1114.74,
            'I3': 1114.74,
            'P1': 1699.53,
        }
        DEFAULT_TARIFF = 1444.70 # Average fallback

        def calculate_revenue_and_energy(model, months_cols, year):
            total_energy = Decimal(0)
            total_revenue = Decimal(0)
            
            # Efficiently fetch Tariff and Monthly Data in one go
            # This is complex in pure SQL with map, so we'll fetch ID, DAL, Tariff and compute in Python 
            # OR for Dashboard stats which needs aggregate, we might need a simpler approach for performance
            # For now, let's use the fast_table_sum for Energy (already done)
            # And for Revenue, we can approximate by grouping by Tariff
            
            # 1. Total Energy (Already calculated below as total_cons_2024/2025)
            # Reuse existing logic for energy
            
            # 2. Revenue Calculation Strategy:
            # Group by Tarif -> Sum Energy -> Multiply by Tarif Rate
            
            stmt = self.db.query(
                model.tarif,
                *[func.sum(getattr(model, col)) for col in months_cols]
            ).group_by(model.tarif)
            
            results = stmt.all()
            
            for row in results:
                tarif_code = row[0]
                # Sum all months for this tariff group
                kwh_sum = sum((float(val) for val in row[1:] if val is not None))
                
                # Get rate
                rate = TARIFF_MAP.get(str(tarif_code).upper(), DEFAULT_TARIFF)
                
                total_energy += Decimal(kwh_sum)
                total_revenue += Decimal(kwh_sum) * Decimal(rate)
                
            return float(total_energy), float(total_revenue)

        # Calculate for 2024
        energy_2024, revenue_2024 = calculate_revenue_and_energy(Customer2024, months_2024, 2024)
        
        # Calculate for 2025
        energy_2025, revenue_2025 = calculate_revenue_and_energy(Customer2025, months_2025, 2025)

        # Legacy values (keep compatible for a moment, but essentially they are Energy)
        total_cons_2024 = energy_2024
        total_cons_2025 = energy_2025
        
        avg_2024 = total_cons_2024 / total_2024 if total_2024 > 0 else 0
        avg_2025 = total_cons_2025 / total_2025 if total_2025 > 0 else 0
        
        consumption_change = None
        if total_cons_2024 > 0:
            consumption_change = ((total_cons_2025 - total_cons_2024) / total_cons_2024) * 100
        
        result = SummaryStats(
            total_customers_2024=total_2024,
            total_customers_2025=total_2025,
            active_customers=active_customers,
            new_customers=new_customers,
            lost_customers=lost_customers,
            total_consumption_2024=float(total_cons_2024),
            total_consumption_2025=float(total_cons_2025),
            avg_consumption_2024=avg_2024,
            avg_consumption_2025=avg_2025,
            consumption_change_percent=consumption_change,
            # NEW FIELDS
            total_revenue_2024=revenue_2024,
            total_revenue_2025=revenue_2025,
            total_energy_2024=energy_2024,
            total_energy_2025=energy_2025
        )
        
        # Save to Disk Cache (Serialize Pydantic to dict)
        save_cache_to_disk('dashboard_stats', result.model_dump())
        return result
    
    def get_new_customers(self, page: int = 1, page_size: int = 50,
                          tarif: Optional[str] = None, jenis: Optional[str] = None,
                          layanan: Optional[str] = None) -> PaginatedResponse:
        """Get customers present in 2025 but not 2024"""
        try:
            # Efficient way: LEFT JOIN where NULL
            query = self.db.query(Customer2025).outerjoin(
                Customer2024, Customer2025.idpel == Customer2024.idpel
            ).filter(Customer2024.idpel == None)

            if tarif: query = query.filter(Customer2025.tarif == tarif)
            if jenis: query = query.filter(Customer2025.jenis == jenis)
            if layanan: query = query.filter(Customer2025.layanan == layanan)
            
            total = query.count()
            offset = (page - 1) * page_size
            customers = query.offset(offset).limit(page_size).all()
            
            items = []
            for customer in customers:
                total_consumption = self._calculate_total(customer, 2025)
                items.append({
                    'idpel': customer.idpel,
                    'nama': customer.nama,
                    'alamat': customer.alamat,
                    'tarif': customer.tarif,
                    'daya': customer.daya,
                    'jenis': customer.jenis,
                    'layanan': customer.layanan,
                    'gardu': customer.gardu,
                    'total_consumption': float(total_consumption) if total_consumption else None
                })
                
            return PaginatedResponse(
                items=items,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=(total + page_size - 1) // page_size if total > 0 else 0
            )
        except Exception as e:
            print(f"ERROR calculating new customers: {e}")
            raise e

    def get_lost_customers(self, page: int = 1, page_size: int = 50,
                           tarif: Optional[str] = None, jenis: Optional[str] = None,
                           layanan: Optional[str] = None) -> PaginatedResponse:
        """Get customers present in 2024 but not 2025"""
        try:
            # LEFT JOIN 2024 -> 2025 where 2025 is NULL
            query = self.db.query(Customer2024).outerjoin(
                Customer2025, Customer2024.idpel == Customer2025.idpel
            ).filter(Customer2025.idpel == None)

            if tarif: query = query.filter(Customer2024.tarif == tarif)
            if jenis: query = query.filter(Customer2024.jenis == jenis)
            if layanan: query = query.filter(Customer2024.layanan == layanan)
            
            total = query.count()
            offset = (page - 1) * page_size
            customers = query.offset(offset).limit(page_size).all()
            
            items = []
            for customer in customers:
                total_consumption = self._calculate_total(customer, 2024)
                items.append({
                    'idpel': customer.idpel,
                    'nama': customer.nama,
                    'alamat': customer.alamat,
                    'tarif': customer.tarif,
                    'daya': customer.daya,
                    'jenis': customer.jenis,
                    'layanan': customer.layanan,
                    'gardu': customer.gardu,
                    'total_consumption': float(total_consumption) if total_consumption else None
                })
                
            return PaginatedResponse(
                items=items,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=(total + page_size - 1) // page_size if total > 0 else 0
            )
        except Exception as e:
            print(f"ERROR calculating lost customers: {e}")
            raise e

    def get_all_customers(self, year: int, page: int = 1, page_size: int = 50,
                         tarif: Optional[str] = None, jenis: Optional[str] = None,
                         layanan: Optional[str] = None, gardu: Optional[str] = None) -> PaginatedResponse:
        """Get all customers untuk tahun tertentu dengan filter"""
        try:
            if year == 2024:
                query = self.db.query(Customer2024)
            else:
                query = self.db.query(Customer2025)
            
            # Filter
            if tarif:
                query = query.filter(Customer2024.tarif == tarif if year == 2024 else Customer2025.tarif == tarif)
            if jenis:
                query = query.filter(Customer2024.jenis == jenis if year == 2024 else Customer2025.jenis == jenis)
            if layanan:
                query = query.filter(Customer2024.layanan == layanan if year == 2024 else Customer2025.layanan == layanan)
            if gardu:
                query = query.filter(Customer2024.gardu == gardu if year == 2024 else Customer2025.gardu == gardu)
            
            total = query.count()
            offset = (page - 1) * page_size
            customers = query.offset(offset).limit(page_size).all()
            
            items = []
            for customer in customers:
                total_consumption = self._calculate_total(customer, year)
                items.append({
                    'idpel': customer.idpel,
                    'nama': customer.nama,
                    'alamat': customer.alamat,
                    'tarif': customer.tarif,
                    'daya': customer.daya,
                    'jenis': customer.jenis,
                    'layanan': customer.layanan,
                    'gardu': customer.gardu,
                    'total_consumption': float(total_consumption) if total_consumption else None
                })
            
            return PaginatedResponse(
                items=items,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=(total + page_size - 1) // page_size if total > 0 else 0
            )
        except Exception as e:
            import traceback
            error_msg = f"CRASH IN GET_ALL_CUSTOMERS: {str(e)}\n{traceback.format_exc()}"
            print(error_msg)
            with open("CRASH_REPORT.txt", "w") as f:
                f.write(error_msg)
            raise e

    def get_aggregate_trends(self) -> List[MonthlyData]:
        """Get data tren bulanan agregat (Total semua pelanggan)"""
        # Ensure Schema is imported
        from schemas import MonthlyData
        
        # Try Disk Cache First
        cache = load_cache()
        if 'dashboard_trends' in cache:
            # if loaded from json, it's a list of dicts.
            if isinstance(cache['dashboard_trends'], list):
               return [MonthlyData(**item) for item in cache['dashboard_trends']]
            
        print("CALCULATING: Aggregate Trends...")
        from sqlalchemy import func
        
        # Mapping nama kolom
        months_2024_cols = [
            'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
            'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024'
        ]
        
        months_2025_cols = [
            'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
            'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025'
        ]
        
        # Helper to get sum
        def get_sums(model, cols):
            exprs = [func.sum(getattr(model, col)).label(col) for col in cols]
            return self.db.query(*exprs).first()
            
        sums_2024 = get_sums(Customer2024, months_2024_cols)
        sums_2025 = get_sums(Customer2025, months_2025_cols)
        
        trends = []
        
        # Handle None result
        dict_2024 = {col: float(val) if val is not None else 0 for col, val in zip(months_2024_cols, sums_2024)} if sums_2024 else {col: 0 for col in months_2024_cols}
        dict_2025 = {col: float(val) if val is not None else 0 for col, val in zip(months_2025_cols, sums_2025)} if sums_2025 else {col: 0 for col in months_2025_cols}
        
        # Mapping
        mapping = [
            ('Jan', 'jan_2024', 'jan_2025'),
            ('Feb', 'feb_2024', 'feb_2025'),
            ('Mar', 'mar_2024', 'mar_2025'),
            ('Apr', 'apr_2024', 'apr_2025'),
            ('Mei', 'may_2024', 'may_2025'),
            ('Jun', 'jun_2024', 'jun_2025'),
            ('Jul', 'jul_2024', 'jul_2025'),
            ('Agu', 'aug_2024', 'aug_2025'),
            ('Sep', 'sep_2024', 'sep_2025'),
            ('Okt', 'oct_2024', 'oct_2025'),
            ('Nov', 'nov_2024', 'nov_2025'),
            ('Des', 'dec_2024', 'dec_2025'),
        ]
        
        for label, k24, k25 in mapping:
            trends.append(MonthlyData(
                month=label,
                value_2024=dict_2024.get(k24, 0),
                value_2025=dict_2025.get(k25, 0)
            ))
            
        # Serialize list of models
        serialized = [item.model_dump() for item in trends]
        save_cache_to_disk('dashboard_trends', serialized)
        return trends

    def get_distribution_stats(self):
        """Get distribusi data berdasarkan tarif dan layanan (2025)"""
        # Try Disk Cache First
        cache = load_cache()
        if 'distribution_stats' in cache:
             return cache['distribution_stats']

        print("CALCULATING: Distribution Stats...")
        from sqlalchemy import func, desc
        from database import SessionLocal
        
        # 1. Distribusi Tarif
        # Group by Tarif and count
        tarif_dist = self.db.query(
            Customer2025.tarif, 
            func.count(Customer2025.idpel).label('count')
        ).group_by(Customer2025.tarif).order_by(desc('count')).limit(5).all()
        
        total_customers = self.db.query(Customer2025).count()
        
        tarif_data = []
        if total_customers > 0:
            for t, count in tarif_dist:
                if t:
                    percentage = round((count / total_customers) * 100, 1)
                    tarif_data.append({'name': t, 'value': percentage})
        
        # 2. Distribusi Layanan (Prabayar/Pascabayar) & Pendapatan
        # Group by Layanan and sum total consumption
        
        # Helper to sum all month columns for 2025
        def sum_cols(model, cols):
            return sum(func.coalesce(getattr(model, col), 0) for col in cols)
            
        months_2025 = ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                       'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025']
        
        layanan_dist = self.db.query(
            Customer2025.layanan,
            func.sum(sum_cols(Customer2025, months_2025)).label('total_revenue')
        ).group_by(Customer2025.layanan).all()
        
        layanan_data = []
        total_revenue_all = Decimal(0)
        
        for l, rev in layanan_dist:
            if l and rev:
                rev_dec = Decimal(rev)
                layanan_data.append({'label': l, 'value': float(rev_dec)})
                total_revenue_all += rev_dec
                
        # Calculate percentages
        final_layanan = []
        if total_revenue_all > 0:
            for item in layanan_data:
                percentage = round((item['value'] / float(total_revenue_all)) * 100, 1)
                final_layanan.append({
                    'label': item['label'],
                    'value': item['value'],
                    'percentage': percentage
                })
        
        result = {
            'tarif_distribution': tarif_data,
            'layanan_distribution': final_layanan,
            'total_revenue_2025': float(total_revenue_all)
        }
        
        save_cache_to_disk('distribution_stats', result)
        return result

