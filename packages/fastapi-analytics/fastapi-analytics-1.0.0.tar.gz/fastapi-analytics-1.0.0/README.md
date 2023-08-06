# API Analytics

## Installation

```bash
python -m pip install fastapi-analytics
```

## Usage

### FastAPI

```py
from fastapi import FastAPI
from api_analytics.fastapi import Analytics

app = FastAPI()
app.add_middleware(Analytics, <api_key>)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
