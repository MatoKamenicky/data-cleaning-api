from pydantic import BaseModel
from typing import Dict, Any, List

class ValidationResponse(BaseModel):
    rows: int
    columns: int
    missing_values: Dict[str, int]
    duplicate_rows: int
    outliers: Dict[str, int]

class CleanResponse(BaseModel):
    report: ValidationResponse
    data: List[Dict[str, Any]]
