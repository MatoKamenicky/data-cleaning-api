from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Security
import pandas as pd
from typing import List, Dict, Any
import os
from fastapi.security import APIKeyHeader

from app.cleaner import clean_dataframe
from app.schemas import CleanResponse, ValidationResponse


# Configuration

API_KEY = os.getenv("API_KEY")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_ROWS = 100_000


# Auth

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)
rapidapi_key_header = APIKeyHeader(name="X-RapidAPI-Key", auto_error=False)

def verify_api_key(
    api_key: str = Security(api_key_header),
    rapidapi_key: str = Security(rapidapi_key_header),
):
    key = api_key or rapidapi_key
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


# App

app = FastAPI(
    title="Data Cleaning & Validation API",
    description="Upload CSV or JSON data and receive cleaned data + validation report",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Helpers

def read_csv_safe(file: UploadFile) -> pd.DataFrame:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)

    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 10MB)")

    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format")

    if len(df) > MAX_ROWS:
        raise HTTPException(status_code=413, detail="Too many rows (max 100,000)")

    return df

# Clean CSV

@app.post("/clean", response_model=CleanResponse)
async def clean_csv(
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key)
):
    df = read_csv_safe(file)
    cleaned_df, report = clean_dataframe(df)

    return {
        "report": report,
        "data": cleaned_df.to_dict(orient="records")
    }

# Validate CSV

@app.post("/validate", response_model=ValidationResponse)
async def validate_csv(
    file: UploadFile = File(...),
    _: str = Depends(verify_api_key)
):
    df = read_csv_safe(file)
    _, report = clean_dataframe(df)
    return report

# Clean JSON

@app.post("/clean-json", response_model=CleanResponse)
async def clean_json(
    payload: List[Dict[str, Any]],
    _: str = Depends(verify_api_key)
):
    if not payload:
        raise HTTPException(status_code=400, detail="Payload cannot be empty")

    if len(payload) > MAX_ROWS:
        raise HTTPException(status_code=413, detail="Too many rows (max 100,000)")

    try:
        df = pd.DataFrame(payload)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    cleaned_df, report = clean_dataframe(df)

    return {
        "report": report,
        "data": cleaned_df.to_dict(orient="records")
    }
