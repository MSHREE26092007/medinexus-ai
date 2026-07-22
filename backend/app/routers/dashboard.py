"""Dashboard analytics endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

TOTAL_BEDS = 50  # hackathon constant — make configurable later


@router.get("/stats", response_model=schemas.DashboardStats)
def dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(models.Patient.id)).scalar() or 0
    admitted = (db.query(func.count(models.Patient.id))
                .filter(models.Patient.is_admitted.is_(True)).scalar() or 0)

    risk_rows = (db.query(models.Patient.risk_level, func.count(models.Patient.id))
                 .group_by(models.Patient.risk_level).all())
    risk_dist = {level.value: 0 for level in models.RiskLevel}
    for level, count in risk_rows:
        risk_dist[level.value] = count

    disease_rows = (db.query(models.Patient.primary_diagnosis,
                             func.count(models.Patient.id).label("c"))
                    .filter(models.Patient.primary_diagnosis.isnot(None))
                    .group_by(models.Patient.primary_diagnosis)
                    .order_by(func.count(models.Patient.id).desc())
                    .limit(10).all())

    return schemas.DashboardStats(
        total_patients=total,
        admitted_patients=admitted,
        high_risk_count=risk_dist["high"],
        critical_count=risk_dist["critical"],
        bed_occupancy_pct=round(admitted / TOTAL_BEDS * 100, 1),
        disease_distribution=[
            schemas.DiseaseCount(diagnosis=d, count=c) for d, c in disease_rows
        ],
        risk_distribution=risk_dist,
    )
