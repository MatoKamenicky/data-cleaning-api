import pandas as pd
import numpy as np

def clean_dataframe(df: pd.DataFrame):
    report = {}

    # Basic info
    report["rows"] = len(df)
    report["columns"] = df.shape[1]

    # Missing values
    missing = df.isna().sum()
    report["missing_values"] = missing[missing > 0].to_dict()

    # Duplicate rows
    duplicates = df.duplicated().sum()
    report["duplicate_rows"] = int(duplicates)

    # Fill missing values
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("UNKNOWN")

    # Simple outlier detection (IQR)
    outliers = {}
    for col in df.select_dtypes(include=np.number).columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        outlier_count = ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum()
        if outlier_count > 0:
            outliers[col] = int(outlier_count)

    report["outliers"] = outliers

    return df, report
