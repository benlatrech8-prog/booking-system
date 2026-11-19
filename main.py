from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from booking_db import BookingDB

app = FastAPI()
db = BookingDB("booking.db")

class BookingRequest(BaseModel):
    client_id: int
    service_id: int
    date: str
    start_time: str

@app.post("/test-booking", status_code=201)
def test_booking(booking: BookingRequest):
    return booking
