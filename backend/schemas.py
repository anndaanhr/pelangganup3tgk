from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

# Schema untuk response pelanggan
class CustomerBase(BaseModel):
    idpel: int
    unitup: Optional[int] = None  # Unit UP3
    nama: Optional[str] = None
    alamat: Optional[str] = None
    tarif: Optional[str] = None
    daya: Optional[int] = None
    kddk: Optional[str] = None
    cater: Optional[str] = None
    penyulang: Optional[str] = None  # Unit ULP
    gardu: Optional[str] = None
    nomor_meter: Optional[int] = None
    jenis: Optional[str] = None
    layanan: Optional[str] = None
    kd_proses: Optional[str] = None  # Kode Proses

class Customer2024Response(CustomerBase):
    merk_kwh: Optional[str] = None
    dec_2023: Optional[Decimal] = None
    jan_2024: Optional[Decimal] = None
    feb_2024: Optional[Decimal] = None
    mar_2024: Optional[Decimal] = None
    apr_2024: Optional[Decimal] = None
    may_2024: Optional[Decimal] = None
    jun_2024: Optional[Decimal] = None
    jul_2024: Optional[Decimal] = None
    aug_2024: Optional[Decimal] = None
    sep_2024: Optional[Decimal] = None
    oct_2024: Optional[Decimal] = None
    nov_2024: Optional[Decimal] = None
    dec_2024: Optional[Decimal] = None
    
    model_config = {"from_attributes": True}

class Customer2025Response(CustomerBase):
    dec_2024: Optional[Decimal] = None
    jan_2025: Optional[Decimal] = None
    feb_2025: Optional[Decimal] = None
    mar_2025: Optional[Decimal] = None
    apr_2025: Optional[Decimal] = None
    may_2025: Optional[Decimal] = None
    jun_2025: Optional[Decimal] = None
    jul_2025: Optional[Decimal] = None
    aug_2025: Optional[Decimal] = None
    sep_2025: Optional[Decimal] = None
    oct_2025: Optional[Decimal] = None
    nov_2025: Optional[Decimal] = None
    dec_2025: Optional[Decimal] = None
    
    model_config = {"from_attributes": True}

# Schema untuk analisis bulanan
class MonthlyData(BaseModel):
    month: str
    value_2024: Optional[float] = None
    value_2025: Optional[float] = None

# Schema untuk analisis pelanggan
class CustomerAnalysis(BaseModel):
    idpel: int
    nama: Optional[str] = None
    status: str  # 'active', 'new', 'lost'
    total_2024: Optional[float] = None
    total_2025: Optional[float] = None
    difference: Optional[float] = None
    percentage_change: Optional[float] = None
    monthly_data: List[MonthlyData]
    customer_2024: Optional[Customer2024Response] = None
    customer_2025: Optional[Customer2025Response] = None
    attribute_changes: Optional[dict] = None  # Perubahan TARIF, DAYA, dll

# Schema untuk statistik agregat
class SummaryStats(BaseModel):
    total_customers_2024: int
    total_customers_2025: int
    active_customers: int
    new_customers: int
    lost_customers: int
    total_consumption_2024: Optional[float] = None
    total_consumption_2025: Optional[float] = None
    avg_consumption_2024: Optional[float] = None
    avg_consumption_2025: Optional[float] = None
    consumption_change_percent: Optional[float] = None

# Schema untuk pengelompokan
class GroupStats(BaseModel):
    group_name: str
    count_2024: int
    count_2025: int
    total_consumption_2024: Optional[float] = None
    total_consumption_2025: Optional[float] = None

# Schema untuk pagination
class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int

