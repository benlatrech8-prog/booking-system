# Car Wash Booking System

Backend for a car wash booking system, built with Python and SQLite.

## Why
I had built a static frontend for a car wash. This project turns it into a
real application with a database and a backend.

## Database
Three tables:
- **clients**: name, phone, email
- **services**: the menu (name, duration in minutes, price)
- **bookings**: who booked which service, and when. Linked to clients and
  services with foreign keys.

## Business rules
- No double booking: a new booking can't overlap an existing one.
- Bookings only during opening hours (08:00–20:00).

## How to run
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python3 seed.py
    fastapi dev main.py
Then open http://127.0.0.1:8000/docs

## Tests
    pytest

## Status
✅ Done: 
- database layer.
- REST API with FastAPI (GET /services, GET /bookings).
- POST /clients.
- POST /bookings with 201/400/404/409.
- tests with pytest.
- Cancel a booking (DELETE /bookings/{id}).
- Show free time slots for a day(GET /slots).

🚧 Next:
- Run the tests automatically on GitHub (CI)
- Deploy with Docker
