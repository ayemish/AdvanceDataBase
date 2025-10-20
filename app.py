from fastapi import FastAPI
from routes.flights import router as flights_router

app = FastAPI()
app.include_router(flights_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)