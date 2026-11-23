from fastapi import FastAPI, HTTPException      # FastAPI = the reception desk, HTTPException = to send error codes
from pydantic import BaseModel                  # to describe the shape of the JSON body
from booking_db import BookingDB                # my database class (booking_db.py → booking_db)

app = FastAPI()                                 # create the reception desk 🛎️
db = BookingDB("booking.db")                    # open the book 📒 (a real file: data stays)


# --- the shape of the "paper" the client sends for a booking 📝 ---
class BookingRequest(BaseModel):
    client_id: int
    service_id: int
    date: str          # "YYYY-MM-DD"
    start_time: str    # "HH:MM"
# --- GET / : just to check the API is alive ---
@app.get("/")                                   # GET + URL "/"
def home():
    return {"message": "Car wash API is running"}       # dict → JSON, status 200


# --- GET /services : show the menu 📋 ---
@app.get("/services")                           # GET + URL "/services"
def list_services():
    return db.get_services()                    # ask the book, return the list → JSON, 200


# --- GET /bookings?date=... : bookings of one day 📅 ---
@app.get("/bookings")                           # GET + URL "/bookings"
def list_bookings(date: str):                   # "date" is not in the URL path → FastAPI reads it after "?"
    return db.bookings_on(date)                 # empty day → [] with 200 (not 404!)
                                                # no date at all → 422 automatically (FastAPI)


# --- POST /bookings : create a booking 🔒 ---
@app.post("/bookings", status_code=201)         # POST + same URL, success = 201 Created
def create_booking(booking: BookingRequest):    # FastAPI: JSON body → Pydantic → object "booking" 📦
    result = db.add_booking(booking.client_id, booking.service_id,
                            booking.date, booking.start_time)   # values come OUT of the box
    if result == "unknown_client":
        raise HTTPException(status_code=404, detail="This client doesn't exist")
    if result == "unknown_service":
        raise HTTPException(status_code=404, detail="This service doesn't exist")
    if result == "closed":
        raise HTTPException(status_code=400, detail="We are open from 08:00 to 20:00")
    if result == "taken":
        raise HTTPException(status_code=409, detail="This time slot is already taken")
    return {"message": "Booking created"}       # only "ok" reaches here → 201

class ClientRequest(BaseModel):
    name: str
    phone: str
    email: str
@app.post("/clients",status_code=201)
def create_client(client: ClientRequest):
    db.add_client(client.name, client.phone, client.email)
    return{"message": "client added"}
