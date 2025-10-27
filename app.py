import utils.session
from fastapi import FastAPI
from routes.flights import router as flights_router
from routes.pricesnapshot import router as prices_router


app = FastAPI(
    title="Flight Price Tracker API",
    description="API for tracking flight prices over time with hybrid search capabilities",
    version="1.0.0"
)

# Include all routers
app.include_router(flights_router, prefix="/api", tags=["Flights"])
app.include_router(prices_router, prefix="/api", tags=["Price Snapshots"])


@app.get("/")
async def root():
    return {
        "message": "Flight Price Tracker API",
        "endpoints": {
            "flights": "/api/flights",
            "prices": "/api/flights/{flight_id}/prices",
            "search": "/api/search",
            "advanced_search": "/api/search/advanced"
        },
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)