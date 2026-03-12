from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Customer2024, Customer2025
from schemas import Customer2024Response, Customer2025Response, CustomerAnalysis, MonthlyData, PaginatedResponse, SummaryStats
from services.analysis import AnalysisService

router = APIRouter(prefix="/api/customers", tags=["customers"])

# IMPORTANT: Routes dengan path spesifik harus didefinisikan SEBELUM route dengan path parameter
# karena FastAPI akan mencocokkan dari atas ke bawah

@router.get("/dashboard", response_model=SummaryStats)
async def get_dashboard_stats(unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get dashboard overview statistics"""
    service = AnalysisService(db)
    return service.get_dashboard_stats(unitup)

@router.get("/dashboard/trends", response_model=List[MonthlyData])
async def get_dashboard_trends(unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get aggregate monthly trends for dashboard chart"""
    service = AnalysisService(db)
    return service.get_aggregate_trends(unitup)

@router.get("/dashboard/distribution")
async def get_dashboard_distribution(unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get distribution stats for charts"""
    service = AnalysisService(db)
    return service.get_distribution_stats(unitup)

@router.get("/dashboard/difference-analysis")
async def get_dashboard_comparison(unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get comparative usage stats (2024 vs 2025) by Tarif, Jenis, Layanan"""
    service = AnalysisService(db)
    return service.get_usage_distribution_comparison(unitup)

@router.get("/new", response_model=PaginatedResponse)
async def get_new_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    tarif: Optional[str] = None,
    jenis: Optional[str] = None,
    layanan: Optional[str] = None,
    gardu: Optional[str] = None,
    unitup: Optional[str] = None,
    daya: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of new customers in 2025"""
    service = AnalysisService(db)
    result = service.get_new_customers(page=page, page_size=page_size, tarif=tarif, jenis=jenis, layanan=layanan, gardu=gardu, unitup=unitup, daya=daya)
    return result

@router.get("/lost", response_model=PaginatedResponse)
async def get_lost_customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    tarif: Optional[str] = None,
    jenis: Optional[str] = None,
    layanan: Optional[str] = None,
    gardu: Optional[str] = None,
    unitup: Optional[str] = None,
    daya: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of customers lost from 2024 to 2025"""
    service = AnalysisService(db)
    result = service.get_lost_customers(page=page, page_size=page_size, tarif=tarif, jenis=jenis, layanan=layanan, gardu=gardu, unitup=unitup, daya=daya)
    return result

@router.get("/all/{year}", response_model=PaginatedResponse)
async def get_all_customers(
    year: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    tarif: Optional[str] = None,
    jenis: Optional[str] = None,
    layanan: Optional[str] = None,
    gardu: Optional[str] = None,
    unitup: Optional[str] = None,
    daya: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all customers for a specific year with filters"""
    if year not in [2024, 2025]:
        raise HTTPException(status_code=400, detail="Year must be 2024 or 2025")
    service = AnalysisService(db)
    result = service.get_all_customers(year=year, page=page, page_size=page_size, tarif=tarif, jenis=jenis, layanan=layanan, gardu=gardu, unitup=unitup, daya=daya)
    return result

@router.get("/filter-options/{year}")
async def get_filter_options(year: int, db: Session = Depends(get_db)):
    """Get unique filter options for a specific year"""
    if year not in [2024, 2025]:
        raise HTTPException(status_code=400, detail="Year must be 2024 or 2025")
    
    if year == 2024:
        tarif_options = db.query(Customer2024.tarif).distinct().filter(Customer2024.tarif.isnot(None)).order_by(Customer2024.tarif).all()
        jenis_options = db.query(Customer2024.jenis).distinct().filter(Customer2024.jenis.isnot(None)).order_by(Customer2024.jenis).all()
        layanan_options = db.query(Customer2024.layanan).distinct().filter(Customer2024.layanan.isnot(None)).order_by(Customer2024.layanan).all()
        gardu_options = db.query(Customer2024.gardu).distinct().filter(Customer2024.gardu.isnot(None)).order_by(Customer2024.gardu).all()
        unitup_options = db.query(Customer2024.unitup).distinct().filter(Customer2024.unitup.isnot(None)).order_by(Customer2024.unitup).all()
        daya_options = db.query(Customer2024.daya).distinct().filter(Customer2024.daya.isnot(None)).order_by(Customer2024.daya).all()
    else:
        tarif_options = db.query(Customer2025.tarif).distinct().filter(Customer2025.tarif.isnot(None)).order_by(Customer2025.tarif).all()
        jenis_options = db.query(Customer2025.jenis).distinct().filter(Customer2025.jenis.isnot(None)).order_by(Customer2025.jenis).all()
        layanan_options = db.query(Customer2025.layanan).distinct().filter(Customer2025.layanan.isnot(None)).order_by(Customer2025.layanan).all()
        gardu_options = db.query(Customer2025.gardu).distinct().filter(Customer2025.gardu.isnot(None)).order_by(Customer2025.gardu).all()
        unitup_options = db.query(Customer2025.unitup).distinct().filter(Customer2025.unitup.isnot(None)).order_by(Customer2025.unitup).all()
        daya_options = db.query(Customer2025.daya).distinct().filter(Customer2025.daya.isnot(None)).order_by(Customer2025.daya).all()
    
    return {
        "tarif": [opt[0] for opt in tarif_options if opt[0]],
        "jenis": [opt[0] for opt in jenis_options if opt[0]],
        "layanan": [opt[0] for opt in layanan_options if opt[0]],
        "gardu": [opt[0] for opt in gardu_options if opt[0]],
        "unitup": [opt[0] for opt in unitup_options if opt[0] is not None],
        "daya": [opt[0] for opt in daya_options if opt[0] is not None]
    }

def _orm_to_response(orm_obj, schema_class):
    """Convert ORM to Pydantic model, ensuring Decimal -> float for JSON."""
    d = {}
    for k, v in orm_obj.__dict__.items():
        if k.startswith("_"):
            continue
        if hasattr(v, "__float__") and not isinstance(v, (int, bool, type(None))):
            try:
                d[k] = float(v)
            except (TypeError, ValueError):
                d[k] = v
        else:
            d[k] = v
    return schema_class.model_validate(d)


@router.get("/{idpel}", response_model=dict)
async def get_customer(idpel: int, db: Session = Depends(get_db)):
    """Get customer data by IDPEL"""
    try:
        customer_2024 = db.query(Customer2024).filter(Customer2024.idpel == idpel).first()
        customer_2025 = db.query(Customer2025).filter(Customer2025.idpel == idpel).first()
        
        if not customer_2024 and not customer_2025:
            raise HTTPException(status_code=404, detail=f"Customer with IDPEL {idpel} not found")
        
        result = {}
        if customer_2024:
            result["2024"] = _orm_to_response(customer_2024, Customer2024Response)
        if customer_2025:
            result["2025"] = _orm_to_response(customer_2025, Customer2025Response)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Gagal memuat data pelanggan.")

@router.get("/{idpel}/analysis", response_model=CustomerAnalysis)
async def get_customer_analysis(idpel: int, db: Session = Depends(get_db)):
    """Get complete analysis for a customer"""
    service = AnalysisService(db)
    analysis = service.analyze_customer(idpel)
    
    if not analysis:
        raise HTTPException(status_code=404, detail=f"Customer with IDPEL {idpel} not found")
    
    return analysis

@router.get("/{idpel}/trends", response_model=List[MonthlyData])
async def get_customer_trends(idpel: int, db: Session = Depends(get_db)):
    """Get monthly consumption trends for a customer"""
    service = AnalysisService(db)
    trends = service.get_monthly_trends(idpel)
    
    if not trends:
        raise HTTPException(status_code=404, detail=f"Customer with IDPEL {idpel} not found")
    
    return trends

