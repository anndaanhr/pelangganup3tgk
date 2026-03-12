from sqlalchemy.orm import Session
from sqlalchemy import func, desc, text
from models import Customer2025, Customer2024
from typing import List, Dict, Any

# In-memory simple cache for high variance
_MEMORY_CACHE = {}
_CACHE_TTL_SECONDS = 300  # 5 minutes

class AdvancedAnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def get_pareto_analysis(self, limit: int = 100, unitup: int = None) -> List[Dict[str, Any]]:
        """
        Get Top N customers by total consumption in 2025.
        Returns list of dict with idpel, nama, total_kwh, contribution_percent.
        """
        # Calculate total consumption per customer
        # Note: We sum individual months for accuracy, or use a pre-calculated logic if available.
        # Assuming we need to sum columns dynamically or use a simpler approximation if fields don't exist
        # Based on models.py, we have month columns. Let's sum them up.

        # Helper to sum columns handling nulls
        total_kwh_expr = (
            func.coalesce(Customer2025.jan_2025, 0) + func.coalesce(Customer2025.feb_2025, 0) +
            func.coalesce(Customer2025.mar_2025, 0) + func.coalesce(Customer2025.apr_2025, 0) +
            func.coalesce(Customer2025.may_2025, 0) + func.coalesce(Customer2025.jun_2025, 0) +
            func.coalesce(Customer2025.jul_2025, 0) + func.coalesce(Customer2025.aug_2025, 0) +
            func.coalesce(Customer2025.sep_2025, 0) + func.coalesce(Customer2025.oct_2025, 0) +
            func.coalesce(Customer2025.nov_2025, 0) + func.coalesce(Customer2025.dec_2025, 0)
        )

        base_query = self.db.query(
            Customer2025.idpel,
            Customer2025.nama,
            Customer2025.tarif,
            Customer2025.daya,
            Customer2025.gardu,
            total_kwh_expr.label("total_kwh")
        )

        if unitup:
            base_query = base_query.filter(Customer2025.unitup == unitup)

        query = (
            base_query
            .order_by(total_kwh_expr.desc())
            .limit(limit)
        )
        
        results = query.all()
        
        # Calculate global total for percentage
        
        # Calculate global total for percentage (filtered by unitup if present)
        total_query = self.db.query(func.sum(total_kwh_expr))
        if unitup:
            total_query = total_query.filter(Customer2025.unitup == unitup)
            
        global_total = float(total_query.scalar() or 1)
        
        data = []
        cumulative_percent = 0
        for row in results:
            kwh = float(row.total_kwh or 0)
            percent = (kwh / global_total) * 100
            cumulative_percent += percent
            
            data.append({
                "idpel": row.idpel,
                "nama": row.nama,
                "tarif": row.tarif,
                "daya": row.daya,
                "gardu": row.gardu,
                "total_kwh": kwh,
                "percentage": round(percent, 4),
                "cumulative_percentage": round(cumulative_percent, 4)
            })
            
        return data

    def get_anomalies_zero_usage(self, page: int = 1, limit: int = 50, unitup: int = None) -> Dict[str, Any]:
        """
        Detect customers with 0 usage for last 3 months (Oct, Nov, Dec 2025).
        Optimized with direct SQL pagination (Limit/Offset).
        """
        # Base query for zero usage
        query = (
            self.db.query(Customer2025)
            .filter(
                (func.coalesce(Customer2025.oct_2025, 0) == 0) &
                (func.coalesce(Customer2025.nov_2025, 0) == 0) &
                (func.coalesce(Customer2025.dec_2025, 0) == 0)
            )
        )
        
        if unitup:
            query = query.filter(Customer2025.unitup == unitup)
        
        # Count total first (efficient count)
        total_items = query.count()
        total_pages = (total_items + limit - 1) // limit if total_items > 0 else 1
        
        # Ensure page is within bounds
        if page < 1: page = 1
        if page > total_pages: page = total_pages

        offset = (page - 1) * limit
        
        # Fetch only current page
        results = query.offset(offset).limit(limit).all()
        
        paginated_data = [
            {
                "idpel": c.idpel,
                "nama": c.nama,
                "alamat": c.alamat,
                "info": "0 kWh (Okt-Des 2025)"
            }
            for c in results
        ]

        return {
            "data": paginated_data,
            "total": total_items,
            "page": page,
            "pages": total_pages
        }

    def get_anomalies_high_variance(self, page: int = 1, limit: int = 50, unitup: int = None, min_pct: int = None, max_pct: int = None) -> Dict[str, Any]:
        """
        Detect customers with high fluctuation in monthly usage for 2025.
        Optimized: Fetches only minimal required columns. Use direct DB filtering where possible.
        Uses Global In-Memory Cache.
        """
        import time
        import traceback

        try:
            # Cache Key logic
            cache_key = f"high_variance_{unitup if unitup else 'all'}_{min_pct}_{max_pct}"
            current_time = time.time()
            
            # Check Cache
            cached = _MEMORY_CACHE.get(cache_key)
            if cached and (current_time - cached['timestamp'] < _CACHE_TTL_SECONDS):
                return {
                    "data": cached['data'][(page - 1) * limit : page * limit],
                    "total": len(cached['data']),
                    "page": page,
                    "pages": (len(cached['data']) + limit - 1) // limit if cached['data'] else 1
                }

            month_cols = [
                'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025'
            ]

            # Optimization 1: Use specific columns instead of full object
            # Use simple SQL execution for speed instead of ORM overhead
            # Construct raw SQL query for maximum performance
            
            select_cols = ", ".join([f"COALESCE({col}, 0)" for col in month_cols])
            
            sql = f"""
                SELECT idpel, nama, alamat, {select_cols}
                FROM customers_2025
            """
            
            params = {}
            if unitup:
                sql += " WHERE unitup = :unitup"
                params['unitup'] = unitup
                
            # Optimization: Don't sort in SQL unless we have a computed column
            # We will fetch and compute in python using optimized list comprehension
                
            query = text(sql)
            # Use session.execute instead of manual connection to be safer with ORM session state
            result = self.db.execute(query, params)
            
            anomalies = []
            
            # Fast iteration
            for row in result:
                # row: idpel, nama, alamat, m1, m2... m12
                # 0, 1, 2, 3..14
                
                # Fast numeric access (row is tuple-like)
                # Slice 3:15 are the months
                # IMPORTANT: Cast to float to avoid Decimal vs float issues
                try:
                    values = [float(x) for x in row[3:15]]
                except (ValueError, TypeError):
                    continue
                
                # Skip if customer has 6 or more months with 0 usage
                # This prevents extreme mathematical anomalies (e.g. 1000%+) 
                # for customers who basically don't use their electricity.
                zero_months_count = values.count(0)
                if zero_months_count >= 6:
                    continue

                # Optimized Mean/Dev Calc (No stats module)
                current_sum = sum(values)
                # count = 12
                mean = current_sum / 12.0
                
                if mean < 1: continue

                max_val = max(values)
                min_val = min(values)
                
                dev_max = max_val - mean
                dev_min = min_val - mean
                
                if abs(dev_max) > abs(dev_min):
                    max_dev = dev_max
                    ext_index = values.index(max_val)
                else:
                    max_dev = dev_min
                    ext_index = values.index(min_val)
                    
                deviation_pct = (max_dev / mean) * 100
                
                # Filter out pure mathematical noise:
                # E.g. averaging 1 kWh and jumping to 50 kWh is a 5000% anomaly
                # but physically irrelevant. Require at least ~50 kWh absolute difference
                if abs(max_dev) < 50:
                    continue
                    
                # Filter check (Inlined for speed)
                # Default (-50 to 50 instead of 5) to ensure it's truly an anomaly
                if min_pct is None and max_pct is None:
                    if -50 < deviation_pct < 50: continue
                else:
                    if min_pct is not None and deviation_pct < min_pct: continue
                    if max_pct is not None and deviation_pct > max_pct: continue
                
                months_ids = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Ags', 'Sep', 'Okt', 'Nov', 'Des']
                ext_month = months_ids[ext_index]
                
                # Info formatting (Lazy, only if passes filter)
                info_text = f"{int(deviation_pct)}%"
                if deviation_pct <= -100: info_text += f" (Drop Total di {ext_month})"
                elif deviation_pct <= -80: info_text += f" (Drop Ekstrem di {ext_month})"
                elif deviation_pct <= -50: info_text += f" (Drop Signifikan di {ext_month})"
                elif deviation_pct >= 100: info_text += f" (Lonjakan Ekstrem di {ext_month})"
                elif deviation_pct >= 50: info_text += f" (Lonjakan Signifikan di {ext_month})"
                else: info_text += f" (Anomali di {ext_month})"

                anomalies.append({
                    "idpel": row[0],
                    "nama": row[1],
                    "alamat": row[2],
                    "range": abs(deviation_pct),
                    "info": info_text,
                    "deviation_pct": deviation_pct
                })
            
            # Sort in memory (Python is decent at sorting 100k items)
            # If anomalies list > 100k, we might want to trim it
            anomalies.sort(key=lambda x: x['range'], reverse=True)
            
            # Save to Cache
            _MEMORY_CACHE[cache_key] = {
                'timestamp': current_time,
                'data': anomalies
            }
            
            # Pagination
            total_items = len(anomalies)
            total_pages = (total_items + limit - 1) // limit if total_items > 0 else 1
            
            if page < 1: page = 1
            if page > total_pages: page = total_pages

            start = (page - 1) * limit
            end = start + limit
            paginated_data = anomalies[start:end]

            return {
                "data": paginated_data,
                "total": total_items,
                "page": page,
                "pages": total_pages
            }
        except Exception as e:
            print("ERROR IN GET_ANOMALIES_HIGH_VARIANCE:")
            traceback.print_exc()
            # Return empty structure instead of crashing
            return {
                "data": [],
                "total": 0,
                "page": page,
                "pages": 1,
                "error": str(e)
            }

    def get_infrastructure_load(self, limit: int = 50, unitup: int = None) -> List[Dict[str, Any]]:
        """
        Aggregates consumption by Gardu. 
        Returns Top N busiest Gardu.
        """
        # Sum of all months in 2025 per Gardu
        total_kwh_expr = (
            func.coalesce(Customer2025.jan_2025, 0) + func.coalesce(Customer2025.feb_2025, 0) +
            func.coalesce(Customer2025.mar_2025, 0) + func.coalesce(Customer2025.apr_2025, 0) +
            func.coalesce(Customer2025.may_2025, 0) + func.coalesce(Customer2025.jun_2025, 0) +
            func.coalesce(Customer2025.jul_2025, 0) + func.coalesce(Customer2025.aug_2025, 0) +
            func.coalesce(Customer2025.sep_2025, 0) + func.coalesce(Customer2025.oct_2025, 0) +
            func.coalesce(Customer2025.nov_2025, 0) + func.coalesce(Customer2025.dec_2025, 0)
        )
        
        base_query = self.db.query(
            Customer2025.gardu,
            func.count(Customer2025.idpel).label("customer_count"),
            func.sum(Customer2025.daya).label("total_daya"),
            func.sum(total_kwh_expr).label("total_kwh")
        ).filter(Customer2025.gardu.isnot(None))

        if unitup:
            base_query = base_query.filter(Customer2025.unitup == unitup)

        query = (
            base_query
            .group_by(Customer2025.gardu)
            .having(func.count(Customer2025.idpel) < 2000)
            .order_by(func.sum(total_kwh_expr).desc())
            .limit(limit)
        )
        
        results = query.all()
        
        # New: Get 2024 data for these specific Gardus
        gardu_list = [row.gardu for row in results]
        
        if not gardu_list:
            return []

        # Sum 2024 for these gardus
        total_kwh_2024_expr = (
            func.coalesce(Customer2024.jan_2024, 0) + func.coalesce(Customer2024.feb_2024, 0) +
            func.coalesce(Customer2024.mar_2024, 0) + func.coalesce(Customer2024.apr_2024, 0) +
            func.coalesce(Customer2024.may_2024, 0) + func.coalesce(Customer2024.jun_2024, 0) +
            func.coalesce(Customer2024.jul_2024, 0) + func.coalesce(Customer2024.aug_2024, 0) +
            func.coalesce(Customer2024.sep_2024, 0) + func.coalesce(Customer2024.oct_2024, 0) +
            func.coalesce(Customer2024.nov_2024, 0) + func.coalesce(Customer2024.dec_2024, 0)
        )

        query_2024 = (
            self.db.query(
                Customer2024.gardu,
                func.sum(total_kwh_2024_expr).label("total_kwh_2024")
            )
            .filter(Customer2024.gardu.in_(gardu_list))
            .group_by(Customer2024.gardu)
        )
        
        results_2024 = {row.gardu: float(row.total_kwh_2024 or 0) for row in query_2024.all()}

        return [
            {
                "gardu": row.gardu,
                "customer_count": row.customer_count,
                "total_daya": float(row.total_daya or 0),
                "total_kwh": float(row.total_kwh or 0),
                "total_kwh_2024": results_2024.get(row.gardu, 0)
            }
            for row in results
        ]

    def get_power_changes(self, unitup: int = None) -> Dict[str, Any]:
        """
        Compare 2024 and 2025 to find power upgrades/downgrades.
        """
        sql = """
            SELECT 
                c25.idpel, c25.nama, c24.daya as daya_2024, c25.daya as daya_2025
            FROM customers_2025 c25
            JOIN customers_2024 c24 ON c25.idpel = c24.idpel
            WHERE c25.daya != c24.daya
        """
        params = {}
        if unitup:
            sql += " AND c25.unitup = :unitup"
            params['unitup'] = unitup

        query = text(sql)
        result = self.db.execute(query, params).fetchall()
        
        upgrades = []
        downgrades = []
        
        for row in result:
            item = {
                "idpel": row.idpel,
                "nama": row.nama,
                "daya_2024": row.daya_2024,
                "daya_2025": row.daya_2025,
                "diff": row.daya_2025 - row.daya_2024
            }
            if item["diff"] > 0:
                upgrades.append(item)
            else:
                downgrades.append(item)
                
        return {
            "summary": {
                "total_upgrades": len(upgrades),
                "total_downgrades": len(downgrades),
                "total_kva_added": sum(u["diff"] for u in upgrades) / 1000,
                "total_kva_reduced": abs(sum(d["diff"] for d in downgrades)) / 1000
            },
            "upgrades": upgrades, # Return ALL data
            "downgrades": downgrades # Return ALL data
        }

    def get_daya_distribution(self, year: int = 2025, unitup: int = None):
        """Get distribution of customers and energy by Power Limit (Daya)"""
        
        Model = Customer2025 if year == 2025 else Customer2024
        
        # Determine cols to sum
        month_cols = []
        if year == 2025:
             month_cols = [
                'dec_2024', 'jan_2025', 'feb_2025', 'mar_2025', 'apr_2025', 'may_2025',
                'jun_2025', 'jul_2025', 'aug_2025', 'sep_2025', 'oct_2025', 'nov_2025', 'dec_2025'
            ]
        else:
             month_cols = [
                'dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024'
            ]
        
        def sum_cols_expr(cols):
            return sum(func.coalesce(getattr(Model, col), 0) for col in cols)

        # Aggregate by Daya
        query = self.db.query(
            Model.daya,
            func.count(Model.idpel).label('count'),
            func.sum(sum_cols_expr(month_cols)).label('total_kwh')
        )
        if unitup:
            query = query.filter(Model.unitup == unitup)
            
        results = query.group_by(Model.daya).order_by(func.count(Model.idpel).desc()).all()

        # If year 2025, fetch 2024 comparisons for growth calculation
        comparison_map = {}
        if year == 2025:
            # Aggregate 2024 data
             # Month cols for 2024
            month_cols_24 = [
                'dec_2023', 'jan_2024', 'feb_2024', 'mar_2024', 'apr_2024', 'may_2024',
                'jun_2024', 'jul_2024', 'aug_2024', 'sep_2024', 'oct_2024', 'nov_2024', 'dec_2024'
            ]
            
            def sum_cols_expr_24(cols):
                return sum(func.coalesce(getattr(Customer2024, col), 0) for col in cols)

            results_2024_query = self.db.query(
                Customer2024.daya,
                func.count(Customer2024.idpel).label('count'),
                func.sum(sum_cols_expr_24(month_cols_24)).label('total_kwh')
            )
            
            if unitup:
                results_2024_query = results_2024_query.filter(Customer2024.unitup == unitup)
                
            results_2024_rows = results_2024_query.group_by(Customer2024.daya).all()
            
            comparison_map = {int(row.daya or 0): {"count": row.count, "kwh": float(row.total_kwh or 0)} for row in results_2024_rows}

        distribution = []
        for row in results:
            daya_val = int(row.daya) if row.daya else 0
            count = row.count
            total_kwh = float(row.total_kwh or 0)
            
            # Comparison Logic
            growth_count = 0
            growth_kwh = 0
            
            if year == 2025:
                prev = comparison_map.get(daya_val)
                if prev and prev["count"] > 0:
                    growth_count = ((count - prev["count"]) / prev["count"]) * 100
                if prev and prev["kwh"] > 0:
                     growth_kwh = ((total_kwh - prev["kwh"]) / prev["kwh"]) * 100

            distribution.append({
                "daya": daya_val,
                "count": count,
                "total_kwh": total_kwh,
                "label": f"{row.daya} VA",
                "growth_count": growth_count,
                "growth_kwh": growth_kwh
            })
            
        return distribution
