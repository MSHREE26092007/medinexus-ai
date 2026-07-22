"""SQLAlchemy models for MediNexus AI — Phase 1 core schema."""
import enum
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum, Boolean
)
from sqlalchemy.orm import relationship

from .database import Base


def utcnow():
    return datetime.now(timezone.utc)


class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    mrn = Column(String(20), unique=True, index=True, nullable=False)  # Medical Record Number
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    blood_group = Column(String(5))
    phone = Column(String(20))
    address = Column(Text)

    # Clinical fields
    primary_diagnosis = Column(String(255), index=True)
    comorbidities = Column(Text)  # comma-separated for hackathon simplicity
    allergies = Column(Text)
    current_medications = Column(Text)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW, index=True)
    risk_score = Column(Float, default=0.0)  # 0–100, updated by ML module later

    # Admission / bed tracking (drives bed-occupancy stat)
    is_admitted = Column(Boolean, default=False, index=True)
    bed_number = Column(String(10), nullable=True)
    admission_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)

    vitals = relationship("VitalsHistory", back_populates="patient",
                          cascade="all, delete-orphan", lazy="dynamic")
    reports = relationship("MedicalReport", back_populates="patient",
                           cascade="all, delete-orphan")
    consultations = relationship("Consultation", back_populates="patient",
                                 cascade="all, delete-orphan")


class VitalsHistory(Base):
    __tablename__ = "vitals_history"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)

    heart_rate = Column(Float)          # bpm
    systolic_bp = Column(Float)         # mmHg
    diastolic_bp = Column(Float)        # mmHg
    temperature = Column(Float)         # °C
    spo2 = Column(Float)                # %
    respiratory_rate = Column(Float)    # breaths/min
    glucose = Column(Float)             # mg/dL

    source = Column(String(20), default="manual")  # manual | sensor_sim
    recorded_at = Column(DateTime, default=utcnow, index=True)

    patient = relationship("Patient", back_populates="vitals")


class MedicalReport(Base):
    __tablename__ = "medical_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    report_type = Column(String(50), default="general")  # discharge | lab | ai_generated ...
    content = Column(Text)
    file_path = Column(String(500), nullable=True)  # PDF/DOCX path (Module 5)
    created_at = Column(DateTime, default=utcnow)

    patient = relationship("Patient", back_populates="reports")


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_name = Column(String(100))
    chief_complaint = Column(Text)
    notes = Column(Text)
    ai_summary = Column(Text, nullable=True)  # filled by LLM module later
    created_at = Column(DateTime, default=utcnow)

    patient = relationship("Patient", back_populates="consultations")
