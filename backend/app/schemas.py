"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from .models import RiskLevel, Gender


# ---------- Patient ----------

class PatientBase(BaseModel):
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    age: int = Field(..., ge=0, le=130)
    gender: Gender
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    primary_diagnosis: Optional[str] = None
    comorbidities: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    is_admitted: bool = False
    bed_number: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    """All fields optional for PATCH-style partial updates."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=130)
    gender: Optional[Gender] = None
    blood_group: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    primary_diagnosis: Optional[str] = None
    comorbidities: Optional[str] = None
    allergies: Optional[str] = None
    current_medications: Optional[str] = None
    risk_level: Optional[RiskLevel] = None
    risk_score: Optional[float] = Field(None, ge=0, le=100)
    is_admitted: Optional[bool] = None
    bed_number: Optional[str] = None


class PatientOut(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    mrn: str
    risk_level: RiskLevel
    risk_score: float
    admission_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class PatientListOut(BaseModel):
    total: int
    patients: List[PatientOut]


# ---------- Vitals ----------

class VitalsCreate(BaseModel):
    heart_rate: Optional[float] = None
    systolic_bp: Optional[float] = None
    diastolic_bp: Optional[float] = None
    temperature: Optional[float] = None
    spo2: Optional[float] = Field(None, ge=0, le=100)
    respiratory_rate: Optional[float] = None
    glucose: Optional[float] = None
    source: str = "manual"


class VitalsOut(VitalsCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    recorded_at: datetime


# ---------- Dashboard ----------

class DiseaseCount(BaseModel):
    diagnosis: str
    count: int


class DashboardStats(BaseModel):
    total_patients: int
    admitted_patients: int
    high_risk_count: int
    critical_count: int
    bed_occupancy_pct: float
    disease_distribution: List[DiseaseCount]
    risk_distribution: dict
