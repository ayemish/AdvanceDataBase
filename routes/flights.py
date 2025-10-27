from fastapi import APIRouter, HTTPException
from models.flight import Flight
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
router = APIRouter()
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["flighttrack_python"]  # ✅ Make sure this matches seed.py
flights_collection = db["flights"]

def serialize_flight(flight):
    """Convert MongoDB document to JSON-serializable format"""
    if flight:
        flight["_id"] = str(flight["_id"])  # ✅ Convert ObjectId to string
        if isinstance(flight.get("created_at"), datetime):
            flight["created_at"] = flight["created_at"].isoformat()
    return flight

@router.get("/flights")
async def get_flights():
    """Get all flights"""
    flights = list(flights_collection.find())
    return [serialize_flight(f) for f in flights]  # ✅ Serialize each flight

@router.get("/flights/{flight_id}")
async def get_flight(flight_id: str):
    """Get a specific flight by ID"""
    flight = flights_collection.find_one({"flightId": flight_id})
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return serialize_flight(flight)  # ✅ Serialize before returning

@router.post("/flights")
async def create_flight(flight: Flight):
    """Create a new flight"""
    flight_dict = flight.dict()
    flight_dict["flightId"] = flight_dict.pop("flight_id")
    flight_dict["created_at"] = datetime.utcnow()
    
    # Check if flight already exists
    existing = flights_collection.find_one({"flightId": flight_dict["flightId"]})
    if existing:
        raise HTTPException(status_code=400, detail="Flight with this ID already exists")
    
    result = flights_collection.insert_one(flight_dict)
    flight_dict["_id"] = str(result.inserted_id)
    
    return {
        "message": "Flight created successfully",
        "flight": serialize_flight(flight_dict)
    }

@router.delete("/flights/{flight_id}")
async def delete_flight(flight_id: str):
    """Delete a flight"""
    result = flights_collection.delete_one({"flightId": flight_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Flight not found")
    return {"message": "Flight deleted successfully", "flight_id": flight_id}

@router.put("/flights/{flight_id}")
async def update_flight(flight_id: str, flight: Flight):
    """Update a flight"""
    flight_dict = flight.dict()
    flight_dict.pop("flight_id", None)  # Don't update ID
    
    result = flights_collection.update_one(
        {"flightId": flight_id},
        {"$set": flight_dict}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    updated = flights_collection.find_one({"flightId": flight_id})
    return {
        "message": "Flight updated successfully",
        "flight": serialize_flight(updated)
    }