from fastapi import FastAPI
from booking_db import BookingDB

app = FastAPI()
db = BookingDB("booking.db")

@app.get("/bookings")
def list_bookings(date: str):
    return db.bookings_on(date)
