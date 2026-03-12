from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from services.advanced_analysis import AdvancedAnalysisService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/pareto")
def get_pareto(limit: int = 100, unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    service = AdvancedAnalysisService(db)
    return service.get_pareto_analysis(limit, unitup)

@router.get("/anomalies/zero-usage")
def get_zero_usage(page: int = 1, limit: int = 50, unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    service = AdvancedAnalysisService(db)
    return service.get_anomalies_zero_usage(page, limit, unitup)

@router.get("/anomalies/high-variance")
def get_high_variance(
    page: int = 1, 
    limit: int = 50, 
    unitup: Optional[int] = Query(None), 
    min_pct: Optional[int] = Query(None),
    max_pct: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    service = AdvancedAnalysisService(db)
    return service.get_anomalies_high_variance(page, limit, unitup, min_pct, max_pct)

@router.get("/infrastructure/gardu")
def get_gardu_stats(limit: int = 50, unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    service = AdvancedAnalysisService(db)
    return service.get_infrastructure_load(limit, unitup)

@router.get("/lifecycle/power-changes")
def get_power_changes(unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get power upgrade/downgrade stats"""
    service = AdvancedAnalysisService(db)
    return service.get_power_changes(unitup)

# New ULP Analysis Endpoints
from services.ulp_analysis import UlpAnalysisService

@router.get("/ulp/overview")
def get_ulp_overview(db: Session = Depends(get_db)):
    """Get performance overview of all ULPs"""
    service = UlpAnalysisService(db)
    return service.get_overview()



@router.get("/distribution/daya")
def get_daya_distribution(year: int = 2025, unitup: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """Get customer distribution by Power Limit (Daya). Year: 2024 or 2025."""
    service = AdvancedAnalysisService(db)
    return service.get_daya_distribution(year, unitup)
