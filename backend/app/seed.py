"""Seed the database with realistic demo patients for the hackathon demo.

Run from backend/:  python -m app.seed
"""
import random
from datetime import datetime, timedelta, timezone

from .database import Base, SessionLocal, engine
from .models import Patient, VitalsHistory, RiskLevel, Gender

DIAGNOSES = [
    "Type 2 Diabetes", "Hypertension", "Pneumonia", "Acute MI",
    "COPD", "Chronic Kidney Disease", "Sepsis", "Asthma",
    "Congestive Heart Failure", "Dengue Fever",
]

FIRST = ["Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Sneha", "Arjun",
         "Meera", "Karan", "Divya", "Rahul", "Isha", "Sanjay", "Pooja"]
LAST = ["Sharma", "Patel", "Reddy", "Iyer", "Khan", "Gupta", "Nair",
        "Singh", "Das", "Mehta"]

RISK_WEIGHTS = [(RiskLevel.LOW, 0.45), (RiskLevel.MEDIUM, 0.3),
                (RiskLevel.HIGH, 0.17), (RiskLevel.CRITICAL, 0.08)]


def seed(n_patients: int = 30):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Patient).count() > 0:
            print("Database already seeded — skipping. Delete medinexus.db to reseed.")
            return

        now = datetime.now(timezone.utc)
        for i in range(1, n_patients + 1):
            risk = random.choices([r for r, _ in RISK_WEIGHTS],
                                  weights=[w for _, w in RISK_WEIGHTS])[0]
            admitted = risk in (RiskLevel.HIGH, RiskLevel.CRITICAL) or random.random() < 0.3
            p = Patient(
                mrn=f"MRN-{i:05d}",
                first_name=random.choice(FIRST),
                last_name=random.choice(LAST),
                age=random.randint(18, 90),
                gender=random.choice(list(Gender)),
                blood_group=random.choice(["A+", "B+", "O+", "AB+", "O-", "A-"]),
                primary_diagnosis=random.choice(DIAGNOSES),
                risk_level=risk,
                risk_score={"low": 15, "medium": 45, "high": 72, "critical": 91}[risk.value]
                           + random.uniform(-8, 8),
                is_admitted=admitted,
                bed_number=f"B-{i:02d}" if admitted else None,
                admission_date=now - timedelta(days=random.randint(0, 14)) if admitted else None,
            )
            db.add(p)
            db.flush()

            # 24h of hourly vitals per patient
            for h in range(24):
                sick = risk in (RiskLevel.HIGH, RiskLevel.CRITICAL)
                db.add(VitalsHistory(
                    patient_id=p.id,
                    heart_rate=random.gauss(95 if sick else 75, 8),
                    systolic_bp=random.gauss(145 if sick else 120, 10),
                    diastolic_bp=random.gauss(90 if sick else 78, 6),
                    temperature=round(random.gauss(38.2 if sick else 36.8, 0.4), 1),
                    spo2=min(100, random.gauss(92 if sick else 98, 1.5)),
                    respiratory_rate=random.gauss(22 if sick else 15, 2),
                    glucose=random.gauss(180 if sick else 105, 20),
                    source="sensor_sim",
                    recorded_at=now - timedelta(hours=23 - h),
                ))

        db.commit()
        print(f"Seeded {n_patients} patients with 24h vitals each.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
