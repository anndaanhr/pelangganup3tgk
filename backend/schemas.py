from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class MonthlyData(BaseModel):
    month: str
    value_2024: Optional[float] = None
    value_2025: Optional[float] = None
    
    class Config:
        from_attributes = True

class Customer2024Response(BaseModel):
    idpel: int
    unitup: Optional[int] = None
    nama: Optional[str] = None
    alamat: Optional[str] = None
    tarif: Optional[str] = None
    daya: Optional[int] = None
    kddk: Optional[str] = None
    cater: Optional[str] = None
    penyulang: Optional[str] = None
    gardu: Optional[str] = None
    merk_kwh: Optional[str] = None
    nomor_meter: Optional[int] = None
    jenis: Optional[str] = None
    layanan: Optional[str] = None
    kd_proses: Optional[str] = None
    
    # Monthly data
    dec_2023: Optional[float] = None
    jan_2024: Optional[float] = None
    feb_2024: Optional[float] = None
    mar_2024: Optional[float] = None
    apr_2024: Optional[float] = None
    may_2024: Optional[float] = None
    jun_2024: Optional[float] = None
    jul_2024: Optional[float] = None
    aug_2024: Optional[float] = None
    sep_2024: Optional[float] = None
    oct_2024: Optional[float] = None
    nov_2024: Optional[float] = None
    dec_2024: Optional[float] = None

    class Config:
        from_attributes = True

class Customer2025Response(BaseModel):
    idpel: int
    unitup: Optional[int] = None
    nama: Optional[str] = None
    alamat: Optional[str] = None
    tarif: Optional[str] = None
    daya: Optional[int] = None
    kddk: Optional[str] = None
    cater: Optional[str] = None
    penyulang: Optional[str] = None
    gardu: Optional[str] = None
    nomor_meter: Optional[int] = None
    jenis: Optional[str] = None
    layanan: Optional[str] = None
    kd_proses: Optional[str] = None
    
    # Monthly data
    dec_2024: Optional[float] = None
    jan_2025: Optional[float] = None
    feb_2025: Optional[float] = None
    mar_2025: Optional[float] = None
    apr_2025: Optional[float] = None
    may_2025: Optional[float] = None
    jun_2025: Optional[float] = None
    jul_2025: Optional[float] = None
    aug_2025: Optional[float] = None
    sep_2025: Optional[float] = None
    oct_2025: Optional[float] = None
    nov_2025: Optional[float] = None
    dec_2025: Optional[float] = None

    class Config:
        from_attributes = True

class CustomerAnalysis(BaseModel):
    idpel: int
    nama: Optional[str] = None
    status: str  # active, new, lost
    total_2024: Optional[float] = None
    total_2025: Optional[float] = None
    difference: Optional[float] = None
    percentage_change: Optional[float] = None
    monthly_data: List[MonthlyData]
    customer_2024: Optional[Customer2024Response] = None
    customer_2025: Optional[Customer2025Response] = None
    attribute_changes: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    items: List[Dict[str, Any]]  # Simplified for flexibility, or use specific schemas
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True

class SummaryStats(BaseModel):
    total_customers_2024: int
    total_customers_2025: int
    active_customers: int
    new_customers: int
    lost_customers: int
    
    total_consumption_2024: float
    total_consumption_2025: float
    
    # New fields for explicit Revenue vs Energy
    total_revenue_2024: Optional[float] = 0
    total_revenue_2025: Optional[float] = 0
    total_energy_2024: Optional[float] = 0
    total_energy_2025: Optional[float] = 0

    avg_consumption_2024: float
    avg_consumption_2025: float
    consumption_change_percent: Optional[float] = None

    class Config:
        from_attributes = True
