"""Patient CRUD + vitals endpoints."""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/patients", tags=["patients"])


def _generate_mrn(db: Session) -> str:
    """MRN-00001 style sequential medical record number."""
    last = db.query(models.Patient).order_by(models.Patient.id.desc()).first()
    next_id = (last.id + 1) if last else 1
    return f"MRN-{next_id:05d}"


@router.post("/", response_model=schemas.PatientOut, status_code=201)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = models.Patient(**payload.model_dump(), mrn=_generate_mrn(db))
    if patient.is_admitted:
        patient.admission_date = datetime.now(timezone.utc)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/", response_model=schemas.PatientListOut)
def list_patients(
    search: Optional[str] = Query(None, description="Search name, MRN, or diagnosis"),
    risk_level: Optional[models.RiskLevel] = None,
    admitted_only: bool = False,
    skip: int = 0,
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(models.Patient)

    if search:
        like = f"%{search}%"
        q = q.filter(or_(
            models.Patient.first_name.ilike(like),
            models.Patient.last_name.ilike(like),
            models.Patient.mrn.ilike(like),
            models.Patient.primary_diagnosis.ilike(like),
        ))
    if risk_level:
        q = q.filter(models.Patient.risk_level == risk_level)
    if admitted_only:
        q = q.filter(models.Patient.is_admitted.is_(True))

    total = q.count()
    patients = q.order_by(models.Patient.updated_at.desc()).offset(skip).limit(limit).all()
    return {"total": total, "patients": patients}


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return patient


@router.put("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(patient_id: int, payload: schemas.PatientUpdate,
                   db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")

    data = payload.model_dump(exclude_unset=True)
    # Stamp admission date on admit; clear bed on discharge
    if data.get("is_admitted") is True and not patient.is_admitted:
        patient.admission_date = datetime.now(timezone.utc)
    if data.get("is_admitted") is False:
        data["bed_number"] = None
        data["admission_date"] = None

    for field, value in data.items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


@router.delete("/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    db.delete(patient)
    db.commit()


# ---------- Vitals (nested under patient) ----------

@router.post("/{patient_id}/vitals", response_model=schemas.VitalsOut, status_code=201)
def add_vitals(patient_id: int, payload: schemas.VitalsCreate,
               db: Session = Depends(get_db)):
    if not db.get(models.Patient, patient_id):
        raise HTTPException(404, "Patient not found")
    vitals = models.VitalsHistory(**payload.model_dump(), patient_id=patient_id)
    db.add(vitals)
    db.commit()
    db.refresh(vitals)
    return vitals


@router.get("/{patient_id}/vitals", response_model=list[schemas.VitalsOut])
def get_vitals(patient_id: int, limit: int = Query(100, le=1000),
               db: Session = Depends(get_db)):
    if not db.get(models.Patient, patient_id):
        raise HTTPException(404, "Patient not found")
    return (db.query(models.VitalsHistory)
            .filter(models.VitalsHistory.patient_id == patient_id)
            .order_by(models.VitalsHistory.recorded_at.desc())
            .limit(limit).all())
