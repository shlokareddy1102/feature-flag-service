from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from pathlib import Path
from fastapi.staticfiles import StaticFiles

import models
from database import SessionLocal, engine
from models import User, FeatureFlag, FeatureLog
from schemas import (
    UserCreate,
    UserResponse,
    FeatureCreate,
    FeatureUpdate,
    FeatureResponse,
)
import os
print("CWD:", os.getcwd())

app = FastAPI()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)



# Create database tables
models.Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"message": "FastAPI is running on my Mac 🚀"}


# ---------------- USERS ----------------
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------------- FEATURE CHECK ----------------
@app.get("/check-feature")
def check_feature(
    user_id: int,
    feature_name: str,
    db: Session = Depends(get_db)
):
    feature = (
        db.query(FeatureFlag)
        .filter(FeatureFlag.name == feature_name)
        .first()
    )

    enabled = False

    if feature and feature.enabled:
        rollout = random.randint(1, 100)
        enabled = rollout <= feature.rollout_percentage

    log = FeatureLog(
        user_id=user_id,
        feature_name=feature_name,
        result=enabled
    )
    db.add(log)
    db.commit()

    return {
        "feature": feature_name,
        "enabled": enabled
    }


# ---------------- ADMIN CRUD ----------------
@app.post("/features", response_model=FeatureResponse)
def create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    existing = db.query(FeatureFlag).filter(FeatureFlag.name == feature.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Feature already exists")

    new_feature = FeatureFlag(
        name=feature.name,
        enabled=feature.enabled,
        rollout_percentage=feature.rollout_percentage
    )
    db.add(new_feature)
    db.commit()
    db.refresh(new_feature)
    return new_feature


@app.get("/features", response_model=List[FeatureResponse])
def list_features(db: Session = Depends(get_db)):
    return db.query(FeatureFlag).all()


@app.put("/features/{feature_name}", response_model=FeatureResponse)
def update_feature(
    feature_name: str,
    update: FeatureUpdate,
    db: Session = Depends(get_db)
):
    feature = db.query(FeatureFlag).filter(FeatureFlag.name == feature_name).first()
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")

    feature.enabled = update.enabled
    feature.rollout_percentage = update.rollout_percentage
    db.commit()
    db.refresh(feature)
    return feature
