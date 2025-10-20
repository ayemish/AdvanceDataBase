from pydantic import BaseModel
from datetime import datetime

class PriceSnapshot(BaseModel):
    flight_id: str
    price: float
    currency: str = "USD"
    fetched_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "flight_id": "DL123",
                "price": 250.50,
                "currency": "USD"
            }
        }