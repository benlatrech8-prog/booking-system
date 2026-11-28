from fastapi.testclient import TestClient
import main
from main import app
from booking_db import BookingDB

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Car wash API is running"}

def test_services():
    main.db = BookingDB(":memory:")
    main.db.add_service("wash", 30, 25)

    response = client.get("/services")

    assert response.status_code == 200
    assert response.json() == [
  {
    "id": 1,
    "name": "wash",
    "duration": 30,
    "price": 25

  }
]

def test_create_booking():
    # Arrange: a fresh book with 1 client and 1 service

    main.db = BookingDB(":memory:")
    main.db.add_client("Ali", "0151 0000000", "ali@example.com")
    main.db.add_service("wash", 30, 25)

    # Act: POST a booking (json= is the body 📝)
    response = client.post("/bookings", json={
        "client_id": 1,
        "service_id": 1,
        "date": "2026-11-25",
        "start_time": "10:00",
    })

    #assert
    assert response.status_code == 201
    assert response.json() == {"message": "Booking created"}

    response = client.post("/bookings", json={
        "client_id": 1,
        "service_id": 1,
        "date": "2026-11-25",
        "start_time": "10:00",
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "This time slot is already taken"}

    response = client.post("/bookings", json={
        "client_id": 22,
        "service_id": 1,
        "date": "2026-11-25",
        "start_time": "10:00",
    })

    assert response.status_code == 404
    assert response.json() == {"detail": "This client doesn't exist"}

    response = client.post("/bookings", json={
        "client_id": 1,
        "service_id": 1,
        "date": "2026-11-25",
        "start_time": "22:00",
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "We are open from 08:00 to 20:00"}

    response = client.post("/bookings", json={
        "client_id": 1,
        "service_id": 12,
        "date": "2026-11-25",
        "start_time": "",
    })

    assert response.status_code == 404
    assert response.json() == {"detail": "This service doesn't exist"}

def test_list_bookings():
        main.db = BookingDB(":memory:")
        main.db.add_client("Ali", "0150 000000", "ali@examlp.com")
        main.db.add_service("wash", 30, 25)
        main.db.add_booking(1, 1, "2026-11-25", "10:00")

        response =client.get("/bookings?date=2026-11-25")

        assert response.status_code == 200
        assert response.json() == [
        {"client": "Ali", "service": "wash", "start": "10:00", "end": "10:30"}
        ]

        response = client.get("/bookings?date=2030-11-25")

        assert response.status_code == 200
        assert response.json() == []

def test_cancel_booking():
    main.db = BookingDB(":memory:")
    main.db.add_client("Ali", "0150 000000", "ali@examlp.com")
    main.db.add_service("wash", 30, 25)
    main.db.add_booking(1, 1, "2026-11-25", "10:00")

    response = client.delete("/bookings/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Booking deleted"}

    response = client.delete("/bookings/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "This booking doesn't exist "}

    response = client.delete("/bookings/abc")
    assert response.status_code == 422

def test_slots_on():
    main.db= BookingDB(":memory:")
    main.db.add_client("Ali", "0150 000000", "ali@examlp.com")
    main.db.add_service("wash", 30, 25)
    main.db.add_service("full wash", 60, 45)
    main.db.add_booking(1, 1, "2026-11-29", "10:00")

    response = client.get("/slots?date=2026-11-29&service_id=2")
    assert response.status_code == 200    # 200
    slots = response.json()
    assert {"free": "09:30", "until": "10:30"} not in slots      # overlaps the booking
    assert {"free": "09:00", "until": "10:00"} in slots          # touches only
    assert {"free": "10:00", "until": "11:00"} not in slots

    response = client.get("/slots?date=2026-11-29&service_id=99")
    assert response.status_code == 404
    assert response.json() == {"detail": "This service doesn't exist"}
