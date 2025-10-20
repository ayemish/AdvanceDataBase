from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime
import random

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/flighttrack")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["flighttrack_python"]
flights_collection = db["flights"]
snapshots_collection = db["price_snapshots"]

# Clear existing data
flights_collection.delete_many({})
snapshots_collection.delete_many({})

# Flight data
flights = [
    {"flightId": "F001", "route": {"from": "LHE", "to": "BKK"}, "airline": "AirExample", "flight_date": "2026-01-15", "tracking": {"enabled": True, "start_threshold_days_before": 180, "interval": "1w"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F002", "route": {"from": "SIN", "to": "BKK"}, "airline": "BudgetSky", "flight_date": "2025-12-05", "tracking": {"enabled": True, "start_threshold_days_before": 90, "interval": "1d"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F003", "route": {"from": "LHE", "to": "JED"}, "airline": "RoyalAir", "flight_date": "2025-11-20", "tracking": {"enabled": True, "start_threshold_days_before": 60, "interval": "1w"}, "metadata": {"cabin": "business"}, "created_at": datetime.utcnow()},
    {"flightId": "F004", "route": {"from": "DXB", "to": "LHR"}, "airline": "SkyConnect", "flight_date": "2026-02-10", "tracking": {"enabled": True, "start_threshold_days_before": 120, "interval": "1w"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F005", "route": {"from": "KHI", "to": "IST"}, "airline": "EasternAir", "flight_date": "2025-12-25", "tracking": {"enabled": True, "start_threshold_days_before": 90, "interval": "1d"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F006", "route": {"from": "LHE", "to": "DXB"}, "airline": "AirExample", "flight_date": "2026-03-05", "tracking": {"enabled": True, "start_threshold_days_before": 180, "interval": "1w"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F007", "route": {"from": "BKK", "to": "SIN"}, "airline": "BudgetSky", "flight_date": "2026-01-01", "tracking": {"enabled": True, "start_threshold_days_before": 120, "interval": "1d"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F008", "route": {"from": "JED", "to": "LHE"}, "airline": "RoyalAir", "flight_date": "2025-11-28", "tracking": {"enabled": True, "start_threshold_days_before": 60, "interval": "1w"}, "metadata": {"cabin": "business"}, "created_at": datetime.utcnow()},
    {"flightId": "F009", "route": {"from": "SIN", "to": "HKG"}, "airline": "AsiaFly", "flight_date": "2026-02-20", "tracking": {"enabled": True, "start_threshold_days_before": 120, "interval": "1w"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()},
    {"flightId": "F010", "route": {"from": "LHE", "to": "CPE"}, "airline": "IslandAir", "flight_date": "2026-04-01", "tracking": {"enabled": True, "start_threshold_days_before": 180, "interval": "1w"}, "metadata": {"cabin": "economy"}, "created_at": datetime.utcnow()}
]

# Insert flights
result = flights_collection.insert_many(flights)
print(f"Inserted {len(result.inserted_ids)} flights.")

# Generate snapshots
snapshots = []
for i, flight in enumerate(flights):
    base_price = 100 + i * 30 + random.uniform(0, 200)
    snapshots.append({
        "flight_id": flight["flightId"],
        "fetched_at": datetime(2025, 10, 15),
        "price": round(base_price, 2),
        "currency": "USD",
        "source": "simulator"
    })
    snapshots.append({
        "flight_id": flight["flightId"],
        "fetched_at": datetime(2025, 11, 1),
        "price": round(base_price * (1 + random.uniform(0, 0.1)), 2),
        "currency": "USD",
        "source": "simulator"
    })
    snapshots.append({
        "flight_id": flight["flightId"],
        "fetched_at": datetime(2025, 11, 15),
        "price": round(base_price * (1 + random.uniform(0, 0.2)), 2),
        "currency": "USD",
        "source": "simulator"
    })

# Insert snapshots
snapshot_result = snapshots_collection.insert_many(snapshots)
print(f"Inserted {len(snapshot_result.inserted_ids)} price snapshots.")

# Close connection
client.close()
print("Seed complete!")