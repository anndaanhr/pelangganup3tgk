"""
Service untuk analisis data pelanggan
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, select
from typing import Optional, List, Dict
from models import Customer2024, Customer2025
from schemas import CustomerAnalysis, MonthlyData, PaginatedResponse, Customer2024Response, Customer2025Response
from decimal import Decimal

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_customer(self, idpel: int) -> Optional[CustomerAnalysis]:
        """Analisis lengkap untuk satu pelanggan"""
        customer_2024 = self.db.query(Customer2024).filter(Customer2024.idpel == idpel).first()
        customer_2025 = self.db.query(Customer2025).filter(Customer2025.idpel == idpel).first()
        
        if not customer_2024 and not customer_2025:
            return None
        
        # Tentukan status
        if customer_2024 and customer_2025:
            status = "active"
        elif customer_2025:
            status = "new"
        else:
            status = "lost"
        
        # Hitung total konsumsi
        total_2024 = self._calculate_total(customer_2024, 2024) if customer_2024 else None
        total_2025 = self._calculate_total(customer_2025, 2025) if customer_2025 else None
        
        # Hitung selisih dan persentase
        difference = None
        percentage_change = None
        if total_2024 is not None and total_2025 is not None:
            total_2024_float = float(total_2024)
            total_2025_float = float(total_2025)
            difference = total_2025_float - total_2024_float
            if total_2024_float > 0:
                percentage_change = (difference / total_2024_float) * 100
        
        # Data bulanan
        monthly_data = self.get_monthly_trends(idpel)
        
        # Perubahan atribut - tidak menyamakan tarif/jenis antar tahun
        attribute_changes = None
        if customer_2024 and customer_2025:
            changes = {}
            # Perhatikan: tarif dan jenis bisa berbeda antar tahun, jadi tidak disamakan
            if customer_2024.tarif != customer_2025.tarif:
                changes['tarif'] = {'from': customer_2024.tarif, 'to': customer_2025.tarif}
            if customer_2024.daya != customer_2025.daya:
                changes['daya'] = {'from': customer_2024.daya, 'to': customer_2025.daya}
            if customer_2024.jenis != customer_2025.jenis:
                changes['jenis'] = {'from': customer_2024.jenis, 'to': customer_2025.jenis}
            if customer_2024.layanan != customer_2025.layanan:
                changes['layanan'] = {'from': customer_2024.layanan, 'to': customer_2025.layanan}
            if customer_2024.unitup != customer_2025.unitup:
                changes['unitup'] = {'from': customer_2024.unitup, 'to': customer_2025.unitup}
            if customer_2024.penyulang != customer_2025.penyulang:
                changes['penyulang'] = {'from': customer_2024.penyulang, 'to': customer_2025.penyulang}
            if customer_2024.kd_proses != customer_2025.kd_proses:
                changes['kd_proses'] = {'from': customer_2024.kd_proses, 'to': customer_2025.kd_proses}
            if changes:
                attribute_changes = changes
        
        return CustomerAnalysis(
            idpel=idpel,
            nama=customer_2025.nama if customer_2025 else (customer_2024.nama if customer_2024 else None),
            status=status,
            total_2024=float(total_2024) if total_2024 else None,
            total_2025=float(total_2025) if total_2025 else None,
            difference=difference,
            percentage_change=percentage_change,
            monthly_data=monthly_data,
            customer_2024=Customer2024Response.model_validate(customer_2024) if customer_2024 else None,
            customer_2025=Customer2025Response.model_validate(customer_2025) if customer_2025 else None,
            attribute_changes=attribute_changes
        )
    
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
    
    def get_monthly_trends(self, idpel: int) -> List[MonthlyData]:
        """Get data tren bulanan"""
        customer_2024 = self.db.query(Customer2024).filter(Customer2024.idpel == idpel).first()
        customer_2025 = self.db.query(Customer2025).filter(Customer2025.idpel == idpel).first()
        
        months_2024 = [
            ('Des 2023', 'dec_2023'),
            ('Jan 2024', 'jan_2024'), ('Feb 2024', 'feb_2024'), ('Mar 2024', 'mar_2024'),
            ('Apr 2024', 'apr_2024'), ('Mei 2024', 'may_2024'), ('Jun 2024', 'jun_2024'),
            ('Jul 2024', 'jul_2024'), ('Agu 2024', 'aug_2024'), ('Sep 2024', 'sep_2024'),
            ('Okt 2024', 'oct_2024'), ('Nov 2024', 'nov_2024'), ('Des 2024', 'dec_2024')
        ]
        
        months_2025 = [
            ('Des 2024', 'dec_2024'),
            ('Jan 2025', 'jan_2025'), ('Feb 2025', 'feb_2025'), ('Mar 2025', 'mar_2025'),
            ('Apr 2025', 'apr_2025'), ('Mei 2025', 'may_2025'), ('Jun 2025', 'jun_2025'),
            ('Jul 2025', 'jul_2025'), ('Agu 2025', 'aug_2025'), ('Sep 2025', 'sep_2025'),
            ('Okt 2025', 'oct_2025'), ('Nov 2025', 'nov_2025'), ('Des 2025', 'dec_2025')
        ]
        
        # Map untuk perbandingan (Des 2024 muncul di kedua)
        monthly_data = []
        
        # Data 2024
        if customer_2024:
            for month_label, col_name in months_2024:
                val = getattr(customer_2024, col_name, None)
                monthly_data.append(MonthlyData(
                    month=month_label,
                    value_2024=float(val) if val is not None else None,
                    value_2025=None
                ))
        
        # Data 2025 (overwrite Des 2024 jika ada)
        if customer_2025:
            for month_label, col_name in months_2025:
                val = getattr(customer_2025, col_name, None)
                # Cari entry yang sudah ada atau buat baru
                found = False
                for md in monthly_data:
                    if md.month == month_label:
                        md.value_2025 = float(val) if val is not None else None
                        found = True
                        break
                if not found:
                    monthly_data.append(MonthlyData(
                        month=month_label,
                        value_2024=None,
                        value_2025=float(val) if val is not None else None
                    ))
        
        return monthly_data
    
    def get_new_customers(self, page: int = 1, page_size: int = 50, 
                         tarif: Optional[str] = None, jenis: Optional[str] = None,
                         layanan: Optional[str] = None) -> PaginatedResponse:
        """Get pelanggan baru di 2025"""
        # Pelanggan yang ada di 2025 tapi tidak ada di 2024
        # Gunakan subquery untuk menghindari masalah dengan set kosong
        idpel_2024_subquery = select(Customer2024.idpel).subquery()
        
        query = self.db.query(Customer2025).filter(
            ~Customer2025.idpel.in_(select(idpel_2024_subquery.c.idpel))
        )
        
        # Filter
        if tarif:
            query = query.filter(Customer2025.tarif == tarif)
        if jenis:
            query = query.filter(Customer2025.jenis == jenis)
        if layanan:
            query = query.filter(Customer2025.layanan == layanan)
        
        total = query.count()
        offset = (page - 1) * page_size
        customers = query.offset(offset).limit(page_size).all()
        
        items = []
        for customer in customers:
            total_2025 = self._calculate_total(customer, 2025)
            items.append({
                'idpel': customer.idpel,
                'nama': customer.nama,
                'alamat': customer.alamat,
                'tarif': customer.tarif,
                'daya': customer.daya,
                'jenis': customer.jenis,
                'layanan': customer.layanan,
                'gardu': customer.gardu,
                'total_consumption_2025': float(total_2025) if total_2025 else None
            })
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size if total > 0 else 0
        )
    
    def get_lost_customers(self, page: int = 1, page_size: int = 50,
                          tarif: Optional[str] = None, jenis: Optional[str] = None,
                          layanan: Optional[str] = None) -> PaginatedResponse:
        """Get pelanggan yang hilang dari 2024 ke 2025"""
        # Pelanggan yang ada di 2024 tapi tidak ada di 2025
        # Gunakan subquery untuk menghindari masalah dengan set kosong
        idpel_2025_subquery = select(Customer2025.idpel).subquery()
        
        query = self.db.query(Customer2024).filter(
            ~Customer2024.idpel.in_(select(idpel_2025_subquery.c.idpel))
        )
        
        # Filter
        if tarif:
            query = query.filter(Customer2024.tarif == tarif)
        if jenis:
            query = query.filter(Customer2024.jenis == jenis)
        if layanan:
            query = query.filter(Customer2024.layanan == layanan)
        
        total = query.count()
        offset = (page - 1) * page_size
        customers = query.offset(offset).limit(page_size).all()
        
        items = []
        for customer in customers:
            total_2024 = self._calculate_total(customer, 2024)
            items.append({
                'idpel': customer.idpel,
                'nama': customer.nama,
                'alamat': customer.alamat,
                'tarif': customer.tarif,
                'daya': customer.daya,
                'jenis': customer.jenis,
                'layanan': customer.layanan,
                'gardu': customer.gardu,
                'total_consumption_2024': float(total_2024) if total_2024 else None
            })
        
        return PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size if total > 0 else 0
        )
    
    def get_dashboard_stats(self):
        """Get dashboard overview statistics"""
        from schemas import SummaryStats
        
        total_2024 = self.db.query(Customer2024).count()
        total_2025 = self.db.query(Customer2025).count()
        
        # Get active customers (ada di kedua tahun)
        idpel_2024_set = {row[0] for row in self.db.query(Customer2024.idpel).all()}
        idpel_2025_set = {row[0] for row in self.db.query(Customer2025.idpel).all()}
        active_customers = len(idpel_2024_set & idpel_2025_set)
        new_customers = len(idpel_2025_set - idpel_2024_set)
        lost_customers = len(idpel_2024_set - idpel_2025_set)
        
        # Calculate total consumption
        total_consumption_2024 = Decimal(0)
        count_2024 = 0
        for customer in self.db.query(Customer2024).all():
            total = self._calculate_total(customer, 2024)
            if total:
                total_consumption_2024 += total
                count_2024 += 1
        
        total_consumption_2025 = Decimal(0)
        count_2025 = 0
        for customer in self.db.query(Customer2025).all():
            total = self._calculate_total(customer, 2025)
            if total:
                total_consumption_2025 += total
                count_2025 += 1
        
        avg_2024 = float(total_consumption_2024 / count_2024) if count_2024 > 0 else None
        avg_2025 = float(total_consumption_2025 / count_2025) if count_2025 > 0 else None
        
        consumption_change = None
        if total_consumption_2024 > 0 and total_consumption_2025 > 0:
            consumption_change = float((total_consumption_2025 - total_consumption_2024) / total_consumption_2024 * 100)
        
        return SummaryStats(
            total_customers_2024=total_2024,
            total_customers_2025=total_2025,
            active_customers=active_customers,
            new_customers=new_customers,
            lost_customers=lost_customers,
            total_consumption_2024=float(total_consumption_2024) if total_consumption_2024 > 0 else None,
            total_consumption_2025=float(total_consumption_2025) if total_consumption_2025 > 0 else None,
            avg_consumption_2024=avg_2024,
            avg_consumption_2025=avg_2025,
            consumption_change_percent=consumption_change
        )
    
    def get_all_customers(self, year: int, page: int = 1, page_size: int = 50,
                         tarif: Optional[str] = None, jenis: Optional[str] = None,
                         layanan: Optional[str] = None, gardu: Optional[str] = None) -> PaginatedResponse:
        """Get all customers untuk tahun tertentu dengan filter"""
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

