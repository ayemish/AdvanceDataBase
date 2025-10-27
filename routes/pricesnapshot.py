from fastapi import APIRouter, HTTPException, Query
from models.pricesnapshot import PriceSnapshot
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional

load_dotenv()
router = APIRouter()
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"))
db = client["flighttrack_python"]
snapshots_collection = db["price_snapshots"]

@router.get("/flights/{flight_id}/prices")
async def get_price_history(
    flight_id: str,
    start_date: Optional[str] = Query(None, description="ISO format: 2025-10-15"),
    end_date: Optional[str] = Query(None, description="ISO format: 2025-12-31")
):
    """Get price history for a specific flight"""
    query = {"flight_id": flight_id}
    
    # Add date filters if provided
    if start_date or end_date:
        query["fetched_at"] = {}
        if start_date:
            query["fetched_at"]["$gte"] = datetime.fromisoformat(start_date)
        if end_date:
            query["fetched_at"]["$lte"] = datetime.fromisoformat(end_date)
    
    snapshots = list(snapshots_collection.find(query).sort("fetched_at", 1))
    
    if not snapshots:
        raise HTTPException(status_code=404, detail="No price history found")
    
    # Convert MongoDB objects to JSON-serializable format
    for snap in snapshots:
        snap["_id"] = str(snap["_id"])
        if isinstance(snap.get("fetched_at"), datetime):
            snap["fetched_at"] = snap["fetched_at"].isoformat()
    
    return {
        "flight_id": flight_id,
        "count": len(snapshots),
        "prices": snapshots
    }

@router.post("/flights/{flight_id}/prices")
async def add_price_snapshot(flight_id: str, snapshot: PriceSnapshot):
    """Add a new price snapshot for a flight"""
    snapshot_dict = snapshot.dict()
    snapshot_dict["flight_id"] = flight_id
    snapshot_dict["fetched_at"] = datetime.utcnow()
    
    result = snapshots_collection.insert_one(snapshot_dict)
    snapshot_dict["_id"] = str(result.inserted_id)
    
    return {
        "message": "Price snapshot added successfully",
        "snapshot": snapshot_dict
    }

@router.get("/prices/latest")
async def get_latest_prices(limit: int = Query(10, ge=1, le=100)):
    """Get latest price snapshots across all flights"""
    pipeline = [
        {"$sort": {"fetched_at": -1}},
        {"$group": {
            "_id": "$flight_id",
            "latest_price": {"$first": "$price"},
            "currency": {"$first": "$currency"},
            "fetched_at": {"$first": "$fetched_at"}
        }},
        {"$limit": limit}
    ]
    
    results = list(snapshots_collection.aggregate(pipeline))
    
    for result in results:
        result["flight_id"] = result.pop("_id")
        if isinstance(result.get("fetched_at"), datetime):
            result["fetched_at"] = result["fetched_at"].isoformat()
    
    return {"latest_prices": results}