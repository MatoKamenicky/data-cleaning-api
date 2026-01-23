from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from app.cleaner import clean_dataframe
from app.schemas import CleanResponse, ValidationResponse

app = FastAPI(
    title="Data Cleaning & Validation API",
    description="Upload CSV data and receive cleaned data + validation report",
    version="1.0.0"
)

@app.post("/clean", response_model=CleanResponse)
async def clean_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    df = pd.read_csv(file.file)

    cleaned_df, report = clean_dataframe(df)

    return {
        "report": report,
        "data": cleaned_df.to_dict(orient="records")
    }

@app.post("/validate", response_model=ValidationResponse)
async def validate_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    df = pd.read_csv(file.file)

    _, report = clean_dataframe(df)

    return report
