# Data Cleaning & Validation API

A production-ready **FastAPI-based API** for cleaning, validating, and preprocessing tabular data.  
Designed for **developers, data engineers, and SaaS products** that need fast, automated data quality checks.

This API supports **CSV file uploads** and **raw JSON data**, making it ideal for browser apps, backend services, and RapidAPI monetization.


## 🚀 Features

- Upload CSV files or send JSON data
- Automatic missing value handling
- Duplicate row detection
- Outlier detection using IQR
- Cleaned data returned in JSON format
- API key authentication
- RapidAPI-ready design


## 📦 Tech Stack

- Python 3.10+
- FastAPI
- Pandas
- Pydantic
- Uvicorn / Gunicorn


## 🔐 Authentication

All endpoints require an API key sent via HTTP header:


## ⚙️ Installation (Local)

### 1️⃣ Clone repository

``` bash
git clone https://github.com/your-username/data-cleaning-api.git
cd data-cleaning-api
```

### 2️⃣ Install dependencies

``` bash
pip install -r requirements.txt
```

### 3️⃣ Set API key

**Windows (PowerShell)**

``` powershell
$env:API_KEY="your-api-key"
```

**Linux / macOS**

``` bash
export API_KEY=your-api-key
```

### 4️⃣ Run server

``` bash
uvicorn app.main:app --reload
```

## 🔌 Endpoints

### `POST /clean`

Upload a CSV file and receive cleaned data + validation report.

**Request** - `multipart/form-data` - CSV file

### `POST /validate`

Upload a CSV file and receive validation report only.

**Request** - `multipart/form-data` - CSV file


### `POST /clean-json`

Send raw JSON data and receive cleaned data + validation report.

**Request**

``` json
[
  {"age": 25, "city": "Berlin"},
  {"age": null, "city": "Paris"}
]
```


## 🧪 Example cURL (JSON)

``` bash
curl -X POST http://127.0.0.1:8000/clean-json \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-key" \
  -d '[{"age":25,"city":"Berlin"},{"age":null,"city":"Paris"}]'
```


## 🛡️ Limits

-   Max file size: **10 MB**
-   Max rows: **100,000**
-   Designed for SaaS pricing tiers


## 🌍 Deployment

This API is ready for deployment on: - Railway - Render - Fly.io -
Docker / VPS

Set the `API_KEY` environment variable in your hosting provider.