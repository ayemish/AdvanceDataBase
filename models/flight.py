from pydantic import BaseModel
from typing import Optional

class Flight(BaseModel):
    flight_id: str
    route: dict
    airline: str
    flight_date: str  # ISO format, e.g., "2025-01-20"

    class Config:
        schema_extra = {
            "example": {
                "flight_id": "DL123",
                "route": {"from": "JFK", "to": "LAX"},
                "airline": "Delta",
                "flight_date": "2025-01-20"
            }
        }