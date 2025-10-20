from fastapi import APIRouter, HTTPException
from models.flight import Flight
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["flighttrack"]
flights_collection = db["flights"]

@router.get("/flights")
async def get_flights():
    return list(flights_collection.find())

@router.get("/flights/{flight_id}")
async def get_flight(flight_id: str):
    flight = flights_collection.find_one({"flight_id": flight_id})
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight

@router.post("/flights")
async def create_flight(flight: Flight):
    flight_dict = flight.dict()
    result = flights_collection.insert_one(flight_dict)
    return {**flight_dict, "_id": str(result.inserted_id)}