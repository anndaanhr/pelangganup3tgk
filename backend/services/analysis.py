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

    def get_dashboard_stats(self, unitup: Optional[int] = None):
        """Get dashboard overview statistics"""
        # Try Disk Cache First using composite key
        cache_key = f'dashboard_stats_{unitup}' if unitup else 'dashboard_stats'
        cache = load_cache()
        if cache_key in cache:
            # print("DISK CACHE HIT: Dashboard Stats")
            # Reconstruct Pydantic model from JSON dict
            from schemas import SummaryStats
            return SummaryStats(**cache[cache_key])
            
        return self._calculate_dashboard_stats(unitup, cache_key)
    
    def _calculate_dashboard_stats(self, unitup: Optional[int], cache_key: str):

        if unitup:
            print(f"CALCULATING: Dashboard Stats for ULP {unitup}...")
        else:
            print("CALCULATING: Dashboard Stats (This may take a while)...")
            
        from schemas import SummaryStats
        from sqlalchemy import func
        
        # 1. Total Customers
        q24 = self.db.query(Customer2024)
        q25 = self.db.query(Customer2025)
        
        if unitup:
            q24 = q24.filter(Customer2024.unitup == unitup)
            q25 = q25.filter(Customer2025.unitup == unitup)
            
        total_2024 = q24.count()
        total_2025 = q25.count()
        
        # 2. Customer Migration
        # 2. Customer Migration
        active_query = self.db.query(func.count(Customer2025.idpel))\
            .join(Customer2024, Customer2025.idpel == Customer2024.idpel)
            
        if unitup:
            # Ensure both satisfy unitup
            active_query = active_query.filter(
                Customer2025.unitup == unitup,
                Customer2024.unitup == unitup
            )
            
        active_customers = active_query.scalar() or 0
        
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
            
            query = self.db.query(
                model.tarif,
                *[func.sum(getattr(model, col)) for col in months_cols]
            )
            
            if unitup:
                query = query.filter(model.unitup == unitup)
                
            stmt = query.group_by(model.tarif)
            
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
        
        # Save to Disk Cache (Serialize Pydantic to dict)
        save_cache_to_disk(cache_key, result.model_dump())
        return result
    
    def get_new_customers(self, page: int = 1, page_size: int = 50,
                          tarif: Optional[str] = None, jenis: Optional[str] = None,
                          layanan: Optional[str] = None, gardu: Optional[str] = None,
                          unitup: Optional[str] = None,
                          daya: Optional[int] = None) -> PaginatedResponse:
        """Get customers present in 2025 but not 2024"""
        try:
            # Efficient way: LEFT JOIN where NULL
            query = self.db.query(Customer2025).outerjoin(
                Customer2024, Customer2025.idpel == Customer2024.idpel
            ).filter(Customer2024.idpel == None)

            if tarif: query = query.filter(Customer2025.tarif == tarif)
            if jenis: query = query.filter(Customer2025.jenis == jenis)
            if layanan: query = query.filter(Customer2025.layanan == layanan)
            if gardu: query = query.filter(Customer2025.gardu == gardu)
            if unitup: query = query.filter(Customer2025.unitup == unitup)
            if daya is not None: query = query.filter(Customer2025.daya == daya)
            
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
                           layanan: Optional[str] = None, gardu: Optional[str] = None,
                           unitup: Optional[str] = None,
                           daya: Optional[int] = None) -> PaginatedResponse:
        """Get customers present in 2024 but not 2025"""
        try:
            # LEFT JOIN 2024 -> 2025 where 2025 is NULL
            query = self.db.query(Customer2024).outerjoin(
                Customer2025, Customer2024.idpel == Customer2025.idpel
            ).filter(Customer2025.idpel == None)

            if tarif: query = query.filter(Customer2024.tarif == tarif)
            if jenis: query = query.filter(Customer2024.jenis == jenis)
            if layanan: query = query.filter(Customer2024.layanan == layanan)
            if gardu: query = query.filter(Customer2024.gardu == gardu)
            if unitup: query = query.filter(Customer2024.unitup == unitup)
            if daya is not None: query = query.filter(Customer2024.daya == daya)
            
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
                         layanan: Optional[str] = None, gardu: Optional[str] = None,
                         unitup: Optional[str] = None,
                         daya: Optional[int] = None) -> PaginatedResponse:
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
            if unitup:
                query = query.filter(Customer2024.unitup == unitup if year == 2024 else Customer2025.unitup == unitup)
            if daya is not None:
                query = query.filter(Customer2024.daya == daya if year == 2024 else Customer2025.daya == daya)
            
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

    def get_monthly_trends(self, idpel: int) -> List[MonthlyData]:
        """Get monthly consumption trends for one customer (untuk halaman detail)."""
        from schemas import MonthlyData
        customer_2024 = self.db.query(Customer2024).filter(Customer2024.idpel == idpel).first()
        customer_2025 = self.db.query(Customer2025).filter(Customer2025.idpel == idpel).first()
        if not customer_2024 and not customer_2025:
            return []
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
        result = []
        for label, col_24, col_25 in mapping:
            v24 = getattr(customer_2024, col_24, None) if customer_2024 else None
            v25 = getattr(customer_2025, col_25, None) if customer_2025 else None
            result.append(MonthlyData(
                month=label,
                value_2024=float(v24) if v24 is not None else None,
                value_2025=float(v25) if v25 is not None else None,
            ))
        return result

    def get_aggregate_trends(self, unitup: Optional[int] = None) -> List[MonthlyData]:
        """Get data tren bulanan agregat (Total semua pelanggan)"""
        # Ensure Schema is imported
        from schemas import MonthlyData
        
        # Try Disk Cache First
        cache_key = f'dashboard_trends_{unitup}' if unitup else 'dashboard_trends'
        cache = load_cache()
        if cache_key in cache:
            # if loaded from json, it's a list of dicts.
            if isinstance(cache[cache_key], list):
               return [MonthlyData(**item) for item in cache[cache_key]]
            
        return self._calculate_aggregate_trends(unitup, cache_key)

    def _calculate_aggregate_trends(self, unitup: Optional[int], cache_key: str):
        if unitup:
            print(f"CALCULATING: Aggregate Trends for ULP {unitup}...")
        else:
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
            query = self.db.query(*[func.sum(getattr(model, col)).label(col) for col in cols])
            if unitup:
                query = query.filter(model.unitup == unitup)
            return query.first()
            
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
        # Serialize list of models
        serialized = [item.model_dump() for item in trends]
        save_cache_to_disk(cache_key, serialized)
        return trends

    def get_distribution_stats(self, unitup: Optional[int] = None):
        """Get distribusi data berdasarkan tarif dan layanan (2025)"""
        # Try Disk Cache First
        cache_key = f'distribution_stats_{unitup}' if unitup else 'distribution_stats'
        cache = load_cache()
        if cache_key in cache:
             return cache[cache_key]

        return self._calculate_distribution_stats(unitup, cache_key)

    def _calculate_distribution_stats(self, unitup: Optional[int], cache_key: str):
        print(f"CALCULATING: Distribution Stats (ULP={unitup})...")
        from sqlalchemy import func, desc
        from database import SessionLocal
        
        # 1. Distribusi Tarif
        # Group by Tarif and count
        # 1. Distribusi Tarif
        # Group by Tarif and count
        q_tarif = self.db.query(
            Customer2025.tarif, 
            func.count(Customer2025.idpel).label('count')
        )
        if unitup:
            q_tarif = q_tarif.filter(Customer2025.unitup == unitup)
            
        tarif_dist = q_tarif.group_by(Customer2025.tarif).order_by(desc('count')).limit(5).all()
        
        q_total = self.db.query(Customer2025)
        if unitup:
            q_total = q_total.filter(Customer2025.unitup == unitup)
        total_customers = q_total.count()
        
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
        
        q_layanan = self.db.query(
            Customer2025.layanan,
            func.sum(sum_cols(Customer2025, months_2025)).label('total_revenue')
        )
        if unitup:
            q_layanan = q_layanan.filter(Customer2025.unitup == unitup)
            
        layanan_dist = q_layanan.group_by(Customer2025.layanan).all()
        
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
        
        save_cache_to_disk(cache_key, result)
        return result


    def get_usage_distribution_comparison(self, unitup: Optional[int] = None):
        """
        Get aggregated usage (kWh) by Tarif, Jenis, and Layanan for 2024 vs 2025.
        """
        cache_key = f'usage_comparison_{unitup}' if unitup else 'usage_comparison'
        cache = load_cache()
        if cache_key in cache:
             return cache[cache_key]

        return self._calculate_usage_comparison(unitup, cache_key)

    def _calculate_usage_comparison(self, unitup: Optional[int], cache_key: str):
        print(f"CALCULATING: Usage Comparison Stats (ULP={unitup})...")
        from sqlalchemy import func
        
        month_cols_2024 = ['dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                           'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024']
        month_cols_2025 = ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                           'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025']

        def sum_cols_expr(model, cols):
            return sum(func.coalesce(getattr(model, col), 0) for col in cols)

        def aggregate_by(model, group_col, month_cols):
            query = self.db.query(
                getattr(model, group_col),
                func.sum(sum_cols_expr(model, month_cols))
            )
            if unitup:
                query = query.filter(model.unitup == unitup)
                
            results = query.group_by(getattr(model, group_col)).all()
            return {row[0]: float(row[1] or 0) for row in results if row[0]}

        # Aggregate 2024
        tarif_2024 = aggregate_by(Customer2024, 'tarif', month_cols_2024)
        jenis_2024 = aggregate_by(Customer2024, 'jenis', month_cols_2024)
        layanan_2024 = aggregate_by(Customer2024, 'layanan', month_cols_2024)

        # Aggregate 2025
        tarif_2025 = aggregate_by(Customer2025, 'tarif', month_cols_2025)
        jenis_2025 = aggregate_by(Customer2025, 'jenis', month_cols_2025)
        layanan_2025 = aggregate_by(Customer2025, 'layanan', month_cols_2025)

        def merge_data(data_2024, data_2025):
            keys = set(data_2024.keys()) | set(data_2025.keys())
            result = []
            for k in keys:
                # Filter out null/empty keys
                if not k: continue
                val24 = data_2024.get(k, 0)
                val25 = data_2025.get(k, 0)
                # Only include significant data
                if val24 > 0 or val25 > 0:
                    result.append({
                        'label': k,
                        'value_2024': val24,
                        'value_2025': val25
                    })
            # Sort by 2025 value desc
            return sorted(result, key=lambda x: x['value_2025'], reverse=True)

        result = {
            'tarif': merge_data(tarif_2024, tarif_2025),
            'jenis': merge_data(jenis_2024, jenis_2025),
            'layanan': merge_data(layanan_2024, layanan_2025)
        }

        save_cache_to_disk(cache_key, result)
        return result
