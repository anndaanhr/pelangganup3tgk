from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from models import Customer2024, Customer2025
import json
import os

CACHE_FILE = "ulp_stats_cache.json"

ULP_MAPPING = {
    17100: "Karang",
    17110: "Natar",
    17120: "Way Halim",
    17130: "Kalianda",
    17131: "Sidomulyo",
    17150: "Sutami",
    17180: "Teluk Betung"
}

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

class UlpAnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def _get_monthly_cols(self, year):
        if year == 2024:
            return ['dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                    'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024']
        else:
            return ['dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                    'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025']

    def get_overview(self):
        """Get aggregate stats per ULP"""
        cache = load_cache()
        if 'ulp_overview' in cache:
            return cache['ulp_overview']
            
        print("CALCULATING: ULP Overview...")
        
        # Helper to sum cols
        def sum_cols_expr(model, cols):
            return sum(func.coalesce(getattr(model, col), 0) for col in cols)

        month_cols_2024 = self._get_monthly_cols(2024)
        month_cols_2025 = self._get_monthly_cols(2025)

        # Query 2024
        results_2024 = self.db.query(
            Customer2024.unitup,
            func.count(Customer2024.idpel).label('count'),
            func.sum(sum_cols_expr(Customer2024, month_cols_2024)).label('total_kwh')
        ).filter(Customer2024.unitup.in_(ULP_MAPPING.keys())).group_by(Customer2024.unitup).all()

        # Query 2025
        results_2025 = self.db.query(
            Customer2025.unitup,
            func.count(Customer2025.idpel).label('count'),
            func.sum(sum_cols_expr(Customer2025, month_cols_2025)).label('total_kwh')
        ).filter(Customer2025.unitup.in_(ULP_MAPPING.keys())).group_by(Customer2025.unitup).all()

        data_2024 = {row.unitup: {'count': row.count, 'kwh': float(row.total_kwh or 0)} for row in results_2024}
        data_2025 = {row.unitup: {'count': row.count, 'kwh': float(row.total_kwh or 0)} for row in results_2025}

        result = []
        for code, name in ULP_MAPPING.items():
            d24 = data_2024.get(code, {'count': 0, 'kwh': 0})
            d25 = data_2025.get(code, {'count': 0, 'kwh': 0})
            
            kwh_growth = ((d25['kwh'] - d24['kwh']) / d24['kwh'] * 100) if d24['kwh'] > 0 else 0
            cust_growth = ((d25['count'] - d24['count']) / d24['count'] * 100) if d24['count'] > 0 else 0
            
            result.append({
                'unitup': code,
                'name': name,
                'customer_count_2025': d25['count'],
                'customer_count_2024': d24['count'],
                'total_kwh_2025': d25['kwh'],
                'total_kwh_2024': d24['kwh'],
                'kwh_growth_percent': round(kwh_growth, 2),
                'customer_growth_percent': round(cust_growth, 2)
            })

        # Sort by total kWh 2025 desc
        result.sort(key=lambda x: x['total_kwh_2025'], reverse=True)
        
        save_cache_to_disk('ulp_overview', result)
        return result
