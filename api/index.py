from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from datetime import datetime

app = FastAPI(
    title="Japan Real Estate API",
    description="Japan real estate and housing market data including land prices, residential construction, mortgage rates, and housing indicators. Powered by World Bank Open Data.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/JP/indicator"

INDICATORS = {
    "urban_pop":        {"id": "SP.URB.TOTL.IN.ZS",  "name": "Urban Population",                "unit": "% of Total"},
    "urban_growth":     {"id": "SP.URB.GROW",         "name": "Urban Population Growth",         "unit": "Annual %"},
    "construction":     {"id": "NV.IND.MANF.ZS",      "name": "Manufacturing Value Added",       "unit": "% of GDP"},
    "household_exp":    {"id": "NE.CON.PRVT.PC.KD",   "name": "Household Consumption Per Capita","unit": "Constant 2015 USD"},
    "domestic_credit":  {"id": "FS.AST.DOMS.GD.ZS",  "name": "Domestic Credit to Private Sector","unit": "% of GDP"},
    "real_interest":    {"id": "FR.INR.RINR",          "name": "Real Interest Rate",              "unit": "%"},
    "lending_rate":     {"id": "FR.INR.LEND",          "name": "Lending Interest Rate",           "unit": "%"},
    "fdi_inflows":      {"id": "BX.KLT.DINV.CD.WD",   "name": "FDI Net Inflows",                 "unit": "Current USD"},
}


async def fetch_wb(indicator_id: str, limit: int = 10):
    url = f"{WB_BASE_URL}/{indicator_id}"
    params = {"format": "json", "mrv": limit, "per_page": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(url, params=params)
        data = res.json()
    if not data or len(data) < 2:
        return []
    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Japan Real Estate API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "World Bank Open Data",
        "country": "Japan (JP)",
        "endpoints": [
            "/summary", "/urban-population", "/urban-growth", "/construction",
            "/household-spending", "/credit", "/interest-rate", "/lending-rate", "/fdi"
        ],
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=5, ge=1, le=30)):
    """All Japan real estate and housing indicators snapshot"""
    results = {}
    for key, meta in INDICATORS.items():
        results[key] = await fetch_wb(meta["id"], limit)
    formatted = {
        key: {"name": INDICATORS[key]["name"], "unit": INDICATORS[key]["unit"], "data": results[key]}
        for key in INDICATORS
    }
    return {"country": "Japan", "country_code": "JP", "source": "World Bank Open Data", "updated_at": datetime.utcnow().isoformat() + "Z", "indicators": formatted}


@app.get("/urban-population")
async def urban_population(limit: int = Query(default=10, ge=1, le=60)):
    """Urban population as % of total (urbanization rate)"""
    data = await fetch_wb("SP.URB.TOTL.IN.ZS", limit)
    return {"indicator": "Urban Population", "series_id": "SP.URB.TOTL.IN.ZS", "unit": "% of Total", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/urban-growth")
async def urban_growth(limit: int = Query(default=10, ge=1, le=60)):
    """Urban population growth rate (annual %)"""
    data = await fetch_wb("SP.URB.GROW", limit)
    return {"indicator": "Urban Population Growth", "series_id": "SP.URB.GROW", "unit": "Annual %", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/construction")
async def construction(limit: int = Query(default=10, ge=1, le=60)):
    """Manufacturing and construction value added (% of GDP)"""
    data = await fetch_wb("NV.IND.MANF.ZS", limit)
    return {"indicator": "Manufacturing Value Added", "series_id": "NV.IND.MANF.ZS", "unit": "% of GDP", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/household-spending")
async def household_spending(limit: int = Query(default=10, ge=1, le=60)):
    """Household final consumption expenditure per capita (constant 2015 USD)"""
    data = await fetch_wb("NE.CON.PRVT.PC.KD", limit)
    return {"indicator": "Household Consumption Per Capita", "series_id": "NE.CON.PRVT.PC.KD", "unit": "Constant 2015 USD", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/credit")
async def credit(limit: int = Query(default=10, ge=1, le=60)):
    """Domestic credit to private sector (% of GDP) — reflects mortgage availability"""
    data = await fetch_wb("FS.AST.DOMS.GD.ZS", limit)
    return {"indicator": "Domestic Credit to Private Sector", "series_id": "FS.AST.DOMS.GD.ZS", "unit": "% of GDP", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/interest-rate")
async def interest_rate(limit: int = Query(default=10, ge=1, le=60)):
    """Real interest rate (%)"""
    data = await fetch_wb("FR.INR.RINR", limit)
    return {"indicator": "Real Interest Rate", "series_id": "FR.INR.RINR", "unit": "%", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/lending-rate")
async def lending_rate(limit: int = Query(default=10, ge=1, le=60)):
    """Lending interest rate (%)"""
    data = await fetch_wb("FR.INR.LEND", limit)
    return {"indicator": "Lending Interest Rate", "series_id": "FR.INR.LEND", "unit": "%", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}


@app.get("/fdi")
async def fdi(limit: int = Query(default=10, ge=1, le=60)):
    """Foreign direct investment net inflows (current USD)"""
    data = await fetch_wb("BX.KLT.DINV.CD.WD", limit)
    return {"indicator": "FDI Net Inflows", "series_id": "BX.KLT.DINV.CD.WD", "unit": "Current USD", "frequency": "Annual", "country": "Japan", "source": "World Bank", "updated_at": datetime.utcnow().isoformat() + "Z", "data": data}

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
