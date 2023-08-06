# API Analytics

## Installation

```bash
python -m pip install api-analytics
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

### Flask

```py
from flask import Flask
from api_analytics.flask import add_middleware

app = Flask(__name__)
add_middleware(app, <api_key>)

@app.get("/")
def root():
    return {"message": "Hello World"}
```
